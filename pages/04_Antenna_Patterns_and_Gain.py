"""Antenna gain vs. beamwidth estimator."""
import textwrap
import streamlit as st

from calculations import beamwidth_gain_dbi

st.title("Antenna Gain & Beamwidth")
st.write("Estimate antenna gain from -3 dB beamwidths and efficiency.")
st.latex(r"G \approx \eta \frac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}\ \text{(degrees)}")
st.caption(r"Variables: $\eta$ efficiency, $\theta_{az},\theta_{el}$ half-power beamwidths in degrees. Two-way beamwidth limits detection overlap.")

col1, col2 = st.columns(2)
with col1:
    h_bw = st.number_input(r"Horizontal beamwidth $\theta_{az}$ (°)", min_value=0.1, value=3.0)
    v_bw = st.number_input(r"Vertical beamwidth $\theta_{el}$ (°)", min_value=0.1, value=3.0)
with col2:
    efficiency = st.slider(r"Antenna efficiency $\eta$", min_value=0.2, max_value=0.8, value=0.55, step=0.01)

gain = beamwidth_gain_dbi(h_bw, v_bw, efficiency)

st.metric("Estimated gain (dBi)", f"{gain:.2f}")
st.write(
    textwrap.dedent(
        """
        Notes:
        - Rectangular model gain scales with efficiency; narrow beams and higher \(\eta\) raise EIRP.
        - Beam solid angle \(\Omega_A\) shrinks with tighter beamwidths; \(D \approx 4\pi/\Omega_A\).
        - Beamwidth factor and taper drive sidelobe level; adjust \(\eta\) downward to reflect illumination taper or blockage.
        """
    )
)
