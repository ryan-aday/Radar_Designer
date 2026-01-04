# Radar Designer (Streamlit)

Multipage Streamlit app with calculators and quick-reference equations for radar and electronic warfare topics.

## Running locally
1. Install dependencies: `pip install -r requirements.txt`
2. Launch Streamlit multipage app: `streamlit run app.py`
3. Use the sidebar to navigate across pages.

## Pages
- **Electronic warfare overview**: subareas, support/protection measures, burn-through estimator.
- **Frequency bands & ISM**: ISM table, band lettering, radar allocations.
- **Antenna models & field regions**: rectangular vs. elliptical gain models and near-/far-field guidance.
- **Antenna gain & beamwidth**: rectangular gain estimator with efficiency.
- **Link budget & propagation**: two-way link, FSPL, Fresnel radius, bulge, two-ray/knife-edge notes, command-guided beams.
- **Noise & receiver performance**: sensitivity, NF/Fn, noise temperature, SINAD/ENOB, SNIR checks.
- **RCS, chaff, and decoys**: Rayleigh/Mie/optical regions, retroreflectors, chaff cloud sizing, active decoy RCS.
- **Jamming & deception**: J/S estimator plus spot/barrage/swept/pulse/RGPO/VGPO techniques.
- **Pulse & CW radar**: duty cycle, blind/unambiguous range, Doppler, FMCW resolution, hits/scan.
- **Doppler, refraction, and horizon**: radial speed, height estimation, refraction classes, ducting, radar horizon.
- **Resolution, link equations & Swerling**: resolution cells, angular spacing, one-/two-way link equations, losses, fluctuation cases, weather radar notes.
- **Antenna Pattern 3D Visualizer**: approximate 3D gain shapes for common antennas with adjustable aperture/length, array size, and front/back shaping.

## Notes
- Equations are rendered on every page.
- Calculations shared across pages live in `calculations.py` to keep logic in one place.
