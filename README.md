# Radar Designer (Streamlit)

Multipage Streamlit app that packages key radar and EW calculators with inline LaTeX so the governing equations stay visible while you tweak inputs.

## Running locally
1. Install dependencies: `pip install -r requirements.txt`
2. Launch Streamlit multipage app: `streamlit run app.py`
3. Use the sidebar to navigate across pages; drop JPGs from the source eGuide into the provided expanders for visuals.

## Pages
- **Home**: overview plus quick-reference LaTeX equations.
- **Design Inputs & Link Budget**: received power, SNR, and FSPL checks.
- **Electronic Warfare & Burn-Through**: approximate burn-through range against a jammer.
- **Propagation & Clearance**: Fresnel radius, Earth bulge, FSPL, and path-loss budgeting.
- **Antenna Gain & Beamwidth**: estimate gain from -3 dB beamwidths and efficiency.
- **Radar Modes, Timing & Resolution**: compare unmodulated vs. chirp resolution, unambiguous velocity, and dwell time.

## Notes
- Equations are rendered with LaTeX on every page per requirements.
- Calculations shared across pages live in `calculations.py` to keep logic in one place.
