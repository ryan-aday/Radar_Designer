"""Weather radar specifics, propagation, and horizon tools."""
import math
import streamlit as st

from calculations import fspl_db, height_from_range_el_m, radar_horizon_km

st.title("Weather Radar, Propagation & Horizon")

st.markdown(
    r"""
    **Weather radar equation:**
    \[
    P_r \propto \frac{P_t G^2 \lambda^2 |K|^2 V}{(4\pi)^3 R^2 L_{tot}}
    \]
    Volume targets grow with range because pulse volume \(V \propto R^2\), leaving only a quadratic loss vs. range (not \(R^4\) as for point targets). Refraction term \(K\) depends on droplet composition and wavelength.

    **Atmospheric attenuation:** include rain + gaseous loss per km when above 10 GHz; oxygen and water-vapor lines create peaks.
    """
)

col1, col2 = st.columns(2)
with col1:
    tx_power_w = st.number_input("Transmit power $P_t$ (W)", min_value=0.1, value=1000.0, help="Weather radar peak power.")
    gain_dbi = st.number_input("Antenna gain $G$ (dBi)", value=35.0, help="Parabolic dish gain.")
    wavelength_m = st.number_input("Wavelength $\lambda$ (m)", min_value=0.001, value=0.03, help="Carrier wavelength.")
    range_km = st.number_input("Range $R$ (km)", min_value=0.1, value=50.0, help="Target range.")
with col2:
    rain_att_db_km = st.number_input("Rain/gas attenuation (dB/km)", min_value=0.0, value=0.12, help="Rain + gaseous loss per km.")
    misc_loss_db = st.number_input("Other losses $L_{tot}$ (dB)", min_value=0.0, value=5.0, help="Waveguide, radome, processing.")
    reflectivity_factor = st.number_input("Reflectivity factor Z (mm^6/m^3)", min_value=0.1, value=1000.0, help="Storm cells can exceed 10^4.")

# Simple proportional power score (dB) ignoring calibration constants
power_score_db = (
    10 * math.log10(tx_power_w * 1000)
    + 2 * gain_dbi
    + 20 * math.log10(wavelength_m)
    + 10 * math.log10(reflectivity_factor)
    - 20 * math.log10(range_km * 1000)
    - (rain_att_db_km * range_km + misc_loss_db)
)

st.metric("Relative weather return (dB score)", f"{power_score_db:.1f}")
st.caption("Higher Z, shorter range, and higher gain boost returns; rain loss and gas lines reduce them.")

st.divider()

st.subheader("Radar horizon, refraction, and ducting")
col3, col4 = st.columns(2)
with col3:
    h_ant = st.number_input("Antenna height $h_{ant}$ (m)", min_value=0.0, value=20.0)
    h_tgt = st.number_input("Target height $h_{tgt}$ (m)", min_value=0.0, value=5.0)
    elev_deg = st.number_input("Elevation angle $e$ (deg)", min_value=-5.0, value=1.0)
    horizon_km = radar_horizon_km(h_ant, h_tgt)
    est_height_m = height_from_range_el_m(range_km, elev_deg)
with col4:
    fspl_example = fspl_db(range_km, 0.3 / wavelength_m)
    st.metric("Two-way horizon LOS (km)", f"{horizon_km:.2f}")
    st.metric("FSPL at current range (dB)", f"{fspl_example:.2f}")
    st.metric("Estimated target height (m)", f"{est_height_m:.1f}")

st.markdown(
    r"""
    Horizon range uses \(R_{LOS} \approx 4.12(\sqrt{h_{ant}} + \sqrt{h_{tgt}})\) with heights in meters.
    Height estimate uses \(H \approx R\sin e + \dfrac{R^2}{2r_{equiv}}\) with \(r_{equiv}\approx 8500\,\text{km}\) for standard refraction.
    Ducting (surface, evaporation, or elevated) can trap waves beyond line of sight.
    Refraction classes: normal (standard N gradient), sub-refraction (positive gradient), super-refraction/ducting (negative gradient).
    """
)

with st.expander("Paste weather figures"):
    st.write("Rain attenuation curves, refractivity gradient sketches, and ducting diagrams fit here.")
