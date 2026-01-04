"""Design inputs & link budget calculator."""
import math
import streamlit as st

from calculations import fspl_db, noise_floor_dbm, radar_received_power_dbm

st.title("Design Inputs & Link Budget")
st.markdown(r"Estimate received power and SNR with the two-way radar equation:")
st.latex(r"P_r = P_t G_t G_r \left( \frac{\lambda}{4\pi R} \right)^4 \sigma / L_{\text{tot}}")

cols = st.columns(2)
with cols[0]:
    tx_power_w = st.number_input("Transmitter power (W)", min_value=0.1, value=1000.0)
    tx_gain_dbi = st.number_input("TX antenna gain (dBi)", value=30.0)
    rx_gain_dbi = st.number_input("RX antenna gain (dBi)", value=30.0)
    freq_ghz = st.number_input("Carrier frequency (GHz)", min_value=0.1, value=10.0)
    rcs_m2 = st.number_input("Target RCS (m²)", min_value=0.0001, value=1.0, format="%.4f")
    range_km = st.number_input("Target range (km)", min_value=0.1, value=50.0)
with cols[1]:
    losses_db = st.number_input("System & propagation losses (dB)", value=10.0)
    bandwidth_mhz = st.number_input("Receiver noise bandwidth (MHz)", min_value=0.001, value=5.0)
    noise_figure_db = st.number_input("Noise figure (dB)", min_value=0.0, value=3.0)
    required_snr_db = st.number_input("Required SNR for detection (dB)", value=13.0)

wavelength_m = 0.3 / freq_ghz
pr_dbm = radar_received_power_dbm(
    tx_power_w,
    tx_gain_dbi,
    rx_gain_dbi,
    wavelength_m,
    rcs_m2,
    range_km,
    losses_db,
)
nf_dbm = noise_floor_dbm(bandwidth_mhz * 1e6, noise_figure_db)
snr_db = pr_dbm - nf_dbm

st.subheader("Results")
st.metric("Received power (dBm)", f"{pr_dbm:.2f}")
st.metric("Noise floor (dBm)", f"{nf_dbm:.2f}")
st.metric("SNR (dB)", f"{snr_db:.2f}")
if not math.isnan(snr_db):
    margin = snr_db - required_snr_db
    if margin >= 0:
        st.success(f"Link budget meets requirement with {margin:.1f} dB margin.")
    else:
        st.error(f"Short by {abs(margin):.1f} dB — increase power, gain, or reduce losses.")

st.divider()
st.subheader("FSPL quick check")
fspl_value = fspl_db(range_km, freq_ghz)
st.write(f"Free-space path loss at {range_km:.1f} km: **{fspl_value:.2f} dB**")
st.latex(r"\text{FSPL (dB)} = 32.45 + 20\log_{10}(R_{\text{km}}) + 20\log_{10}(f_{\text{MHz}})")
