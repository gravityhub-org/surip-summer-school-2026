from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable

from PIL import Image
from torchvision.datasets import CIFAR10


DEFAULT_CLASSES = ["airplane", "automobile", "cat", "ship"]
ALL_CIFAR10_CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download CIFAR-10 and export a small ImageFolder-style subset for the workshop. "
            "The resulting folder can be loaded by data.py/train.py."
        )
    )
    parser.add_argument("--output-dir", type=str, default="data_cifar", help="Output ImageFolder dataset directory.")
    parser.add_argument("--raw-dir", type=str, default="downloads/cifar10_raw", help="Where torchvision stores the raw CIFAR-10 files.")
    parser.add_argument(
        "--classes",
        nargs="+",
        default=DEFAULT_CLASSES,
        choices=ALL_CIFAR10_CLASSES,
        help="CIFAR-10 classes to export.",
    )
    parser.add_argument("--train-per-class", type=int, default=400, help="Number of training images per class.")
    parser.add_argument("--val-per-class", type=int, default=100, help="Number of validation images per class.")
    parser.add_argument("--overwrite", action="store_true", help="Delete an existing output directory before writing.")
    return parser.parse_args()


def prepare_output_dir(output_dir: Path, classes: Iterable[str], overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(
                f"{output_dir} already exists. Use --overwrite if you want to recreate it."
            )
        shutil.rmtree(output_dir)

    for split in ["train", "val"]:
        for class_name in classes:
            (output_dir / split / class_name).mkdir(parents=True, exist_ok=True)


def export_split(dataset: CIFAR10, output_dir: Path, split: str, class_names: list[str], max_per_class: int) -> None:
    selected_counts = {name: 0 for name in class_names}
    selected_set = set(class_names)

    for image, label in dataset:
        class_name = dataset.classes[label]
        if class_name not in selected_set:
            continue
        if selected_counts[class_name] >= max_per_class:
            continue

        count = selected_counts[class_name]
        out_path = output_dir / split / class_name / f"{class_name}_{count:04d}.png"

        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        image.save(out_path)

        selected_counts[class_name] += 1

        if all(count >= max_per_class for count in selected_counts.values()):
            break

    missing = {name: max_per_class - count for name, count in selected_counts.items() if count < max_per_class}
    if missing:
        raise RuntimeError(f"Not enough images exported for split={split}: missing {missing}")

    print(f"Exported {split}: " + ", ".join(f"{k}={v}" for k, v in selected_counts.items()))


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    raw_dir = Path(args.raw_dir)

    prepare_output_dir(output_dir, args.classes, args.overwrite)

    print("Downloading/loading CIFAR-10 through torchvision...")
    train_dataset = CIFAR10(root=str(raw_dir), train=True, download=True)
    val_dataset = CIFAR10(root=str(raw_dir), train=False, download=True)

    export_split(train_dataset, output_dir, "train", args.classes, args.train_per_class)
    export_split(val_dataset, output_dir, "val", args.classes, args.val_per_class)

    print("Done.")
    print(f"Created dataset at: {output_dir.resolve()}")
    print("Expected structure:")
    print(f"  {output_dir}/train/<class_name>/*.png")
    print(f"  {output_dir}/val/<class_name>/*.png")


if __name__ == "__main__":
    main()
