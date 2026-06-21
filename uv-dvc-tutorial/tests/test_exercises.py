"""Tests for SURIP 2026 workshop exercises."""

import importlib
import subprocess
import sys
from pathlib import Path

import healpy as hp
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SETUP = (ROOT / "SETUP.md").read_text()


def _write_mock_skymaps(directory):
    directory.mkdir(parents=True, exist_ok=True)
    nside = 64
    specs = [
        ("GW150914_skymap.fits", 1.2, 2.0, 0.25),
        ("GW170817_skymap.fits", 1.8, 4.5, 0.20),
        ("GW170814_skymap.fits", 0.9, 5.2, 0.15),
    ]
    npix = hp.nside2npix(nside)
    theta_all, phi_all = hp.pix2ang(nside, np.arange(npix))
    for fname, t0, p0, sigma in specs:
        d2 = (theta_all - t0) ** 2 + (phi_all - p0) ** 2
        m = np.exp(-0.5 * d2 / sigma**2)
        m /= m.sum()
        hp.write_map(directory / fname, m, overwrite=True)


def _run_exercise(script_name, capture=False):
    kwargs = {"cwd": ROOT}
    if capture:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    return subprocess.run(
        [sys.executable, str(ROOT / "exercises" / script_name)],
        **kwargs,
    )


def _make_gaussian_skymap(nside=64, theta0=1.2, phi0=2.0, sigma=0.25):
    npix = hp.nside2npix(nside)
    theta_all, phi_all = hp.pix2ang(nside, np.arange(npix))
    d2 = (theta_all - theta0) ** 2 + (phi_all - phi0) ** 2
    prob = np.exp(-0.5 * d2 / sigma**2)
    prob = np.maximum(prob, 0)
    prob /= prob.sum()
    return prob


def _level_map_from_prob(prob):
    sorted_idx = np.argsort(prob)[::-1]
    cumsum = np.cumsum(prob[sorted_idx])
    level_map = np.zeros_like(prob)
    level_map[sorted_idx] = cumsum
    return level_map, sorted_idx, cumsum


def _credible_mask(prob, level):
    prob = np.asarray(prob, dtype=float)
    prob = np.maximum(prob, 0)
    prob /= prob.sum()
    sorted_idx = np.argsort(prob)[::-1]
    cumsum = np.cumsum(prob[sorted_idx])
    cut = np.searchsorted(cumsum, level)
    mask = np.zeros_like(prob, dtype=bool)
    mask[sorted_idx[: cut + 1]] = True
    return mask


def test_step1_imports():
    for mod in ("numpy", "scipy", "astropy", "matplotlib", "healpy", "colossus", "lenstronomy", "scienceplots"):
        importlib.import_module(mod)


def test_setup_lists_core_packages():
    for pkg in ("numpy", "scipy", "astropy", "matplotlib", "healpy", "colossus", "lenstronomy", "scienceplots", "dvc", "autolens"):
        assert pkg in SETUP


def test_level_map_assigns_cumulative_probability():
    prob = np.array([0.5, 0.3, 0.15, 0.05])
    level_map, sorted_idx, cumsum = _level_map_from_prob(prob)
    assert level_map[sorted_idx[0]] == pytest.approx(0.5)
    assert level_map[sorted_idx[1]] == pytest.approx(0.8)
    assert level_map[sorted_idx[-1]] == pytest.approx(1.0)
    assert np.all(level_map >= 0)
    assert np.all(level_map <= 1)


def test_credible_mask_68_and_95_enclose_expected_probability():
    prob = _make_gaussian_skymap()
    for level in (0.68, 0.95):
        mask = _credible_mask(prob, level)
        enclosed = prob[mask].sum()
        assert enclosed >= level
        assert enclosed < level + prob.max()


def test_level_map_smoothing_produces_finite_grid():
    prob = _make_gaussian_skymap()
    level_map, _, _ = _level_map_from_prob(prob)
    smoothed = hp.smoothing(level_map, fwhm=np.radians(1.0))
    assert np.all(np.isfinite(smoothed))
    assert np.nanmin(smoothed) >= 0
    assert np.nanmax(smoothed) <= 1.05


def test_mollweide_projection_grid_shape():
    prob = _make_gaussian_skymap()
    level_map, _, _ = _level_map_from_prob(prob)
    smoothed = hp.smoothing(level_map, fwhm=np.radians(1.0))
    nside = hp.get_nside(prob)
    npts = 800
    proj = hp.projector.MollweideProj(xsize=npts)
    grid = proj.projmap(smoothed, lambda x, y, z: hp.vec2pix(nside, x, y, z))
    assert grid.shape == (npts // 2, npts)


def test_ex02_missing_data_hint(monkeypatch):
    monkeypatch.chdir(ROOT)
    empty = ROOT / "data" / "skymaps"
    if empty.exists():
        for f in empty.glob("*.fits*"):
            f.unlink()
    result = _run_exercise("ex02_skymaps.py", capture=True)
    assert result.returncode != 0
    assert "dvc repro" in result.stdout.lower() or "fetch_skymaps" in result.stdout.lower()


def test_ex02_skymap_plots(monkeypatch):
    monkeypatch.chdir(ROOT)
    skymap_dir = ROOT / "data" / "skymaps"
    skymap_dir.mkdir(parents=True, exist_ok=True)
    _write_mock_skymaps(skymap_dir)
    out = ROOT / "output"
    for old in out.glob("ex02_*"):
        old.unlink()
    result = _run_exercise("ex02_skymaps.py", capture=True)
    assert result.returncode == 0
    assert "done!" in result.stdout.lower()
    assert (out / "ex02_GW150914.png").is_file()
    assert (out / "ex02_overlay.png").is_file()
    assert (out / "ex02_GW150914.png").stat().st_size > 10_000
    assert (out / "ex02_overlay.png").stat().st_size > 10_000


def test_ex01_halo_ps_plots(monkeypatch):
    monkeypatch.chdir(ROOT)
    out = ROOT / "output"
    result = _run_exercise("ex01_halo_ps.py")
    assert result.returncode == 0
    assert (out / "ex01_halo_mass_function.png").is_file()
    assert (out / "ex01_power_spectrum.png").is_file()


@pytest.mark.slow
def test_ex03_euclid_mock(monkeypatch):
    monkeypatch.chdir(ROOT)
    out = ROOT / "output"
    result = _run_exercise("ex03_euclid_mock.py")
    assert result.returncode == 0
    assert (out / "euclid_lens_image.png").is_file()
