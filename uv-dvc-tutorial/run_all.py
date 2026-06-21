#!/usr/bin/env python3
"""Check packages and run SURIP 2026 exercises.

Usage:
    uv run python run_all.py
    uv run python run_all.py --exercise 1
    uv run python run_all.py --exercise 4
    uv run python run_all.py --all

Exercises 2 and 4 need data/ from dvc repro (fetch_skymaps / fetch_pe).
"""

import argparse
import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXERCISES = {
    1: ROOT / "exercises" / "ex01_halo_ps.py",
    2: ROOT / "exercises" / "ex02_skymaps.py",
    3: ROOT / "exercises" / "ex03_euclid_mock.py",
    4: ROOT / "exercises" / "ex04_PE.py",
}

print("=" * 50)
print("SURIP 2026 cosmology demo")
print("=" * 50)
print("\n[Step 1] Checking Python packages...")

packages = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("astropy", "astropy"),
    ("matplotlib", "matplotlib"),
    ("healpy", "healpy"),
    ("colossus", "colossus"),
    ("lenstronomy", "lenstronomy"),
    ("requests", "requests"),
    ("scienceplots", "scienceplots"),
    ("h5py", "h5py"),
    ("pesummary", "pesummary"),
    ("autolens", "autolens"),
]
try:
    for label, module in packages:
        importlib.import_module(module)
        print(f"  {label} OK")
except ModuleNotFoundError as exc:
    print(f"\n  Import failed: {exc}")
    print("  Hint: install packages from SETUP.md (uv init + uv add, or uv sync after bootstrap)")
    exit(1)

print("\n[Step 1] All packages OK.")

parser = argparse.ArgumentParser(description="SURIP 2026 workshop runner")
parser.add_argument("--exercise", type=int, choices=[1, 2, 3, 4])
parser.add_argument("--all", action="store_true")
args = parser.parse_args()

if args.all:
    for number in (1, 2, 3, 4):
        print(f"\n[Exercise {number}] Running {EXERCISES[number].name}...")
        result = subprocess.run([sys.executable, str(EXERCISES[number])], cwd=ROOT)
        if result.returncode != 0:
            exit(result.returncode)
    print("\nSUCCESS — all exercises complete.")
    exit(0)

if args.exercise:
    print(f"\n[Exercise {args.exercise}] Running {EXERCISES[args.exercise].name}...")
    result = subprocess.run([sys.executable, str(EXERCISES[args.exercise])], cwd=ROOT)
    if result.returncode == 0:
        print(f"\nSUCCESS — exercise {args.exercise} complete.")
    exit(result.returncode)

print("\nPackages OK. Run with --exercise 1|2|3|4 or --all")
