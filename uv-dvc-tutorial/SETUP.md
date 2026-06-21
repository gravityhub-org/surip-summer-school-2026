# SURIP 2026 — student setup

Clone this repo, then build a **reproducible** project: uv environment, DVC pipeline, one `dvc repro` command.

**`pyproject.toml` and `dvc.yaml` are not in Git** — build them locally with the steps below.

---

## Job 1 — uv environment

No `pyproject.toml` is provided on purpose. Create it yourself:

```bash
uv init
```

Add every package below with `uv add` (one at a time or several together — your choice):

```
numpy
scipy
astropy
matplotlib>=3.7,<3.11
healpy
colossus
lenstronomy
requests
scienceplots
h5py
pesummary
dvc
autolens
```

**Important:** `matplotlib>=3.7,<3.11` is required — scienceplots breaks on matplotlib 3.11+.

Check imports:

```bash
uv run python -c "import healpy, colossus, scienceplots, autolens; print('OK')"
```

---

## Job 2 — DVC pipeline (`dvc.yaml`)

**Do not** run `dvc add` on data folders by hand. Every script in this repo must become a **pipeline stage**. Data is produced by fetch stages as stage `outs`.

```bash
dvc init
```

(`dvc init` needs a Git repo — use `git clone`, not a ZIP download.)

Build `dvc.yaml` at the repo root with `dvc stage add` — one command per stage. Repeat for all 6 stages (adjust name, deps, outs, script):

```bash
dvc stage add -n <stage_name> \
  -d <dependency> \
  -o <output> \
  --wdir . \
  "uv run python <script.py>"
```

Every stage needs `--wdir .` and `uv run python …` in the command.

### Required stages (all 6)

| Stage | Script | Main deps | Main outs |
|-------|--------|-----------|-----------|
| `fetch_skymaps` | `load_script/generate_skymaps.py` | load script | `data/skymaps` |
| `fetch_pe` | `load_script/load_pe.py` | load script | `data/PE` |
| `ex01_halo_ps` | `exercises/ex01_halo_ps.py` | script, `pyproject.toml` | `output/ex01_*.png` |
| `ex02_skymaps` | `exercises/ex02_skymaps.py` | script, `data/skymaps` | `output/ex02_GW150914.png`, `output/ex02_overlay.png` |
| `ex03_euclid_mock` | `exercises/ex03_euclid_mock.py` | script, `data/euclid/euclid_lens_spec.md` | `output/euclid_*` |
| `ex04_PE` | `exercises/ex04_PE.py` | script, `data/PE` | `output/ex04_corner_*.png` |

List **every file** each script writes in `outs`. If `dvc repro` complains about an uncommitted output, add it to the stage `outs` list.

See [data/DATA.md](data/DATA.md) for what the downloaded files contain.

---

## Job 3 — run the pipeline

```bash
dvc repro
```

This should download data and produce all exercise outputs in one go.

Optional debug (if one stage fails):

```bash
uv run python load_script/generate_skymaps.py
```

---

## Scripts in this repo

| Path | Role |
|------|------|
| `load_script/generate_skymaps.py` | Download GW skymap FITS |
| `load_script/load_pe.py` | Download PE HDF5 |
| `exercises/ex01_halo_ps.py` | Halo MF + P(k) |
| `exercises/ex02_skymaps.py` | GW skymap plots |
| `exercises/ex03_euclid_mock.py` | Euclid lens mock |
| `exercises/ex04_PE.py` | PE corner plots |
| `run_all.py` | Optional runner (after env works) |
