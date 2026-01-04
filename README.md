# Radar Designer eGuide

Interactive Streamlit app that mirrors the radar and electronic warfare eGuide content with inline calculators for quick trade studies.

## Running locally

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```
3. Use the sidebar to navigate between overview, design inputs, EW, propagation, antenna, and radar mode calculators. Paste JPEG figures from the eGuide into the highlighted expandable sections to complete the visuals.

## Included calculators
- Two-way radar equation with received power, noise floor, and SNR margin
- Free-space path loss checker
- Burn-through range estimator for jammer conflicts
- Fresnel clearance and Earth bulge aids with atmospheric loss roll-up
- Antenna gain vs. beamwidth estimator
- Range resolution, unambiguous velocity, and dwell time tools for pulse or chirp modes
