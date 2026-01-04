"""Electronic warfare subareas and burn-through calculator."""
import streamlit as st

from calculations import burn_through_range_km

st.title("Electronic Warfare Overview & Burn-Through")
st.markdown(
    r"""
    **EW subareas**
    - **Support (ES):** detect, intercept, identify, locate, and localize intentional and unintentional emissions.
    - **Attack (EA):** passive jamming (chaff/decoys), active jamming (barrier, deception, spot, barrage, swept, pulse), intrusion, probing, and electromagnetic pulse effects.
    - **Protection (EP):** frequency agility, sidelobe blanking/cancellation, ultralow sidelobes, pulse compression, PRF jitter, burn-through modes, anti-crosspol, home-on-jam, LPI measures, spectrum management, emission control, electromagnetic compatibility.

    **Support activities**
    - Electronic reconnaissance, intelligence, and security of non-communications emitters.

    **Protection measures**
    - Electromagnetic hardening (blanking, filtering, grounding, shielding), electronic masking, emission control, wartime reserve modes.
    """
)

st.latex(r"R_{BT} \approx \left( \frac{P_t G_t^2 \lambda^2 \sigma}{P_j G_j (4\pi)^2 (J/S)} \right)^{1/4}")
st.caption(r"Variables: $P_t$ radar power, $G_t$ radar gain, $P_j$ jammer power, $G_j$ jammer gain, $\sigma$ RCS, J/S desired jammer advantage.")

col1, col2 = st.columns(2)
with col1:
    tx_power_w = st.number_input(r"Radar power $P_t$ (W)", min_value=0.1, value=5000.0, key="ew_tx")
    tx_gain_dbi = st.number_input(r"Radar antenna gain $G_t$ (dBi)", value=32.0, key="ew_gt")
    freq_ghz = st.number_input(r"Radar frequency $f$ (GHz)", min_value=0.1, value=10.0, key="ew_f")
    rcs_m2 = st.number_input(r"Target RCS $\sigma$ (m²)", min_value=0.0001, value=1.0, format="%.4f", key="ew_rcs")
with col2:
    jammer_power_w = st.number_input(r"Jammer power $P_j$ (W)", min_value=0.1, value=1000.0)
    jammer_gain_dbi = st.number_input(r"Jammer antenna gain $G_j$ (dBi)", value=10.0)
    desired_js_db = st.number_input(r"Desired J/S margin (dB)", value=0.0, help="Positive values model stronger jamming; negative favors the radar.")

wavelength_m = 0.3 / freq_ghz
bt_range = burn_through_range_km(
    tx_power_w,
    tx_gain_dbi,
    jammer_power_w,
    jammer_gain_dbi,
    wavelength_m,
    rcs_m2,
    desired_js_db,
)

st.metric("Approx. burn-through range (km)", f"{bt_range:.2f}")
st.info(
    "Assumes monostatic radar, self-protection geometry, and equal mainlobe coupling. For escorts or sidelobe jamming, adjust the gains to match geometry."
)
