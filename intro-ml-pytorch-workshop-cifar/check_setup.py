from __future__ import annotations

from pathlib import Path

import torch
import yaml
from PIL import Image
from torchvision import datasets, transforms


def detect_device(device_setting: str = "auto") -> torch.device:
    if device_setting != "auto":
        return torch.device(device_setting)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def main():
    print("Python project setup check")
    print(f"PyTorch version: {torch.__version__}")

    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found. Run this script from the project root folder.")

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_dir = Path(config["data"]["data_dir"])
    if not (data_dir / "train").exists() or not (data_dir / "val").exists():
        raise FileNotFoundError(
            f"CIFAR subset not found at {data_dir}.\n"
            "Create it first with:\n"
            "  python prepare_cifar10_subset.py --train-per-class 400 --val-per-class 100\n"
            "For a faster test, use:\n"
            "  python prepare_cifar10_subset.py --train-per-class 100 --val-per-class 25"
        )

    device = detect_device(config["training"].get("device", "auto"))
    print(f"Detected device: {device}")

    image_size = int(config["data"].get("image_size", 32))
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
    ])
    dataset = datasets.ImageFolder(data_dir / "train", transform=transform)
    image, label = dataset[0]

    print(f"Dataset classes:   {dataset.classes}")
    print(f"One image shape:   {tuple(image.shape)}")
    print(f"One label index:   {label}")
    print("Setup check passed.")
    print("Note: train.py will run after you complete the TODOs in data.py.")


if __name__ == "__main__":
    main()
