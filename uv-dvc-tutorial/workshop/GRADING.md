# Grading checklist (instructor)

When a student raises their hand, on **their machine**:

```bash
cd their-repo
uv sync
dvc repro
ls output/
```

## Pass

- [ ] `pyproject.toml` exists with required packages (including `autolens`, `dvc`, matplotlib pin)
- [ ] `uv sync` succeeds
- [ ] `dvc repro` exits 0
- [ ] **6 stages** in `dvc.yaml`: `fetch_skymaps`, `fetch_pe`, `ex01_halo_ps`, `ex02_skymaps`, `ex03_euclid_mock`, `ex04_PE`
- [ ] Every stage uses `wdir: .` and `cmd: uv run python …`
- [ ] Fetch stages use `outs: data/skymaps` and `outs: data/PE` (not manual `dvc add`)
- [ ] Outputs present: ex01 PNGs, ex02 PNGs (`ex02_GW150914.png` + overlay), euclid outputs, ex04 corner PNGs
- [ ] Raw FITS/HDF5 not committed to Git

## Fail → one-line hints

| Symptom | Say |
|---------|-----|
| `ModuleNotFoundError` | Finish `uv add` from SETUP.md package list |
| scienceplots / matplotlib error | Need `matplotlib>=3.7,<3.11` |
| ex02: no skymaps | Add `fetch_skymaps` stage with `outs: data/skymaps` |
| ex04: no PE files | Add `fetch_pe` stage with `outs: data/PE` |
| Missing ex03 or ex04 stage | Every script = one stage |
| Used `dvc add` on data | Use fetch stages in pipeline instead |
| `dvc repro` output mismatch | Add missing files to stage `outs` |

Reference pipeline: [dvc.yaml.answer](dvc.yaml.answer)
