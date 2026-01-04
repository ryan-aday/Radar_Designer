"""Radar cross section, retroreflectors, and scattering modes."""
import math
import streamlit as st

from calculations import rayleigh_sphere_rcs_m2

st.title("RCS, Retroreflectors & Scattering Regions")

st.markdown(
    r"""
    The eGuide classifies scattering for simple and complex targets:
    * **Rayleigh region (small vs. wavelength):** \(\sigma_{sphere} \approx \pi^5 d^6 / \lambda^4\).
    * **Mie/resonance region:** creeping-wave interference can amplify or cancel returns (up to 4× or 0.25× the optical value).
    * **Optical region:** geometric optics dominates; specular and edge diffraction drive \(\sigma\).
    
    Composite airframes mix tip, edge, cavity, and traveling-wave echoes (Fig. 39). Fluctuation loss and Swerling cases model the resulting RCS spread.
    """
)

col1, col2 = st.columns(2)
with col1:
    wavelength_m = st.number_input("Wavelength $\\lambda$ (m)", min_value=0.001, value=0.03)
    diameter_m = st.number_input("Sphere diameter $d$ (m)", min_value=0.001, value=0.1)
with col2:
    sigma_rayleigh = rayleigh_sphere_rcs_m2(diameter_m, wavelength_m)
    sigma_optical = math.pi * (diameter_m**2) / 4  # reflective sphere optical limit
    st.metric("Rayleigh σ (m²)", f"{sigma_rayleigh:.6f}")
    st.metric("Optical σ approx. (m²)", f"{sigma_optical:.4f}")
    st.caption("Rayleigh valid when d ≪ λ; optical approximation dominates when d ≫ λ.")

st.divider()

st.subheader("Retroreflectors and decoys")
st.markdown(
    r"""
    * **Corner reflectors and van Atta arrays** return energy to the source; enlarging one corner beats multiple small ones.
    * **Active decoys** apply gain \(G_{amp}\) and retransmit: \(\sigma_{sim} \approx 39 + G_{amp} - 20\log_{10}(f_{MHz})\) dBsm (eGuide Fig. 18).
    * **Chaff** clouds create volume clutter. Single dipole RCS averages \(\sigma_1 \approx 0.155\,\lambda^2\); dense pulse volumes scale with dipole count \(N\).
    """
)

with st.expander("Paste figure placeholders"):
    st.write("RCS aspect plots, retroreflector sketches, and chaff photos from the eGuide fit here.")
