"""Exercise 1: halo mass function and linear matter power spectrum (no data files)."""

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(["science", "ieee", "high-vis"])
plt.rcParams["text.usetex"] = False
from colossus.cosmology import cosmology
from colossus.lss import mass_function

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

os.environ.setdefault("COLOSSUS_PATH", str(ROOT / ".colossus"))
OUTPUT.mkdir(exist_ok=True)
cosmo = cosmology.setCosmology("planck18")

M = np.logspace(8, 15, 200)
dndm = mass_function.massFunction(M, 0, mdef="200c", model="despali16")

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(M, dndm, lw=2)
ax.set_xlabel(r"$M/h^{-1}M_\odot$", fontsize=12)
ax.set_ylabel(r"$dn/dM$", fontsize=12)
ax.set_title("Halo mass function (Planck18, z=0)", fontsize=14)
fig.savefig(OUTPUT / "ex01_halo_mass_function.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("  Wrote output/ex01_halo_mass_function.png")

k = np.logspace(-3, 1, 300)
pk = cosmo.matterPowerSpectrum(k, 0.0)

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(k, pk, lw=2)
ax.set_xlabel(r"$k/h\,\mathrm{Mpc}^{-1}$", fontsize=12)
ax.set_ylabel(r"$P(k)$", fontsize=12)
ax.set_title("Linear matter power spectrum (Planck18, z=0)", fontsize=14)
fig.savefig(OUTPUT / "ex01_power_spectrum.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("  Wrote output/ex01_power_spectrum.png")
