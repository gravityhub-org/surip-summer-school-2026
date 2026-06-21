# Euclid VIS Lens Simulation Spec

This file holds the numbers used to simulate one strong-lens image as it
would look in an Euclid VIS exposure. The simulation script reads the
YAML block below directly.

## Notes

- Euclid VIS pixel scale and PSF FWHM are taken from the official Euclid
  instrument description (broad single optical band, ~0.1" pixels,
  diffraction-limited PSF FWHM ~0.16-0.18").
- Lens is a singular isothermal ellipsoid (SIE) plus external shear.
- Source is a single elliptical Sersic profile.

```yaml
telescope:
  name: "Euclid_VIS"
  pixel_scale: 0.1          # arcsec / pixel
  image_pixels: 100         # image is image_pixels x image_pixels
  psf_fwhm: 0.17            # arcsec
  exposure_time: 2260       # seconds (single Euclid VIS exposure)
  background_sky_level: 0.2 # counts / pixel / sec, rough VIS sky level

lens_galaxy:
  redshift: 0.5
  mass_profile: "SIE"        # singular isothermal ellipsoid
  einstein_radius: 1.2       # arcsec
  ell_comps: [0.1, 0.05]     # (ell_comps_y, ell_comps_x) = (1-q)/(1+q) * (sin(2*angle), cos(2*angle))
  centre: [0.0, 0.0]
  shear:
    gamma_1: 0.02
    gamma_2: 0.01
  light_profile: "Sersic"
  light_intensity: 0.3
  light_effective_radius: 0.8  # arcsec
  light_sersic_index: 3.0

source_galaxy:
  redshift: 1.0
  light_profile: "Sersic"
  intensity: 1.2
  effective_radius: 0.3      # arcsec
  sersic_index: 1.5
  ell_comps: [-0.05, 0.15]   # (ell_comps_y, ell_comps_x), same convention as lens
  centre: [0.05, 0.05]       # arcsec, offset from lens centre
```