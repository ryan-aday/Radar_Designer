"""Shared radar-related calculations for the Streamlit app."""
import math


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
    gain_linear = efficiency * (41253 / (horizontal_bw_deg * vertical_bw_deg))
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
    return (distance_km**2) / 12.75


def unambiguous_velocity_ms(freq_ghz: float, prf_hz: float) -> float:
    if freq_ghz <= 0 or prf_hz <= 0:
        return float("nan")
    wavelength = 0.3 / freq_ghz
    return wavelength * prf_hz / 4


def dwell_time_ms(beamwidth_deg: float, rpm: float) -> float:
    if beamwidth_deg <= 0 or rpm <= 0:
        return float("nan")
    return (60 / rpm) * (beamwidth_deg / 360) * 1000
