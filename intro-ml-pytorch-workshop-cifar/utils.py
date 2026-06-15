from __future__ import annotations

import csv
import random
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import confusion_matrix


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device(device_setting: str = "auto") -> torch.device:
    if device_setting != "auto":
        return torch.device(device_setting)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_run_dir(config: Dict, config_path: str | Path) -> Path:
    runs_dir = Path(config["outputs"].get("runs_dir", "outputs/runs"))
    experiment_name = config.get("experiment_name", "run")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = ensure_dir(runs_dir / f"{experiment_name}_{timestamp}")

    ensure_dir(run_dir / "checkpoints")
    ensure_dir(run_dir / "figures")
    ensure_dir(run_dir / "logs")

    shutil.copy2(config_path, run_dir / "config_used.yaml")
    latest_path = ensure_dir(runs_dir.parent) / "latest_run.txt"
    latest_path.write_text(str(run_dir), encoding="utf-8")
    return run_dir


def save_metrics_csv(history: List[Dict[str, float]], path: Path) -> None:
    ensure_dir(path.parent)
    if not history:
        return
    keys = list(history[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(history)


def plot_loss_accuracy(history: List[Dict[str, float]], path: Path) -> None:
    ensure_dir(path.parent)
    epochs = [row["epoch"] for row in history]
    train_loss = [row["train_loss"] for row in history]
    val_loss = [row["val_loss"] for row in history]
    train_acc = [row["train_accuracy"] for row in history]
    val_acc = [row["val_accuracy"] for row in history]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, train_loss, marker="o", label="Train")
    axes[0].plot(epochs, val_loss, marker="o", label="Validation")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Loss curve")
    axes[0].legend()

    axes[1].plot(epochs, train_acc, marker="o", label="Train")
    axes[1].plot(epochs, val_acc, marker="o", label="Validation")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title("Accuracy curve")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def collect_predictions(model, loader, device) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    all_images = []
    all_labels = []
    all_preds = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            preds = logits.argmax(dim=1)
            all_images.append(images.detach().cpu())
            all_labels.append(labels.detach().cpu())
            all_preds.append(preds.detach().cpu())

    return (
        torch.cat(all_images, dim=0).numpy(),
        torch.cat(all_labels, dim=0).numpy(),
        torch.cat(all_preds, dim=0).numpy(),
    )


def plot_confusion_matrix(labels: np.ndarray, preds: np.ndarray, class_names: List[str], path: Path) -> None:
    ensure_dir(path.parent)
    cm = confusion_matrix(labels, preds, labels=list(range(len(class_names))))

    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(cm)
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha="right")
    ax.set_yticklabels(class_names)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_title("Confusion matrix")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_prediction_grid(
    images: np.ndarray,
    labels: np.ndarray,
    preds: np.ndarray,
    class_names: List[str],
    path: Path,
    max_images: int = 16,
) -> None:
    ensure_dir(path.parent)
    n = min(max_images, len(images))
    cols = 4
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.2, rows * 2.4))
    axes = np.array(axes).reshape(-1)
    for ax in axes:
        ax.axis("off")

    for i in range(n):
        img = np.transpose(images[i], (1, 2, 0))
        img = np.clip(img, 0, 1)
        axes[i].imshow(img)
        title = f"true: {class_names[int(labels[i])]}\npred: {class_names[int(preds[i])]}"
        axes[i].set_title(title, fontsize=8)
        axes[i].axis("off")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
