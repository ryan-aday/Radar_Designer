import math
import textwrap

import streamlit as st


def fspl_db(distance_km: float, freq_ghz: float) -> float:
    """Free-space path loss in dB."""
    if distance_km <= 0 or freq_ghz <= 0:
        return float("nan")
    # 32.45 term uses km and MHz; convert GHz to MHz.
    return 32.45 + 20 * math.log10(distance_km) + 20 * math.log10(freq_ghz * 1000)


def radar_received_power_dbm(
    tx_power_w: float,
    tx_gain_dbi: float,
    rx_gain_dbi: float,
    wavelength_m: float,
    rcs_m2: float,
    range_km: float,
    system_losses_db: float,
) -> float:
    """Monostatic radar equation (two-way) in dBm."""
    if tx_power_w <= 0 or wavelength_m <= 0 or range_km <= 0 or rcs_m2 <= 0:
        return float("nan")
    range_m = range_km * 1000
    geometric_term_db = 20 * math.log10(wavelength_m / (4 * math.pi))
    range_term_db = 40 * math.log10(range_m)
    rcs_term_db = 10 * math.log10(rcs_m2)
    power_dbm = 10 * math.log10(tx_power_w * 1000)
    return (
        power_dbm
        + tx_gain_dbi
        + rx_gain_dbi
        + geometric_term_db
        + rcs_term_db
        - range_term_db
        - system_losses_db
    )


def noise_floor_dbm(bandwidth_hz: float, noise_figure_db: float) -> float:
    if bandwidth_hz <= 0:
        return float("nan")
    thermal_noise_dbm = -174 + 10 * math.log10(bandwidth_hz)
    return thermal_noise_dbm + noise_figure_db


def burn_through_range_km(
    tx_power_w: float,
    tx_gain_dbi: float,
    jammer_power_w: float,
    jammer_gain_dbi: float,
    wavelength_m: float,
    rcs_m2: float,
    desired_js_db: float,
) -> float:
    """Approximate burn-through range where S/J meets the desired J/S."""
    if any(val <= 0 for val in (tx_power_w, jammer_power_w, wavelength_m, rcs_m2)):
        return float("nan")
    pt_db = 10 * math.log10(tx_power_w)
    pj_db = 10 * math.log10(jammer_power_w)
    sigma_db = 10 * math.log10(rcs_m2)
    lambda_db = 20 * math.log10(wavelength_m)
    numerator_db = pt_db + 2 * tx_gain_dbi + sigma_db + lambda_db
    denominator_db = pj_db + jammer_gain_dbi + 20 * math.log10(4 * math.pi) + desired_js_db
    # S/J proportional to 1/R^4, so range term exponent is 1/4 in dB domain.
    range_db = 0.25 * (numerator_db - denominator_db)
    return 10 ** (range_db) / 1000


def beamwidth_gain_dbi(horizontal_bw_deg: float, vertical_bw_deg: float, efficiency: float) -> float:
    if horizontal_bw_deg <= 0 or vertical_bw_deg <= 0 or efficiency <= 0:
        return float("nan")
    gain_linear = (
        efficiency
        * (41253 / (horizontal_bw_deg * vertical_bw_deg))
    )
    return 10 * math.log10(gain_linear)


def range_resolution_m(pulse_width_us: float) -> float:
    if pulse_width_us <= 0:
        return float("nan")
    return 3e8 * (pulse_width_us * 1e-6) / 2


def bandwidth_resolution_m(bandwidth_mhz: float) -> float:
    if bandwidth_mhz <= 0:
        return float("nan")
    return 3e8 / (2 * bandwidth_mhz * 1e6)


def fresnel_radius_m(distance_km: float, freq_ghz: float, zone_number: int = 1) -> float:
    if distance_km <= 0 or freq_ghz <= 0:
        return float("nan")
    wavelength = 0.3 / freq_ghz
    d_m = distance_km * 1000
    return math.sqrt(zone_number * wavelength * d_m / 2)


def earth_bulge_m(distance_km: float) -> float:
    return (distance_km ** 2) / 12.75


def unambiguous_velocity_ms(freq_ghz: float, prf_hz: float) -> float:
    if freq_ghz <= 0 or prf_hz <= 0:
        return float("nan")
    wavelength = 0.3 / freq_ghz
    return wavelength * prf_hz / 4


def dwell_time_ms(beamwidth_deg: float, rpm: float) -> float:
    if beamwidth_deg <= 0 or rpm <= 0:
        return float("nan")
    return (60 / rpm) * (beamwidth_deg / 360) * 1000


