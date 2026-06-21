"""ex04_PE.py — Corner plots of PE samples for each event."""

from pathlib import Path

import corner
import h5py
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(["science", "ieee", "high-vis"])
plt.rcParams["text.usetex"] = False

ROOT   = Path(__file__).resolve().parents[1]
PE_DIR = ROOT / "data" / "PE"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

LABELS = {
    "GW150914": "Overall_posterior",
    "GW170817": "IMRPhenomPv2NRT_lowSpin_posterior",
    "GW170814": "Overall_posterior",
}

PARAMS = ["m1_detector_frame_Msun", "m2_detector_frame_Msun", "spin1", "spin2"]
LABELS_PLOT = [r"$m_1\ [M_\odot]$", r"$m_2\ [M_\odot]$", r"$a_1$", r"$a_2$"]
COLORS = {"GW150914": "navy", "GW170817": "darkgreen", "GW170814": "purple"}

for event, label in LABELS.items():
    path = PE_DIR / f"{event}.hdf5"
    with h5py.File(path, "r") as f:
        samples = f[label]
        data = np.column_stack([samples[p] for p in PARAMS])

    fig = corner.corner(
    data,
    labels=LABELS_PLOT,
    color=COLORS[event],
    levels=[0.68, 0.95],
    plot_datapoints=False,
    plot_density=False,
    fill_contours=True,
    smooth=1.0,
    hist_kwargs={"density": True, "alpha": 0.7},
    title_kwargs={"fontsize": 10},
    show_titles=True,          # ← shows median + 1σ limits on top of each 1D hist
    title_fmt=".2f",           # ← 2 decimal places
    )
    fig.suptitle(event, fontsize=16, fontweight="bold", y=1.01,
                 color=COLORS[event])

    out = OUTPUT / f"ex04_corner_{event}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out.name}")

print("Done!")