"""Exercise 3: Euclid VIS-like strong-lens mock (PyAutoLens)."""

import re
from pathlib import Path

import autolens as al
import autolens.plot as aplt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
SPEC = ROOT / "data" / "euclid" / "euclid_lens_spec.md"

OUTPUT.mkdir(exist_ok=True)

spec_text = SPEC.read_text()
yaml_block = re.search(r"```yaml\n(.*?)```", spec_text, re.S).group(1)
spec = yaml.safe_load(yaml_block)

telescope = spec["telescope"]
lens_spec = spec["lens_galaxy"]
source_spec = spec["source_galaxy"]

grid = al.Grid2D.uniform(
    shape_native=(telescope["image_pixels"], telescope["image_pixels"]),
    pixel_scales=telescope["pixel_scale"],
)

psf_size = 21
sigma_pix = (telescope["psf_fwhm"] / 2.355) / telescope["pixel_scale"]
yv, xv = np.mgrid[0:psf_size, 0:psf_size] - psf_size // 2
kernel = np.exp(-(xv**2 + yv**2) / (2 * sigma_pix**2))
kernel = kernel / kernel.sum()

psf_array = al.Array2D.no_mask(
    values=kernel, pixel_scales=telescope["pixel_scale"]
)
convolver = al.Convolver(kernel=psf_array)

mass = al.mp.Isothermal(
    centre=tuple(lens_spec["centre"]),
    ell_comps=tuple(lens_spec["ell_comps"]),
    einstein_radius=lens_spec["einstein_radius"],
)

shear = al.mp.ExternalShear(
    gamma_1=lens_spec["shear"]["gamma_1"],
    gamma_2=lens_spec["shear"]["gamma_2"],
)

lens_light = al.lp.Sersic(
    centre=tuple(lens_spec["centre"]),
    intensity=lens_spec["light_intensity"],
    effective_radius=lens_spec["light_effective_radius"],
    sersic_index=lens_spec["light_sersic_index"],
)

lens_galaxy = al.Galaxy(
    redshift=lens_spec["redshift"],
    mass=mass,
    shear=shear,
    light=lens_light,
)

source_light = al.lp.Sersic(
    centre=tuple(source_spec["centre"]),
    intensity=source_spec["intensity"],
    effective_radius=source_spec["effective_radius"],
    sersic_index=source_spec["sersic_index"],
    ell_comps=tuple(source_spec["ell_comps"]),
)

source_galaxy = al.Galaxy(
    redshift=source_spec["redshift"],
    light=source_light,
)

tracer = al.Tracer(galaxies=[lens_galaxy, source_galaxy])

simulator = al.SimulatorImaging(
    exposure_time=telescope["exposure_time"],
    background_sky_level=telescope["background_sky_level"],
    psf=convolver,
    add_poisson_noise_to_data=True,
)

imaging = simulator.via_tracer_from(tracer=tracer, grid=grid)

al.output_to_fits(
    values=imaging.data.native,
    file_path=str(OUTPUT / "euclid_lens_image.fits"),
    overwrite=True,
)
al.output_to_fits(
    values=kernel,
    file_path=str(OUTPUT / "euclid_lens_psf.fits"),
    overwrite=True,
)
al.output_to_fits(
    values=imaging.noise_map.native,
    file_path=str(OUTPUT / "euclid_lens_noise_map.fits"),
    overwrite=True,
)

aplt.subplot_imaging_dataset(
    dataset=imaging,
    output_path=str(OUTPUT),
    output_filename="euclid_lens_dataset",
    output_format="png",
)

aplt.subplot_tracer(
    tracer=tracer,
    grid=grid,
    output_path=str(OUTPUT),
    output_format="png",
)

aplt.plot_array(
    array=imaging.data,
    title="Simulated Euclid VIS lens image",
    output_path=str(OUTPUT),
    output_filename="euclid_lens_image",
    output_format="png",
)

print("Saved euclid_lens outputs in output/")
