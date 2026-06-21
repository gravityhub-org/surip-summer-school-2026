# uv — instructor notes (SURIP 2026)

Assignment model: students get [SETUP.md](../SETUP.md) package list, run `uv init` + `uv add`, build their own `pyproject.toml`.

## Learning outcomes

- **Why uv:** Fast Python env from a package list; lockfile (`uv.lock`) for reproducibility.
- **How:** `uv init` → `uv add …` → `uv sync` → `uv run python …`

## Lecture beats

1. Broken env = missing packages / version clashes
2. Students build `pyproject.toml` themselves — no copy-paste from instructor
3. **`matplotlib>=3.7,<3.11`** pin required for scienceplots
4. Include `dvc` and `autolens` in the list (pipeline + ex03)

## Demo on projector

```bash
uv init
uv add numpy scipy astropy "matplotlib>=3.7,<3.11" healpy colossus lenstronomy requests scienceplots h5py pesummary dvc autolens
uv run python -c "import healpy, autolens; print('OK')"
```

Answer key: [pyproject.toml.answer](pyproject.toml.answer)

## If something breaks

| Issue | Fix |
|-------|-----|
| `uv: command not found` | Pre-class install script |
| scienceplots error | matplotlib pin |
| Import fails after sync | Run from repo root; use `uv run python` |

See [GRADING.md](GRADING.md) and [dvc-remote-setup.md](dvc-remote-setup.md).
