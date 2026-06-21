# Workshop data files

Instructor fetches these before class; students get them with `dvc pull`.  
Scripts: skymaps → `load_script/generate_skymaps.py` · PE → `load_script/load_pe.py`

---

## Skymaps — `data/skymaps/`

**Files:** `GW150914_skymap.fits.gz`, `GW170817_skymap.fits.gz`, `GW170814_skymap.fits.gz`  
**Used by:** `exercises/ex02_skymaps.py`

### What is inside

Each file is a **HEALPix sky map** in FITS format. The map tells you *where on the sky* the gravitational-wave source probably was, pixel by pixel.

| Column | What it is |
|--------|------------|
| `PROB` | Probability that the source lies in that pixel. All pixels sum to 1. **This is what ex02 plots.** |
| `DISTMU` | Distance estimate tied to that pixel (mean) |
| `DISTSIGMA` | Uncertainty on distance |
| `DISTNORM` | Normalisation factor for distance part |

ex02 only reads `PROB` and draws 68% / 95% sky regions. It does **not** use the distance columns.

### File name ending in `.gz`

The file may be `.fits` or `.fits.gz`. **Gzip just compresses the file** — healpy reads both the same way. Smaller for DVC storage; no change to the science.

### `coord="C"` in healpy

When ex02 calls `hp.mollview(..., coord="C")`, **`C` means equatorial coordinates** (RA / Dec on the sky). Other common choices are `G` (Galactic) or `E` (ecliptic). LIGO skymaps are stored in equatorial system, so we plot in `C`.

### Resolution

Official LIGO files use `NSIDE` 512–1024 (many small pixels). ex02 resamples to `NSIDE=256` so contours draw faster — probabilities are re-normalised after that.

```python
import healpy as hp
prob = hp.read_map("data/skymaps/GW150914_skymap.fits.gz", field=0)
prob /= prob.sum()
```

---

## PE samples — `data/PE/`

**Files:** `GW150914.hdf5`, `GW170817.hdf5`, `GW170814.hdf5`  
**Used by:** `exercises/ex04_PE.py`

### What is inside (big picture)

Each HDF5 file holds **MCMC parameter-estimation samples** from LIGO’s GWTC-1 release.  
Think of each **top-level key** as one table:

- **Rows** = individual posterior (or prior) samples  
- **Columns** = physical parameters (`m1`, `m2`, spins, distance, sky position, …)

Different keys = **different waveform models** or **combined / prior** chains (see below).

---

### GW150914 and GW170814 (BBH — binary black holes)

Same four keys in both files:

| Key | What it is |
|-----|------------|
| `IMRPhenomPv2_posterior` | Posterior samples using **IMRPhenomPv2** waveform model |
| `SEOBNRv3_posterior` | Posterior samples using **SEOBNRv3** waveform model |
| `Overall_posterior` | **Combined** posterior — merge of the IMRPhenomPv2 and SEOBNRv3 chains (what LIGO quotes as the main result) |
| `prior` | Samples drawn from the **prior** only (before looking at data — useful for comparison) |

**Sample counts (this repo’s files):**

| Key | GW150914 | GW170814 |
|-----|----------|----------|
| `IMRPhenomPv2_posterior` | 40,836 | 62,644 |
| `SEOBNRv3_posterior` | 4,175 | 20,000 |
| `Overall_posterior` | 8,350 | 40,000 |
| `prior` | 34,393 | 4,173 |

**ex04 uses:** `Overall_posterior` for both events.

**Parameter columns (10 fields):**  
`costheta_jn`, `luminosity_distance_Mpc`, `right_ascension`, `declination`, `m1_detector_frame_Msun`, `m2_detector_frame_Msun`, `spin1`, `spin2`, `costilt1`, `costilt2`

---

### GW170817 (BNS — binary neutron star)

No `Overall_posterior` here. LIGO released **IMRPhenomPv2NRT** chains with two spin priors:

| Key | What it is |
|-----|------------|
| `IMRPhenomPv2NRT_lowSpin_posterior` | Posterior with **low-spin prior** (|a| ≤ 0.05) — **ex04 uses this one** |
| `IMRPhenomPv2NRT_highSpin_posterior` | Posterior with **high-spin prior** (|a| ≤ 0.89) |
| `IMRPhenomPv2NRT_lowSpin_prior` | Prior samples only (low-spin assumption) |
| `IMRPhenomPv2NRT_highSpin_prior` | Prior samples only (high-spin assumption) |

**Sample counts:**

| Key | Samples |
|-----|---------|
| `IMRPhenomPv2NRT_lowSpin_posterior` | 8,078 |
| `IMRPhenomPv2NRT_highSpin_posterior` | 4,041 |
| `IMRPhenomPv2NRT_lowSpin_prior` | 7,109 |
| `IMRPhenomPv2NRT_highSpin_prior` | 6,944 |

**Parameter columns (12 fields):** same as BBH, plus **`lambda1`, `lambda2`** (tidal deformability of each neutron star).

---

### Parameter names (plain language)

| Field | Meaning |
|-------|---------|
| `m1_detector_frame_Msun`, `m2_detector_frame_Msun` | Component masses in detector frame [M☉] |
| `spin1`, `spin2` | Spin magnitudes of each component |
| `luminosity_distance_Mpc` | Luminosity distance [Mpc] |
| `right_ascension`, `declination` | Sky position |
| `costheta_jn` | Cosine of angle between orbital angular momentum and line of sight |
| `costilt1`, `costilt2` | Spin tilt cosines |
| `lambda1`, `lambda2` | Tidal deformability (BNS only) |

---

### Read in Python

```python
import h5py

with h5py.File("data/PE/GW150914.hdf5") as f:
    print(list(f.keys()))                    # all top-level tables
    samples = f["Overall_posterior"]
    m1 = samples["m1_detector_frame_Msun"] # 1D array, length = n samples
    print(samples.dtype.names)             # column names
```

---

## Git vs DVC

| Path | In Git? |
|------|---------|
| `data/euclid/psf_config.json` | yes (small) |
| `data/skymaps/*.fits*` | no — DVC |
| `data/PE/*.hdf5` | no — DVC |
