"""Streamlit Radar Designer multipage app."""

import streamlit as st

st.set_page_config(page_title="Radar Designer", layout="wide")

st.title("Radar Designer")
st.write(
    """Interactive, multipage reference for radar and electronic warfare topics.
    Use the sidebar to jump between design inputs, propagation, antenna performance, timing,
    and EW effects. Each page keeps the governing equations visible alongside calculators."""
)

with st.expander("Key equations at a glance"):
    st.latex(r"\textbf{FSPL (dB)} = 32.45 + 20\log_{10}(R_{\text{km}}) + 20\log_{10}(f_{\text{MHz}})")
    st.latex(r"\textbf{Two-way radar: } P_r = P_t G_t G_r \left( \frac{\lambda}{4\pi R} \right)^4 \sigma / L_{\text{tot}}")
    st.latex(r"\textbf{Burn-through (self-protect): } R_{BT} \propto \left( \frac{P_t G_t^2 \lambda^2 \sigma}{P_j G_j (4\pi)^2 J/S} \right)^{1/4}")
    st.latex(r"\textbf{Range resolution (unmod): } \Delta R = \frac{c_0 \tau}{2} \qquad \textbf{Chirp: } \Delta R = \frac{c_0}{2\,BW}")
    st.latex(r"\textbf{Antenna gain: } G \approx \eta \frac{4\pi}{\Omega_A} \approx \eta \frac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}")
    st.latex(r"\textbf{Radar horizon: } R_{LOS} \approx 4.12(\sqrt{h_{ant}} + \sqrt{h_{tgt}}) \text{ km}")
    st.latex(r"\textbf{Duty cycle: } \text{DC} = \frac{\tau}{\text{PRI}} \qquad \textbf{EIRP: } P_{EIRP} = P_t G_t")

with st.expander("Suggested figure drop-in points"):
    st.markdown(
        """
        - Frequency bands and radar frequencies tables
        - Antenna pattern examples (pencil, fan, cosecant-squared, omni)
        - Propagation attenuation curves (atmospheric and rain)
        - Pulse timing diagrams and chirp modulation sketches
        - Radar cross section tables and resonance region plots
        """
    )

st.markdown(
    """The sidebar lists all available calculators:
    - **Electronic warfare** for subareas, protection measures, and burn-through.
    - **Frequency bands** for ISM allocations and radar-centric bands.
    - **Antenna models & field regions** for rectangular vs. elliptical solid angles and near/far boundaries.
    - **Antenna patterns & gain** for beamwidth, efficiency, and pattern notes including command-guided beams.
    - **Link budget & propagation** for FSPL, Fresnel clearance, bulge, and two-ray/knife-edge notes.
    - **Noise & receiver performance** for Fn/NF, noise temperature, SINAD, ENOB, and SNIR.
    - **RCS, chaff, and decoys** for Rayleigh/optical regimes, retroreflectors, and expendables.
    - **Jamming & deception** for support-jamming J/S and ECM technique notes.
    - **Pulse & CW radar** for blind range, unambiguous range, duty cycle, and FMCW resolution.
    - **Doppler, refraction, and horizon** for radial speed, height estimates, ducting, and radar LOS.
    - **Resolution, link equations & Swerling** for resolution cells, one/two-way links, losses, and fluctuation models.
    - **Antenna Pattern 3D Visualizer** for interactive pattern shapes across common antenna archetypes.
    """
)
