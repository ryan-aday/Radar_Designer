"""Antenna models, efficiency, and field-region notes."""
import streamlit as st

from calculations import beamwidth_gain_dbi, beamwidth_gain_elliptical_dbi

st.title("Antenna Models, Efficiency & Field Regions")

st.markdown(
    r"""
    The eGuide highlights simplified antenna models used to compare illuminated areas and gains:
    
    * **Rectangular mainlobe model** assumes all energy sits uniformly inside the -3 dB beamwidths. Its gain estimate is
      \(G_{\text{rect}} \approx \eta\,\dfrac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}\) (beamwidths in degrees),
      reflecting the \(16\) factor noted versus the true pattern area.
    * **Elliptical solid-angle model** uses the beam solid angle \(\Omega_A = \theta_{\text{az}}\,\theta_{\text{el}}\) in radians, giving
      \(G_{\text{ellip}} \approx \eta\,\dfrac{4\pi}{\Omega_A}\). The eGuide notes this differs from the rectangular model by roughly 78%.
    
    Antenna efficiency \(\eta\) (0.3–0.6 typical for dishes) corrects for taper, blockage, or non-uniform illumination.
    """
)

col1, col2 = st.columns(2)
with col1:
    h_bw = st.number_input(
        "Horizontal beamwidth $\\theta_{az}$ (deg)", min_value=0.1, value=3.0, help="-3 dB width in azimuth."
    )
    v_bw = st.number_input(
        "Vertical beamwidth $\\theta_{el}$ (deg)", min_value=0.1, value=3.0, help="-3 dB width in elevation."
    )
    efficiency = st.slider("Aperture efficiency $\\eta$", min_value=0.2, max_value=0.8, value=0.55, step=0.01)
with col2:
    gain_rect = beamwidth_gain_dbi(h_bw, v_bw, efficiency)
    gain_ellip = beamwidth_gain_elliptical_dbi(h_bw, v_bw, efficiency)
    st.metric("Rectangular model gain (dBi)", f"{gain_rect:.2f}")
    st.metric("Elliptical model gain (dBi)", f"{gain_ellip:.2f}")
    st.caption("Elliptical solid angle is more conservative; rectangular often used for quick comparisons.")

st.divider()

st.subheader("Field regions around an antenna")
st.markdown(
    r"""
    The eGuide separates three regions (see Fig. 3):
    * **Reactive near-field:** immediately adjacent; E and H fields not in phase and pattern depends on distance.
    * **Radiating near-field (Fresnel):** fields in phase but angular distribution still range-dependent. For short antennas \((d \ll \lambda)\),
      boundary \(r_2 \approx 2d^2/\lambda\); for large apertures, \(r_2 \approx 2d^2/\lambda\) also applies as an approximation.
    * **Far-field (Fraunhofer):** E and H orthogonal and distance-independent pattern; directivity and gain are referenced here.
    
    The eGuide uses the heuristic boundary \(R_{ff} \gtrsim 0.62\,d^2/\lambda\) for the start of far-field conditions.
    """
)

st.divider()

st.subheader("Beamwidth, beam solid angle, and sidelobes")
st.markdown(
    r"""
    * Half-power beamwidths define the footprint; **two-way beamwidth** matters for monostatic radars where TX and RX patterns must overlap.
    * Beam solid angle \(\Omega_A \approx \theta_{\text{az}}\,\theta_{\text{el}}\) (radians) feeds directivity \(D \approx 4\pi/\Omega_A\).
    * Cosecant-squared, pencil, fan, and beaver-tail patterns tailor beamwidths per mission (Fig. 14 in the eGuide).
    * Low sidelobes, sidelobe blanking/cancellation, and grating-lobe control underpin EP measures listed in the EW chapter.
    """
)

st.info("Drop pattern figures (pencil, fan, cosecant-squared, omni) from the eGuide into this page for visual references.")
