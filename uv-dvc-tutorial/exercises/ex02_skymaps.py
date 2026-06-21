"""Exercise 2: plot LIGO skymaps with contour lines — single event + overlay."""

from pathlib import Path

import healpy as hp
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(["science", "ieee", "high-vis"])
plt.rcParams["text.usetex"] = False

ROOT = Path(__file__).resolve().parents[1]
SKYMAP_DIR = ROOT / "data" / "skymaps"
OUTPUT = ROOT / "output"

EVENTS = ["GW150914", "GW170817", "GW170814"]
# COLORS = ["white", "cyan", "yellow"]
COLORS = ["navy", "darkgreen", "purple"]
NSIDE = 256
LEVELS = [0.68, 0.95]
NPTS = 800

OUTPUT.mkdir(exist_ok=True)

for event in EVENTS:
    gz = SKYMAP_DIR / f"{event}_skymap.fits.gz"
    fits = SKYMAP_DIR / f"{event}_skymap.fits"
    if not gz.exists() and not fits.exists():
        print(f"  ERROR: no skymap file for {event} in {SKYMAP_DIR}")
        print("  Hint: run fetch_skymaps stage or: dvc repro")
        exit(1)

prob_maps = {}
for event in EVENTS:
    path = SKYMAP_DIR / f"{event}_skymap.fits.gz"
    if not path.exists():
        path = SKYMAP_DIR / f"{event}_skymap.fits"

    prob = np.asarray(hp.read_map(path, field=0), dtype=float)
    prob = np.maximum(prob, 0)
    prob /= prob.sum()
    prob = hp.ud_grade(prob, NSIDE)
    prob = np.maximum(prob, 0)
    prob /= prob.sum()
    prob_maps[event] = prob

# single-event plot (GW150914)
event = EVENTS[0]
prob = prob_maps[event]

hp.mollview(prob, title=f"{event} Sky Localization", cmap="YlOrRd", unit="Probability")
hp.graticule(alpha=0.4)

sorted_idx = np.argsort(prob)[::-1]
level_map = np.zeros_like(prob)
level_map[sorted_idx] = np.cumsum(prob[sorted_idx])
smooth = hp.smoothing(level_map, fwhm=np.radians(1.0))

proj = hp.projector.MollweideProj(xsize=NPTS)
grid = proj.projmap(smooth, lambda x, y, z: hp.vec2pix(NSIDE, x, y, z))

ax = plt.gca()
x = np.linspace(-2, 2, NPTS)
y = np.linspace(-1, 1, NPTS // 2)
cs = ax.contour(
    x,
    y,
    grid,
    levels=LEVELS,
    colors=["white", "red"],
    linewidths=[1.5, 1.5],
    linestyles=["--", "-"],
)
ax.clabel(cs, fmt={0.68: "68%", 0.95: "95%"}, fontsize=9, inline=True)

plt.savefig(OUTPUT / f"ex02_{event}.png", dpi=150, bbox_inches="tight")
plt.close()

# overlay: all events
background = np.min([prob_maps[e] for e in EVENTS], axis=0)
flat_val = min(prob_maps[e].min() for e in EVENTS)
background = np.full(hp.nside2npix(NSIDE), 1e-10)
hp.mollview(
    background,
    title="LIGO Super-Event Sky Localizations",
    cmap="YlOrRd",
    unit="Probability",
    bgcolor="white",
    min = 0,
    max = 1,
    # norm="hist",   # ← histogram equalisation, all events become visible
)
hp.graticule(alpha=0.5, color="gray")

ax   = plt.gca()
proj = hp.projector.MollweideProj(xsize=NPTS)
x    = np.linspace(-2, 2, NPTS)
y    = np.linspace(-1, 1, NPTS // 2)


for event, color in zip(EVENTS, COLORS):
    sorted_idx = np.argsort(prob_maps[event])[::-1]
    level_map  = np.zeros(len(prob_maps[event]))
    level_map[sorted_idx] = np.cumsum(prob_maps[event][sorted_idx])

    grid = proj.projmap(
        hp.smoothing(level_map, fwhm=np.radians(1.0)),
        lambda x, y, z: hp.vec2pix(NSIDE, x, y, z),
    )

    # filled: dark inside 68%, lighter 68-95%
    ax.contourf(x, y, grid, levels=[0, 0.68, 0.95],
                colors=[color, color], alpha=[0.6, 0.25])
    
    # outline on top
    cs = ax.contour(x, y, grid, levels=[0.68, 0.95],
                    colors=[color, color], linewidths=[1.0, 1.8])
    ax.clabel(cs, fmt={0.68: "68%", 0.95: "95%"}, fontsize=8, inline=True)
    ax.plot([], [], color=color, lw=1.8, label=event)

plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.08),
           fontsize=9, framealpha=0.8, ncol=len(EVENTS))
plt.savefig(OUTPUT / "ex02_overlay.png", dpi=150, bbox_inches="tight")
plt.close()
print("Done!")
