"""Antenna models, efficiency, and field-region notes."""
import streamlit as st

from calculations import beamwidth_gain_dbi, beamwidth_gain_elliptical_dbi

st.title("Antenna Models, Efficiency & Field Regions")

st.markdown(
    r"""
    Simplified antenna models compare illuminated areas and directivity:

    * **Rectangular mainlobe model** assumes uniform energy inside the -3 dB beamwidths with gain
      \(G_{\text{rect}} \approx \eta\,\dfrac{41253}{\theta_{\text{az}}\,\theta_{\text{el}}}\) (beamwidths in degrees).
    * **Elliptical solid-angle model** uses \(\Omega_A = \theta_{\text{az}}\,\theta_{\text{el}}\) in radians with
      \(G_{\text{ellip}} \approx \eta\,\dfrac{4\pi}{\Omega_A}\); this is about 78% of the rectangular estimate for narrow beams.

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
    * **Reactive near-field:** immediately adjacent; E and H fields are not in phase and the angular distribution depends on distance.
    * **Radiating near-field (Fresnel):** fields are in phase but pattern still varies with range. A common boundary heuristic is
      \(r_2 \approx 2d^2/\lambda\) for aperture diameter \(d\).
    * **Far-field (Fraunhofer):** E and H orthogonal and pattern distance-independent; a practical start point is \(R_{ff} \gtrsim 0.62\,d^2/\lambda\).
    """
)

st.divider()

st.subheader("Beamwidth, beam solid angle, and sidelobes")
st.markdown(
    r"""
    * Half-power beamwidths define the footprint; **two-way beamwidth** matters for monostatic radars where TX and RX patterns must overlap.
    * Beam solid angle \(\Omega_A \approx \theta_{\text{az}}\,\theta_{\text{el}}\) (radians) feeds directivity \(D \approx 4\pi/\Omega_A\).
    * Antenna patterns: pencil (narrow/narrow), fan (narrow az, wide el), beaver-tail (wider az, narrow el), cosecant-squared (range-compensated elevation), and omni.
    * Low sidelobes, sidelobe blanking/cancellation, and grating-lobe control support EP measures.
    * Beamwidth factor and sidelobe suppression influence effective isotropic radiated power (EIRP = \(P_t G_t\)).
    """
)

st.subheader("Antenna types")
st.markdown(
    """
    Dipoles, patches, helices, horns, slotted waveguides, reflectors, and phased arrays cover polarizations from linear to circular.
    Gain ranges from ~2 dBi (isotropic reference) up to 40+ dBi for large dishes; beamwidth varies with aperture size and taper.
    """
)
