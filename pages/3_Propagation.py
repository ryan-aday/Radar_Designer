"""Propagation, Fresnel, and path loss checks."""
import streamlit as st

from calculations import earth_bulge_m, fresnel_radius_m, fspl_db

st.title("Propagation & Clearance")
st.write("Compute Fresnel clearance, Earth bulge, and attenuation-friendly budgets.")
st.latex(r"r_n = \sqrt{\frac{n \lambda d}{2}} \qquad h_\text{bulge} \approx \frac{d^2}{12.75}")

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
