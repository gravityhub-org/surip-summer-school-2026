# SURIP 2026 — uv and DVC tutorial

**Instructor:** Souvik

Assignment-style hands-on workshop: exercise scripts and setup instructions in Git; local uv environment and DVC pipeline built from [SETUP.md](SETUP.md).

```bash
git clone <repo>
cd uv-dvc-tutorial
```

`pyproject.toml` and `dvc.yaml` are not in Git — see SETUP.md for setup, then run:

```bash
dvc repro
```

| Path | Role |
|------|------|
| [SETUP.md](SETUP.md) | Package list + pipeline instructions (students) |
| [data/DATA.md](data/DATA.md) | What the downloaded files contain |
| `load_script/` | Fetch skymaps and PE data (pipeline stages) |
| `exercises/` | ex01–ex04 science scripts |
| `run_all.py` | Optional runner after the environment is configured |
