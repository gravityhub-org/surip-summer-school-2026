# DVC — instructor notes (SURIP 2026)

Assignment model: students write `dvc.yaml` with **6 stages** (2 fetch + 4 exercises). **No manual `dvc add`.**

## Learning outcomes

- **Pipeline:** each script = one stage; `dvc repro` runs fetch + plots
- **Data:** large FITS/HDF5 = stage `outs` from `load_script/` fetch stages
- **Reproducibility:** `uv sync` + `dvc repro` on any machine

## Required stages

| Stage | Script |
|-------|--------|
| `fetch_skymaps` | `load_script/generate_skymaps.py` |
| `fetch_pe` | `load_script/load_pe.py` |
| `ex01_halo_ps` | `exercises/ex01_halo_ps.py` |
| `ex02_skymaps` | `exercises/ex02_skymaps.py` |
| `ex03_euclid_mock` | `exercises/ex03_euclid_mock.py` |
| `ex04_PE` | `exercises/ex04_PE.py` |

Every stage: `wdir: .` and `cmd: uv run python …`

Reference: [dvc.yaml.answer](dvc.yaml.answer) · Grading: [GRADING.md](GRADING.md)

## Demo on projector

```bash
dvc init
cp workshop/dvc.yaml.answer dvc.yaml   # instructor only — students write their own
dvc repro
```

Second `dvc repro` should skip unchanged stages.

## If something breaks

| Issue | Fix |
|-------|-----|
| ex02: no skymaps | Missing `fetch_skymaps` stage |
| ex04: no HDF5 | Missing `fetch_pe` stage |
| Output tracking error | Add missing file to stage `outs` |
| Student used `dvc add` | Redirect to fetch stages |

See [dvc-remote-setup.md](dvc-remote-setup.md) and [GRADING.md](GRADING.md).