def overview_page():
    st.title("Radar Designer eGuide")
    st.write(
        """Interactive, multi-page reference inspired by the radar and electronic warfare
        eGuide. Use the sidebar to jump between design inputs, EW considerations, propagation,
        antenna performance, radar modes, and core equations. Each section includes inline
        calculators so you can explore trade-offs while reviewing the formulas."""
    )
    st.info(
        "Paste figure JPGs from the source eGuide into the placeholder expandable sections to "
        "complete the visual references."
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


def design_inputs_page():
    st.header("Design Inputs & Link Budget")
    st.write(
        "Estimate received power and SNR for a monostatic radar using the two-way radar equation."
    )
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


def ew_page():
    st.header("Electronic Warfare & Burn-Through")
    st.write(
        "Explore the burn-through range where the radar echo exceeds jammer energy at the receiver."
    )
    col1, col2 = st.columns(2)
    with col1:
        tx_power_w = st.number_input("Radar power (W)", min_value=0.1, value=5000.0, key="ew_tx")
        tx_gain_dbi = st.number_input("Radar antenna gain (dBi)", value=32.0, key="ew_gt")
        freq_ghz = st.number_input("Radar frequency (GHz)", min_value=0.1, value=10.0, key="ew_f")
        rcs_m2 = st.number_input("Target RCS (m²)", min_value=0.0001, value=1.0, format="%.4f", key="ew_rcs")
    with col2:
        jammer_power_w = st.number_input("Jammer power (W)", min_value=0.1, value=1000.0)
        jammer_gain_dbi = st.number_input("Jammer antenna gain (dBi)", value=10.0)
        desired_js_db = st.number_input("Desired J/S margin (dB)", value=0.0, help="Positive values model stronger jamming; negative favors the radar.")
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


def propagation_page():
    st.header("Propagation & Clearance")
    st.write("Compute Fresnel clearance, Earth bulge, and attenuation-friendly budgets.")
    col1, col2 = st.columns(2)
    with col1:
        distance_km = st.number_input("Path length (km)", min_value=0.1, value=20.0)
        freq_ghz = st.number_input("Frequency (GHz)", min_value=0.1, value=5.0, key="prop_f")
        zone = st.number_input("Fresnel zone number", min_value=1, value=1, step=1)
    with col2:
        rain_loss_db_km = st.number_input("Rain/atmospheric loss (dB/km)", min_value=0.0, value=0.05)
        misc_loss_db = st.number_input("Other path losses (dB)", min_value=0.0, value=2.0)
    fresnel = fresnel_radius_m(distance_km, freq_ghz, zone)
    bulge = earth_bulge_m(distance_km)
    fspl_value = fspl_db(distance_km, freq_ghz)
    total_env_loss = distance_km * rain_loss_db_km + misc_loss_db
    st.metric("First Fresnel zone radius (m)", f"{fresnel:.2f}")
    st.metric("Earth bulge at midpoint (m)", f"{bulge:.2f}")
    st.metric("Free-space path loss (dB)", f"{fspl_value:.2f}")
    st.metric("Atmospheric + misc. loss (dB)", f"{total_env_loss:.2f}")
    st.caption("Ensure at least 60% Fresnel clearance and add bulge/obstacles for true clearance margins.")


def antenna_page():
    st.header("Antenna Gain & Beamwidth")
    st.write("Estimate antenna gain from -3 dB beamwidths and efficiency.")
    col1, col2 = st.columns(2)
    with col1:
        h_bw = st.number_input("Horizontal beamwidth (°)", min_value=0.1, value=3.0)
        v_bw = st.number_input("Vertical beamwidth (°)", min_value=0.1, value=3.0)
    with col2:
        efficiency = st.slider("Antenna efficiency", min_value=0.2, max_value=0.8, value=0.55, step=0.01)
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


def radar_modes_page():
    st.header("Radar Modes, Timing & Resolution")
    st.write("Compare unmodulated and chirp resolution, Doppler limits, and dwell time.")
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
    dwell_ms = dwell_time_ms(beamwidth_deg, rpm)
    st.metric("Unmodulated range resolution (m)", f"{rng_res_unmod:.2f}")
    st.metric("Chirp range resolution (m)", f"{rng_res_chirp:.2f}")
    st.metric("Max unambiguous radial velocity (m/s)", f"{v_unamb:.2f}")
    st.metric("Dwell time per beam (ms)", f"{dwell_ms:.2f}")
    st.caption("Dwell ≈ 6·PRT/beam for MTI; use staggered PRFs to balance range/velocity ambiguities.")


def main():
    st.set_page_config(page_title="Radar Designer", layout="wide")
    pages = {
        "Overview": overview_page,
        "Design inputs": design_inputs_page,
        "Electronic warfare": ew_page,
        "Propagation": propagation_page,
        "Antenna": antenna_page,
        "Radar modes": radar_modes_page,
    }
    choice = st.sidebar.radio("Navigate", list(pages.keys()))
    pages[choice]()


if __name__ == "__main__":
    main()
