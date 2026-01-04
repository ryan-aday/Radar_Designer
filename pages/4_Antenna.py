"""Antenna gain vs. beamwidth estimator."""
import textwrap
import streamlit as st

from calculations import beamwidth_gain_dbi

st.title("Antenna Gain & Beamwidth")
st.write("Estimate antenna gain from -3 dB beamwidths and efficiency.")
st.latex(r"G \approx \eta \frac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}\ \text{(degrees)}")
st.caption("Variables: $\eta$ efficiency, $\theta_{az},\theta_{el}$ half-power beamwidths in degrees. Two-way beamwidth limits detection overlap.")

col1, col2 = st.columns(2)
with col1:
    h_bw = st.number_input("Horizontal beamwidth $\theta_{az}$ (°)", min_value=0.1, value=3.0)
    v_bw = st.number_input("Vertical beamwidth $\theta_{el}$ (°)", min_value=0.1, value=3.0)
with col2:
    efficiency = st.slider("Antenna efficiency $\eta$", min_value=0.2, max_value=0.8, value=0.55, step=0.01)

gain = beamwidth_gain_dbi(h_bw, v_bw, efficiency)

st.metric("Estimated gain (dBi)", f"{gain:.2f}")
st.write(
    textwrap.dedent(
        """
        Notes:
        - Uses rectangular model (41253 / (θaz · θel)) scaled by efficiency, as in the eGuide.
        - Tight beams raise gain; lowering efficiency reflects taper or aperture blockage.
        - Swap beamwidths to explore pencil, fan, or cosecant-squared shaping.
        """
    )
)
