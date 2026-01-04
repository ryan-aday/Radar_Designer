"""Radar resolution cells, link equations, and Swerling context."""
import streamlit as st

from calculations import (
    angular_resolution_m,
    fspl_db,
    one_way_received_power_dbm,
    resolution_cell_volume_m3,
    range_resolution_m,
)

st.title("Resolution, Link Equations & Swerling")
st.write("Explore range/angular resolution, pulse volume, and one-way link power with LaTeX references from the eGuide.")

with st.expander("Resolution cell formulas"):
    st.latex(r"\Delta R = \frac{c_0\tau}{2} \qquad \Delta S_{az} \approx R\,\theta_{Az} \qquad V = \frac{R^2\,\theta_{Az}\,\theta_{El}\,c_0\,\tau}{8}")
    st.caption("Variables: $\tau$ pulse width, $R$ slant range, $\theta_{Az/El}$ beamwidths (rad). Volume target echo grows with $R^2$.")

cols = st.columns(3)
with cols[0]:
    rng_km = st.number_input("Range $R$ (km)", min_value=0.1, value=20.0)
    tau_us = st.number_input("Pulse width $\tau$ (μs)", min_value=0.01, value=5.0)
    st.metric("ΔR (m)", f"{range_resolution_m(tau_us):.2f}")
with cols[1]:
    bw_az = st.number_input("Beamwidth $\theta_{Az}$ (deg)", min_value=0.01, value=1.0)
    cross_az = angular_resolution_m(rng_km, bw_az)
    st.metric("Cross-range span (m)", f"{cross_az:.1f}")
with cols[2]:
    bw_el = st.number_input("Beamwidth $\theta_{El}$ (deg)", min_value=0.01, value=3.0)
    pulse_vol = resolution_cell_volume_m3(rng_km, bw_az, bw_el, tau_us)
    st.metric("Pulse volume V (m³)", f"{pulse_vol:.2f}")

st.divider()
st.subheader("One-way link equation (secondary / warning receivers)")
st.latex(r"P_r = P_t + G_t + G_r - \text{FSPL} - L_{tot}")
st.caption("Variables: $P_t$ TX power (dBm), $G_t/G_r$ antenna gains (dBi), FSPL from eGuide, $L_{tot}$ misc. losses.")

col4, col5 = st.columns(2)
with col4:
    tx_w = st.number_input("TX power $P_t$ (W)", min_value=0.001, value=10.0)
    tx_g = st.number_input("TX gain $G_t$ (dBi)", value=10.0)
    rx_g = st.number_input("RX gain $G_r$ (dBi)", value=5.0)
    freq = st.number_input("Frequency $f$ (GHz)", min_value=0.05, value=1.0)
with col5:
    range_l = st.number_input("Range $R$ (km)", min_value=0.1, value=15.0)
    losses = st.number_input("Losses $L_{tot}$ (dB)", min_value=0.0, value=3.0, help="Cable, mismatch, processing.")
    pr_oneway = one_way_received_power_dbm(tx_w, tx_g, rx_g, range_l, freq, losses)
    st.metric("One-way $P_r$ (dBm)", f"{pr_oneway:.2f}")
    st.metric("FSPL (dB)", f"{fspl_db(range_l, freq):.2f}")

st.divider()
st.subheader("Swerling fluctuation context")
st.markdown(
    r"""
    * **Fluctuation loss**: eGuide cites ~8.4 dB for \(P_D=0.9\) (Case I/II). Cases III/IV reduce loss; Case V (steady RCS) is ~0 dB.
    * **Use margin**: Add the loss to required SNR when sizing transmitter power or dwell hits/scan.
    * **Ambiguity**: For multiple hits, noncoherent integration adds \(10\log_{10}(N)\) dB; coherent adds \(20\log_{10}(N)\).
    """
)
