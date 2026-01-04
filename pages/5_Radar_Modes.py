"""Radar timing, resolution, and Doppler checks."""
import streamlit as st

from calculations import (
    bandwidth_resolution_m,
    dwell_time_ms,
    range_resolution_m,
    unambiguous_velocity_ms,
)

st.title("Radar Modes, Timing & Resolution")
st.write("Compare unmodulated and chirp resolution, Doppler limits, and dwell time.")
st.latex(r"\Delta R_{\text{unmod}} = \frac{c_0\,\tau}{2} \qquad \Delta R_{\text{chirp}} = \frac{c_0}{2\,BW}")
st.latex(r"v_{\text{unamb}} = \frac{\lambda \cdot PRF}{4} \qquad T_D \approx \frac{60}{\text{RPM}} \cdot \frac{\theta}{360}")

col1, col2, col3 = st.columns(3)
with col1:
    pw_us = st.number_input("Pulse width (µs)", min_value=0.01, value=1.0)
    prf_hz = st.number_input("PRF (Hz)", min_value=1.0, value=1000.0)
with col2:
    bandwidth_mhz = st.number_input("Transmit bandwidth (MHz)", min_value=0.001, value=5.0, key="mode_bw")
    freq_ghz = st.number_input("Carrier (GHz)", min_value=0.1, value=10.0, key="mode_f")
with col3:
    beamwidth_deg = st.number_input("Beamwidth for dwell (°)", min_value=0.1, value=2.0)
    rpm = st.number_input("Antenna rotation (RPM)", min_value=0.1, value=12.0)

rng_res_unmod = range_resolution_m(pw_us)
rng_res_chirp = bandwidth_resolution_m(bandwidth_mhz)
v_unamb = unambiguous_velocity_ms(freq_ghz, prf_hz)
dwell = dwell_time_ms(beamwidth_deg, rpm)

st.metric("Unmodulated range resolution (m)", f"{rng_res_unmod:.2f}")
st.metric("Chirp range resolution (m)", f"{rng_res_chirp:.2f}")
st.metric("Max unambiguous radial velocity (m/s)", f"{v_unamb:.2f}")
st.metric("Dwell time per beam (ms)", f"{dwell:.2f}")
st.caption("Dwell ≈ 6·PRT/beam for MTI; use staggered PRFs to balance range/velocity ambiguities.")
