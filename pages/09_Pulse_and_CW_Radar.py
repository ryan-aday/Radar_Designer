"""Pulse and CW radar timing, duty cycle, and Doppler calculators."""
import streamlit as st

from calculations import (
    bandwidth_resolution_m,
    blind_range_m,
    doppler_frequency_hz,
    duty_cycle,
    range_resolution_m,
    unambiguous_range_km,
    unambiguous_velocity_ms,
)

st.title("Pulse & CW Radar")
st.write(
    "Capture pulse timing, duty cycle, blind range, unambiguous range/velocity, and FMCW range resolution references."
)

with st.expander("Pulse radar equations"):
    st.latex(r"\textbf{Duty cycle: } DC = \frac{\tau}{PRI} \qquad \textbf{Blind range: } R_{min} = \frac{c_0(\tau + t_{dead} + t_{rec})}{2}")
    st.latex(r"\textbf{Unambiguous range: } R_{ua} = \frac{c_0(PRI-\tau)}{2} \qquad \textbf{Hits/scan: } H = \frac{6\,PRI}{\theta_{Az} n}")
    st.latex(r"\textbf{Range resolution (unmod): } \Delta R = \frac{c_0\tau}{2} \qquad \textbf{Chirp/FMCW: } \Delta R = \frac{c_0}{2\,BW}")
    st.latex(r"\textbf{Chirp slope: } k = \frac{BW}{T_{chirp}} \qquad \textbf{FMCW beat: } R = \frac{c_0 f_b}{2k}")
    st.markdown("Radar blind range falls inside the transmit/guard time; staggered PRFs mitigate ambiguous ranges.")

col1, col2, col3 = st.columns(3)
with col1:
    pri_us = st.number_input(r"PRI (μs)", min_value=0.1, value=1000.0, help="Pulse repetition interval.")
    tau_us = st.number_input(r"Pulse width $\tau$ (μs)", min_value=0.01, value=10.0)
    dc = duty_cycle(pri_us, tau_us)
    st.metric("Duty cycle", f"{dc:.4f}")
    blind_m = blind_range_m(tau_us, st.number_input(r"Dead time $t_{dead}$ (μs)", min_value=0.0, value=5.0), st.number_input(r"Recovery $t_{rec}$ (μs)", min_value=0.0, value=5.0, key="rec"))
    st.metric("Blind range (m)", f"{blind_m:.1f}")

with col2:
    rua_km = unambiguous_range_km(pri_us, tau_us)
    st.metric("Unambiguous range (km)", f"{rua_km:.2f}")
    unmod_res = range_resolution_m(tau_us)
    bw_mhz = st.number_input(r"Chirp/FMCW bandwidth $BW$ (MHz)", min_value=0.1, value=150.0)
    fm_res = bandwidth_resolution_m(bw_mhz)
    st.metric("Unmod. ΔR (m)", f"{unmod_res:.2f}")
    st.metric("Chirp/FMCW ΔR (m)", f"{fm_res:.2f}")

with col3:
    freq_ghz = st.number_input(r"Carrier $f$ (GHz)", min_value=0.1, value=10.0)
    prf_hz = 1 / (pri_us * 1e-6)
    v_ua = unambiguous_velocity_ms(freq_ghz, prf_hz)
    st.latex(r"v_{ua} = \frac{\lambda\,PRF}{4}")
    st.metric("Unambiguous velocity (m/s)", f"{v_ua:.2f}")
    radial_v = st.number_input(r"Radial speed $v_r$ (m/s)", value=100.0)
    doppler = doppler_frequency_hz(freq_ghz, radial_v)
    st.latex(r"f_D = \frac{2 v_r}{\lambda}")
    st.metric("Doppler shift (Hz)", f"{doppler:.1f}")

with st.expander("CW radar notes, codes, and sidelobes"):
    st.markdown(
        r"""
- **Unmodulated CW**: measures Doppler only; range ambiguous beyond a wavelength.
- **FMCW / FMiCW**: sawtooth or interrupted FM enables range via $\Delta f$; range resolution set by swept bandwidth.
- **Chirp radar**: long intrapulse FM or PM is compressed; compression ratio $PCR \approx \tfrac{BW}{1/\tau}$, keeping energy but narrowing effective $\tau$.
- **Barker codes**: BPSK with sidelobes $|x_i|\le1$; useful lengths $n\in\{2,3,4,5,7,11,13\}$, nestable (e.g., $B_5\otimes B_{13}$).
- **Sidelobe metrics**: $PSL=10\log_{10}(x_i^2/x_0^2)$, $ISL=10\log_{10}(\sum x_i^2/x_0^2)$; taper and phase coding reduce PSL.
- **Doppler dilemma**: high PRF for velocity vs. low PRF for range; staggered PRFs or burst modes help.
- **Jet engine modulation (JEM)**: blade flashes appear as Doppler lines on cavity returns.
        """
    )

st.info("Adjust PRI/PRF to balance range ambiguity and Doppler coverage; guard intervals set the blind range floor.")
