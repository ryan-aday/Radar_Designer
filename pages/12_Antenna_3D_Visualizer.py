"""Interactive 3D antenna pattern visualizer with adjustable dimensions."""
from __future__ import annotations

import math
from typing import Dict

import numpy as np
import plotly.graph_objects as go
import streamlit as st


def gaussian_gain(theta: np.ndarray, beamwidth_deg: float) -> np.ndarray:
    """Approximate mainlobe with -3 dB at beamwidth/2 using a Gaussian taper."""
    beamwidth_deg = max(1e-3, beamwidth_deg)
    theta0 = math.radians(beamwidth_deg / 2) / math.sqrt(math.log(2))
    return np.exp(-(theta / theta0) ** 2)


def beamwidth_from_aperture(aperture_m: float, wavelength_m: float, scale: float = 70.0) -> float:
    """Empirical beamwidth estimate ~ scale * lambda / D (degrees)."""
    if aperture_m <= 0 or wavelength_m <= 0:
        return 180.0
    return min(180.0, max(1.0, scale * wavelength_m / aperture_m))


def pattern_for_type(
    antenna_type: str,
    theta: np.ndarray,
    phi: np.ndarray,
    wavelength_m: float,
    aperture_m: float,
    element_count: int,
    front_back_db: float,
) -> np.ndarray:
    """Return normalized power pattern over theta/phi for the requested antenna archetype."""
    fb_linear = 10 ** (-front_back_db / 10)
    if antenna_type == "Isotropic radiator":
        pattern = np.ones_like(theta)
    elif antenna_type in {"Halfwave dipole", "PCB dipole w/ reflector", "Folded dipole", "Biconical", "Rectangle loop"}:
        base = np.sin(theta) ** 2
        if antenna_type == "PCB dipole w/ reflector":
            pattern = base * (1 + 0.5 * np.cos(phi))
        elif antenna_type == "Folded dipole":
            pattern = base * 1.2
        elif antenna_type == "Biconical":
            pattern = base ** 0.8
        elif antenna_type == "Rectangle loop":
            pattern = (np.sin(theta) ** 2) * (np.cos(theta) ** 2 + 0.3)
        else:
            pattern = base
    elif antenna_type == "1/4 wave whip (monopole)":
        hemi = np.sin(theta) ** 2
        pattern = np.where(theta <= math.pi / 2, hemi, hemi * fb_linear)
    elif antenna_type in {"Patch antenna", "Tapered slot antenna"}:
        bw = beamwidth_from_aperture(aperture_m or wavelength_m, wavelength_m, scale=65.0)
        pattern = gaussian_gain(theta, bw) * (np.cos(phi) ** 2 + 0.3)
    elif antenna_type in {"Pyramidal horn", "Conical horn"}:
        bw = beamwidth_from_aperture(aperture_m or wavelength_m, wavelength_m, scale=55.0)
        pattern = gaussian_gain(theta, bw)
    elif antenna_type == "Helix":
        bw = min(80.0, 52 * math.sqrt(wavelength_m / max(aperture_m, wavelength_m)))
        pattern = gaussian_gain(theta, bw)
    elif antenna_type == "Yagi":
        bw = max(12.0, 100.0 / max(element_count, 1))
        pattern = gaussian_gain(theta, bw) * (np.cos(phi) ** 2 + 0.5)
    elif antenna_type == "Parabolic antenna":
        bw = beamwidth_from_aperture(aperture_m or wavelength_m, wavelength_m, scale=70.0)
        pattern = gaussian_gain(theta, bw)
    elif antenna_type == "Phased array":
        bw = max(2.0, 50.0 * wavelength_m / max(element_count * (aperture_m or wavelength_m), wavelength_m))
        pattern = gaussian_gain(theta, bw)
    elif antenna_type == "Logarithmic-periodic dipole antenna":
        bw = 60.0
        pattern = gaussian_gain(theta, bw) * (0.7 + 0.3 * np.cos(phi) ** 2)
    elif antenna_type == "Lindenblad antenna":
        pattern = np.sin(theta) ** 2 * 0.8 + 0.2
    else:
        pattern = np.ones_like(theta)

    # Apply a simple front-to-back shaping.
    pattern = np.where(theta <= math.pi / 2, pattern, pattern * fb_linear)
    # Normalize to peak = 1.
    peak = np.max(pattern)
    return pattern / peak if peak > 0 else pattern


