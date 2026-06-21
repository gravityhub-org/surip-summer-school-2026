# DVC pipeline notes (instructor)

Students use **pipeline stages only** — no manual `dvc add` on data folders.

Fetch scripts live in `load_script/`:

```bash
uv run python load_script/generate_skymaps.py
uv run python load_script/load_pe.py
```

Reference pipeline: [dvc.yaml.answer](dvc.yaml.answer)

Grading: [GRADING.md](GRADING.md)

---

## Gitignored vs committed

| Local-only (gitignored) | In student clone |
|-------------------------|------------------|
| `pyproject.toml`, `uv.lock`, `.venv/` | scripts, `SETUP.md`, `workshop/` answer keys |
| `data/*` (from fetch stages), `output/` | empty `data/` / `output/` dirs |
| `.dvc/cache/` | — |

`dvc.yaml`, `dvc.lock`, and `.dvc/config` are **not** gitignored — DVC refuses ignored pipeline files. Omit them from commits if students write their own pipeline.

## Maintainer dry-run

```bash
cp workshop/pyproject.toml.answer pyproject.toml
uv sync --extra dev
dvc init   # if fresh clone
cp workshop/dvc.yaml.answer dvc.yaml
dvc repro
uv run pytest -m "not slow"
```

Optional shared remote (not required for in-room grading): see legacy notes below.

```bash
# Optional — if using a shared remote for pre-staged data
dvc remote add -d origin /path/to/storage
dvc push -r origin
```

Clean-clone test:

```bash
cd /tmp && git clone YOUR_REPO surip-test && cd surip-test
cp workshop/pyproject.toml.answer pyproject.toml
uv sync
cp workshop/dvc.yaml.answer dvc.yaml
dvc repro
ls output/
```
