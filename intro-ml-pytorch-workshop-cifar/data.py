from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def build_transforms(image_size: int):
    """Build the image preprocessing pipeline.

    The dataset notebook shows the same logic first. In this script version,
    students should fill in the reusable implementation used by train.py.
    """
    # TODO 1:
    # Replace the next line with a transforms.Compose([...]) object that:
    #   1. resizes each image to (image_size, image_size)
    #   2. converts the image into a PyTorch tensor
    # Hints: copy from notebooks/01_dataset_exploration.ipynb and check torchvision.transforms documentation:
    # if you want to apply random 90 degree rotation, 
    # add transforms.Lambda(lambda x: torch.rot90(x, k=random.choice([1, 2, 3]), dims=[1, 2]))
    transform = None


    if transform is None:
        raise NotImplementedError(
            "TODO 1 in data.py: create the transform pipeline. "
            "Open notebooks/01_dataset_exploration.ipynb for the working example."
        )
    return transform


def build_dataloaders(config: Dict) -> Tuple[DataLoader, DataLoader, List[str]]:
    """Create train and validation DataLoaders.

    Expected CIFAR subset structure after running prepare_cifar10_subset.py:

        data_cifar/train/airplane/*.png
        data_cifar/train/automobile/*.png
        data_cifar/train/cat/*.png
        data_cifar/train/ship/*.png
        data_cifar/val/airplane/*.png
        data_cifar/val/automobile/*.png
        data_cifar/val/cat/*.png
        data_cifar/val/ship/*.png

    Student checks:
        - What is the shape of one batch?
        - What do B, C, H, W mean?
        - Why is train_loader shuffled but val_loader is not shuffled?
    """
    data_dir = Path(config["data"]["data_dir"])
    image_size = int(config["data"]["image_size"])
    batch_size = int(config["training"]["batch_size"])
    num_workers = int(config["data"].get("num_workers", 0))

    train_dir = data_dir / "train"
    val_dir = data_dir / "val"
    if not train_dir.exists() or not val_dir.exists():
        raise FileNotFoundError(
            f"Could not find CIFAR subset at {data_dir}.\n"
            "Create it first with:\n"
            "  python prepare_cifar10_subset.py --train-per-class 400 --val-per-class 100"
        )

    transform = build_transforms(image_size)

    # TODO 2:
    # Create train_dataset and val_dataset using torchvision.datasets.ImageFolder.
    # Hint:
    #   datasets.ImageFolder(train_dir, transform=transform)
    train_dataset = None
    val_dataset = None

    if train_dataset is None or val_dataset is None:
        raise NotImplementedError(
            "TODO 2 in data.py: create train_dataset and val_dataset using ImageFolder."
        )

    # TODO 3:
    # Wrap the datasets with DataLoader.
    # Use shuffle=True for training and shuffle=False for validation.
    # Hint:
    #   DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    train_loader = None
    val_loader = None

    if train_loader is None or val_loader is None:
        raise NotImplementedError(
            "TODO 3 in data.py: create train_loader and val_loader using DataLoader."
        )

    class_names = train_dataset.classes
    return train_loader, val_loader, class_names