def plot_pattern(pattern: np.ndarray, theta: np.ndarray, phi: np.ndarray, title: str) -> go.Figure:
    """Convert spherical gain pattern to Cartesian surface for visualization."""
    r = pattern
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    surface = go.Surface(x=x, y=y, z=z, surfacecolor=10 * np.log10(r + 1e-6), colorscale="Turbo", showscale=True)
    fig = go.Figure(data=[surface])
    fig.update_layout(
        title=title,
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z", aspectmode="data"),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


TYPICAL_SPECS: Dict[str, str] = {
    "Isotropic radiator": "0 dBi reference, 360° beamwidth, linear polarization (definition only).",
    "Halfwave dipole": "~2.1 dBi, 80° elevation beam, linear pol; broad azimuth omni.",
    "PCB dipole w/ reflector": "4–6 dBi with reflector, narrower front lobe, linear pol.",
    "Folded dipole": "~3 dBi, broader bandwidth than halfwave dipole, linear pol.",
    "Patch antenna": "5–9 dBi, 40°–80° beam, linear or circular pol; bandwidth ~3%.",
    "Tapered slot antenna": "6–12 dBi, 40°–70° beam, linear pol, 2–4 octave bandwidth.",
    "1/4 wave whip (monopole)": "~5.2 dBi over ground plane, 45°–90° elevation beam, vertical pol.",
    "Helix": "8–15 dBi axial mode, 40°–60° beam, circular pol; gain ~15 N (C/λ)^2 (S/λ).",
    "Pyramidal horn": "10–20 dBi, 15°–40° beam, linear pol; bandwidth ~5%.",
    "Conical horn": "8–15 dBi, 20°–50° beam, linear/circular pol; bandwidth ~5%.",
    "Yagi": "6–15 dBi, 15°–50° beam depending on elements, linear pol.",
    "Parabolic antenna": "20–45 dBi, beamwidth \(\approx 70\lambda/D\), linear/circular pol depending on feed.",
    "Phased array": "Gain scales with element count; beamwidth \(\approx 0.88\lambda/(Nd)\); electronic steering.",
    "Logarithmic-periodic dipole antenna": "4–8 dBi, 50°–70° beam, very wideband, linear pol.",
    "Lindenblad antenna": "3–7 dBi, near-omni in azimuth with circular pol (satellite comms).",
    "Biconical": "1–4 dBi, broadband omni with vertical pol; 80° elevation beam typical.",
    "Rectangle loop": "1–3 dBi, figure-8 pattern; loop size sets bandwidth, linear pol.",
}


st.title("Antenna Pattern 3D Visualizer")
st.markdown(
    """
    Visualize approximate 3D patterns for common antenna types. Adjust frequency, aperture/length,
    element count, and front-to-back ratio to see how beamwidth and directivity change. Patterns use
    simplified Gaussian or sinusoidal shapes for quick comparison; detailed EM design should use
    full-wave tools. Elliptical vs. rectangular gain models remain available on the **Antenna Models** page.
    """
)

antenna_type = st.selectbox(
    "Antenna type",
    [
        "Isotropic radiator",
        "Halfwave dipole",
        "PCB dipole w/ reflector",
        "Folded dipole",
        "Patch antenna",
        "Tapered slot antenna",
        "1/4 wave whip (monopole)",
        "Helix",
        "Pyramidal horn",
        "Conical horn",
        "Yagi",
        "Parabolic antenna",
        "Phased array",
        "Logarithmic-periodic dipole antenna",
        "Lindenblad antenna",
        "Biconical",
        "Rectangle loop",
    ],
)

col1, col2, col3 = st.columns(3)
with col1:
    freq_ghz = st.number_input("Frequency f (GHz)", min_value=0.1, value=10.0, step=0.1)
    wavelength_m = 0.3 / freq_ghz
    aperture_help = "Aperture/diameter/boom length (m) affecting beamwidth; defaults to one wavelength."
    aperture_m = st.number_input("Aperture or length (m)", min_value=0.01, value=float(round(wavelength_m, 3)), help=aperture_help)

with col2:
    element_count = st.slider("Element count (arrays/Yagi)", min_value=1, max_value=64, value=8)
    front_back_db = st.slider("Front-to-back ratio (dB)", min_value=0.0, max_value=40.0, value=10.0)

with col3:
    st.caption("Wavelength λ = {:.3f} m".format(wavelength_m))
    st.caption("Beamwidth scales roughly with λ/D; array elements narrow the beam and raise gain.")

theta = np.linspace(0, math.pi, 90)
phi = np.linspace(0, 2 * math.pi, 181)
theta_grid, phi_grid = np.meshgrid(theta, phi)

pattern = pattern_for_type(antenna_type, theta_grid, phi_grid, wavelength_m, aperture_m, element_count, front_back_db)
fig = plot_pattern(pattern, theta_grid, phi_grid, f"{antenna_type} normalized pattern")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Typical specifications")
spec_text = TYPICAL_SPECS.get(antenna_type, "Specs vary with implementation.")
st.markdown(f"- {spec_text}")
st.markdown("- Adjust aperture/length to see how the -3 dB beamwidth narrows with larger electrical size.")
st.markdown("- Use element count to approximate array directivity; arrays retain sidelobe sensitivity to taper and spacing.")
