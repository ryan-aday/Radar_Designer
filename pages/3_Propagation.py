"""Propagation, Fresnel, and path loss checks."""
import streamlit as st

from calculations import earth_bulge_m, fresnel_radius_m, fspl_db

st.title("Propagation & Clearance")
st.write("Compute Fresnel clearance, Earth bulge, and attenuation-friendly budgets.")
st.latex(r"r_n = \sqrt{\frac{n \lambda d}{2}} \qquad h_\text{bulge} \approx \frac{d^2}{12.75}")
st.caption("Variables: $n$ Fresnel zone index, $\lambda$ wavelength, $d$ link length (m), bulge formula uses $d$ in km per eGuide.")

col1, col2 = st.columns(2)
with col1:
    distance_km = st.number_input("Path length $d$ (km)", min_value=0.1, value=20.0, help="TX-RX separation.")
    freq_ghz = st.number_input("Frequency $f$ (GHz)", min_value=0.1, value=5.0, key="prop_f", help="Sets $\lambda=0.3/f$.")
    zone = st.number_input("Fresnel zone number $n$", min_value=1, value=1, step=1)
with col2:
    rain_loss_db_km = st.number_input("Rain/atmospheric loss (dB/km)", min_value=0.0, value=0.05, help="Use Fig. 10 guidance.")
    misc_loss_db = st.number_input("Other path losses (dB)", min_value=0.0, value=2.0, help="Knife-edge, foliage, mismatch.")

fresnel = fresnel_radius_m(distance_km, freq_ghz, zone)
bulge = earth_bulge_m(distance_km)
fspl_value = fspl_db(distance_km, freq_ghz)
total_env_loss = distance_km * rain_loss_db_km + misc_loss_db

st.metric("First Fresnel zone radius (m)", f"{fresnel:.2f}")
st.metric("Earth bulge at midpoint (m)", f"{bulge:.2f}")
st.metric("Free-space path loss (dB)", f"{fspl_value:.2f}")
st.metric("Atmospheric + misc. loss (dB)", f"{total_env_loss:.2f}")
st.caption("Ensure at least 60% Fresnel clearance and add bulge/obstacles for true clearance margins.")

st.divider()
st.subheader("Additional eGuide propagation notes")
st.markdown(
    r"""
    * **Fresnel zone distance:** beyond the first-zone distance, two-ray interference dominates; below it, FSPL applies.
    * **Two-ray model:** LOS + ground reflection combine with phase \(\phi = 2\pi (d_2-d_1)/\lambda\); destructive interference yields \(-40\log R\) slope.
    * **Knife-edge diffraction:** use Fresnel–Kirchhoff parameter \(v = h\sqrt{2/(\lambda)(1/d_1 + 1/d_2)}\); approximate loss \(L_{KED} \approx 1.27v^2 + 9v + 6\) dB for \(0<v<2.4\).
    * **Earth bulge:** \(H = d^2/66\) (m) or \(d^2/12.75\) (m at midpoint) per eGuide Fig. 9, where \(d\) is in km.
    * **Atmospheric attenuation:** below 10 GHz often negligible; above, add rain + gas peaks shown in Fig. 10/11.
    """
)
