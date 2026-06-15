from __future__ import annotations

from typing import Dict

import torch
from torch import nn


class SmallCNN(nn.Module):
    """A small CNN classifier for CIFAR-style RGB images.

    Pipeline:
        image batch -> convolution blocks -> flatten -> linear classifier -> logits

    The model-architecture notebook visualizes the same shape flow:
        [B, 3, 32, 32] -> [B, C, 16, 16] -> [B, 2C, 8, 8] -> [B, num_classes]
    """

    def __init__(self, num_classes: int, image_size: int = 32, base_channels: int = 16):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, base_channels, kernel_size=3, padding=1), #nn.COnv2d(in_channels, out_channels, kernel_size)
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(base_channels, base_channels * 2, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        feature_size = image_size // 4  # modify image_size // 4 to image_size // (2 * number of MaxPool2d(2) in self.features) 
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(base_channels * 2 * feature_size * feature_size, num_classes), 
            # modify base_channels * 2 to the output channels of last Conv2d layer in self.features
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        logits = self.classifier(x)
        return logits


def build_model(config: Dict, num_classes: int) -> nn.Module:
    model_name = config["model"].get("name", "small_cnn")
    if model_name != "small_cnn":
        raise ValueError(f"Unknown model name: {model_name}")

    return SmallCNN(
        num_classes=num_classes,
        image_size=int(config["data"]["image_size"]),
        base_channels=int(config["model"].get("base_channels", 16)),
    )
