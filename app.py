"""Streamlit Radar Designer multipage app with LaTeX equations."""

import streamlit as st

st.set_page_config(page_title="Radar Designer", layout="wide")

st.title("Radar Designer eGuide")
st.write(
    """Interactive, multipage reference inspired by the radar and electronic warfare eGuide.
    Use the sidebar to jump between design inputs, EW considerations, propagation, antenna
    performance, and radar modes. Each page keeps LaTeX equations visible alongside the calculators."""
)

with st.expander("Key equations at a glance"):
    st.latex(r"\textbf{FSPL (dB)} = 32.45 + 20\log_{10}(R_{\text{km}}) + 20\log_{10}(f_{\text{MHz}})")
    st.latex(r"\textbf{Two-way radar: } P_r = P_t G_t G_r \left( \frac{\lambda}{4\pi R} \right)^4 \sigma / L_{\text{tot}}")
    st.latex(r"\textbf{Burn-through (self-protect): } R_{BT} \propto \left( \frac{P_t G_t^2 \lambda^2 \sigma}{P_j G_j (4\pi)^2 J/S} \right)^{1/4}")
    st.latex(r"\textbf{Range resolution (unmod): } \Delta R = \frac{c_0 \tau}{2} \qquad \textbf{Chirp: } \Delta R = \frac{c_0}{2\,BW}")
    st.latex(r"\textbf{Antenna gain: } G \approx \eta \frac{4\pi}{\Omega_A} \approx \eta \frac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}")

st.info(
    "Paste figure JPGs from the source eGuide into the placeholder expanders on each page to complete the visual references."
)

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
    - **Design inputs & link budget** for received power/SNR trades.
    - **Electronic warfare** for burn-through exploration.
    - **Propagation** for Fresnel clearance and FSPL checks.
    - **Antenna** for gain vs. beamwidth.
    - **Radar modes** for timing, resolution, and velocity ambiguity.
    """
)
