from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import torch
import yaml
from torch import nn
from torch.optim import Adam

from data import build_dataloaders
from model import build_model
from utils import (
    collect_predictions,
    get_device,
    make_run_dir,
    plot_confusion_matrix,
    plot_loss_accuracy,
    plot_prediction_grid,
    save_metrics_csv,
    set_seed,
)


def load_config(path: str | Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_one_epoch(model, loader, criterion, optimizer, device, train: bool):
    if train:
        model.train()
    else:
        model.eval()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    context = torch.enable_grad() if train else torch.no_grad()
    with context:
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            # Core ML step: the model outputs logits, not probabilities.
            logits = model(images)
            loss = criterion(logits, labels)

            if train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            batch_size = images.size(0)
            total_loss += loss.item() * batch_size
            total_correct += (logits.argmax(dim=1) == labels).sum().item()
            total_samples += batch_size

    return total_loss / total_samples, total_correct / total_samples


def dry_run(model, train_loader, device, class_names):
    images, labels = next(iter(train_loader))
    images = images.to(device)
    model = model.to(device)
    logits = model(images)

    print("Dry run successful.")
    print(f"Input batch shape:   {tuple(images.shape)}")
    print(f"Label batch shape:   {tuple(labels.shape)}")
    print(f"Output logits shape: {tuple(logits.shape)}")
    print(f"Number of classes:   {len(class_names)}")
    print(f"Class names:         {class_names}")


def train(config: Dict, config_path: str | Path, dry_run_only: bool = False):
    set_seed(int(config["training"].get("seed", 42)))
    torch.set_num_threads(int(config["training"].get("num_threads", 1)))

    train_loader, val_loader, class_names = build_dataloaders(config)
    num_classes = len(class_names)

    device = get_device(config["training"].get("device", "auto"))
    print(f"Using device: {device}")

    model = build_model(config, num_classes=num_classes).to(device)

    if dry_run_only:
        dry_run(model, train_loader, device, class_names)
        return None

    run_dir = make_run_dir(config, config_path)
    checkpoint_dir = run_dir / "checkpoints"
    figure_dir = run_dir / "figures"
    log_dir = run_dir / "logs"

    print(f"Run folder: {run_dir}")

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=float(config["training"]["learning_rate"]))

    epochs = int(config["training"]["epochs"])
    history: List[Dict[str, float]] = []
    best_val_acc = -1.0
    best_path = checkpoint_dir / "best_model.pt"

    print("Starting training...")
    for epoch in range(1, epochs + 1):
        train_loss, train_acc = run_one_epoch(model, train_loader, criterion, optimizer, device, train=True)
        val_loss, val_acc = run_one_epoch(model, val_loader, criterion, optimizer, device, train=False)

        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_acc,
            "val_loss": val_loss,
            "val_accuracy": val_acc,
        }
        history.append(row)

        print(
            f"Epoch {epoch:02d}/{epochs} | "
            f"train loss {train_loss:.4f} | train acc {train_acc:.3f} | "
            f"val loss {val_loss:.4f} | val acc {val_acc:.3f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_names": class_names,
                    "config": config,
                    "val_accuracy": val_acc,
                },
                best_path,
            )

    metrics_path = log_dir / "metrics.csv"
    curve_path = figure_dir / "loss_accuracy_curve.png"
    confusion_path = figure_dir / "confusion_matrix.png"
    pred_grid_path = figure_dir / "prediction_grid.png"

    save_metrics_csv(history, metrics_path)
    plot_loss_accuracy(history, curve_path)

    images, labels, preds = collect_predictions(model, val_loader, device)
    plot_confusion_matrix(labels, preds, class_names, confusion_path)
    plot_prediction_grid(
        images,
        labels,
        preds,
        class_names,
        pred_grid_path,
        max_images=int(config["outputs"].get("save_prediction_count", 16)),
    )

    print("Training complete.")
    print(f"Best checkpoint: {best_path}")
    print(f"Metrics CSV:     {metrics_path}")
    print(f"Loss curve:      {curve_path}")
    print(f"Confusion matrix:{confusion_path}")
    print(f"Prediction grid: {pred_grid_path}")
    print("Open notebooks/03_evaluate_run.ipynb to view the saved results.")
    return run_dir


def main():
    parser = argparse.ArgumentParser(description="Train a small PyTorch image classifier.")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Check one data/model pass without training.")
    args = parser.parse_args()

    config = load_config(args.config)
    train(config, config_path=args.config, dry_run_only=args.dry_run)


if __name__ == "__main__":
    main()
