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


def beamwidth_gain_elliptical_dbi(horizontal_bw_deg: float, vertical_bw_deg: float, efficiency: float) -> float:
    """Elliptical solid-angle model (4π/Ω) with beamwidths in degrees."""
    if horizontal_bw_deg <= 0 or vertical_bw_deg <= 0 or efficiency <= 0:
        return float("nan")
    theta_az_rad = math.radians(horizontal_bw_deg)
    theta_el_rad = math.radians(vertical_bw_deg)
    omega = theta_az_rad * theta_el_rad
    gain_linear = efficiency * (4 * math.pi) / omega
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


def radar_horizon_km(antenna_height_m: float, target_height_m: float | None = None) -> float:
    """Line-of-sight radar horizon in km (4.12*sqrt(h) with h in meters)."""
    if antenna_height_m < 0:
        return float("nan")
    base = 4.12 * math.sqrt(antenna_height_m)
    if target_height_m is not None and target_height_m >= 0:
        return base + 4.12 * math.sqrt(target_height_m)
    return base


def eirp_dbm(tx_power_w: float, tx_gain_dbi: float) -> float:
    """Effective isotropic radiated power in dBm."""
    if tx_power_w <= 0:
        return float("nan")
    return 10 * math.log10(tx_power_w * 1000) + tx_gain_dbi


def height_from_range_el_m(range_km: float, elevation_deg: float, r_equiv_km: float = 8500) -> float:
    """Approximate target height from slant range and elevation using equivalent earth radius."""
    if range_km < 0 or r_equiv_km <= 0:
        return float("nan")
    range_m = range_km * 1000
    e_rad = math.radians(elevation_deg)
    return range_m * math.sin(e_rad) + (range_m**2) / (2 * r_equiv_km * 1000)


def rayleigh_sphere_rcs_m2(diameter_m: float, wavelength_m: float) -> float:
    """Approximate Rayleigh-region RCS for a sphere (valid when diameter << wavelength)."""
    if diameter_m <= 0 or wavelength_m <= 0:
        return float("nan")
    # σ ≈ (π^5 * d^6)/(λ^4) for small spheres (Rayleigh scattering)
    return (math.pi**5) * (diameter_m**6) / (wavelength_m**4)


def angular_resolution_m(range_km: float, beamwidth_deg: float) -> float:
    """Cross-range spacing resolved by beamwidth (approx R*θ for small angles)."""
    if range_km < 0 or beamwidth_deg <= 0:
        return float("nan")
    return range_km * 1000 * math.radians(beamwidth_deg)


def resolution_cell_volume_m3(
    range_km: float, beamwidth_az_deg: float, beamwidth_el_deg: float, pulse_width_us: float
) -> float:
    """Pulse volume V = R^2 θAz θEl c0 τ / 8 (beamwidths in radians)."""
    if range_km < 0 or beamwidth_az_deg <= 0 or beamwidth_el_deg <= 0 or pulse_width_us < 0:
        return float("nan")
    r_m = range_km * 1000
    theta_az = math.radians(beamwidth_az_deg)
    theta_el = math.radians(beamwidth_el_deg)
    return (r_m**2) * theta_az * theta_el * 3e8 * (pulse_width_us * 1e-6) / 8


def one_way_received_power_dbm(
    tx_power_w: float, tx_gain_dbi: float, rx_gain_dbi: float, range_km: float, freq_ghz: float, losses_db: float
) -> float:
    """One-way link budget in dBm."""
    if tx_power_w <= 0 or freq_ghz <= 0 or range_km <= 0:
        return float("nan")
    pr_dbm = 10 * math.log10(tx_power_w * 1000) + tx_gain_dbi + rx_gain_dbi
    pr_dbm -= fspl_db(range_km, freq_ghz)
    pr_dbm -= losses_db
    return pr_dbm


def duty_cycle(pri_us: float, pulse_width_us: float) -> float:
    """Transmit duty factor (unitless fraction)."""
    if pri_us <= 0 or pulse_width_us < 0:
        return float("nan")
    return pulse_width_us / pri_us


def blind_range_m(pulse_width_us: float, dead_time_us: float = 0.0, recovery_time_us: float = 0.0) -> float:
    """Minimum detectable range due to transmit/receive dead time."""
    if pulse_width_us < 0 or dead_time_us < 0 or recovery_time_us < 0:
        return float("nan")
    total_us = pulse_width_us + dead_time_us + recovery_time_us
    return 3e8 * (total_us * 1e-6) / 2


def unambiguous_range_km(pri_us: float, pulse_width_us: float = 0.0) -> float:
    """Maximum unambiguous range for pulse radar."""
    if pri_us <= 0 or pulse_width_us < 0:
        return float("nan")
    effective_pri_s = max(pri_us * 1e-6 - pulse_width_us * 1e-6, 0)
    return 3e8 * effective_pri_s / 2 / 1000


def doppler_frequency_hz(freq_ghz: float, radial_speed_mps: float) -> float:
    """Doppler shift for a moving target (monostatic, radial speed)."""
    if freq_ghz <= 0:
        return float("nan")
    wavelength = 0.3 / freq_ghz
    return 2 * radial_speed_mps / wavelength


def enob_from_sinad(sinad_db: float) -> float:
    """Effective number of bits from SINAD (approx)."""
    return (sinad_db - 1.76) / 6.02


def sinad_from_enob(enob_bits: float) -> float:
    """SINAD derived from ENOB."""
    return enob_bits * 6.02 + 1.76


def support_jamming_js_db(
    erp_j_w: float,
    erp_t_w: float,
    mainlobe_gain_dbi: float,
    sidelobe_gain_dbi: float,
    range_target_km: float,
    range_jammer_km: float,
    freq_mhz: float,
) -> float:
    """J/S estimate for support/sidelobe jamming relationship."""
    if any(val <= 0 for val in (erp_j_w, erp_t_w, range_target_km, range_jammer_km, freq_mhz)):
        return float("nan")
    erp_j_dbw = 10 * math.log10(erp_j_w)
    erp_t_dbw = 10 * math.log10(erp_t_w)
    return (
        erp_j_dbw
        - erp_t_dbw
        + 11
        + mainlobe_gain_dbi
        - sidelobe_gain_dbi
        + 40 * math.log10(range_target_km)
        - 20 * math.log10(range_jammer_km)
        - 10 * math.log10(freq_mhz)
    )
