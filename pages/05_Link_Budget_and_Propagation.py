"""Link budget, Fresnel clearance, and propagation extras."""
import math
import streamlit as st

from calculations import earth_bulge_m, fresnel_radius_m, fspl_db, noise_floor_dbm, radar_received_power_dbm

st.title("Link Budget, Fresnel Zone, and Propagation")
st.markdown(r"Estimate received power and SNR with the two-way radar equation (monostatic, point target):")
st.latex(r"P_r = P_t G_t G_r \left( \frac{\lambda}{4\pi R} \right)^4 \frac{\sigma}{L_{\text{tot}}}")
st.caption("Variables: $P_t$ transmit power, $G_t/G_r$ antenna gains, $\lambda$ wavelength, $R$ range, $\sigma$ RCS, $L_{tot}$ total losses.")

cols = st.columns(2)
with cols[0]:
    tx_power_w = st.number_input("Transmitter power $P_t$ (W)", min_value=0.1, value=1000.0, help="Peak pulse power.")
    tx_gain_dbi = st.number_input("TX antenna gain $G_t$ (dBi)", value=30.0, help="Mainlobe gain toward target.")
    rx_gain_dbi = st.number_input("RX antenna gain $G_r$ (dBi)", value=30.0, help="Assume monostatic: same as $G_t$ if shared.")
    freq_ghz = st.number_input("Carrier frequency $f$ (GHz)", min_value=0.1, value=10.0, help="Sets wavelength $\lambda=0.3/f$.")
    rcs_m2 = st.number_input("Target RCS $\sigma$ (m²)", min_value=0.0001, value=1.0, format="%.4f", help="Radar cross section.")
    range_km = st.number_input("Target range $R$ (km)", min_value=0.1, value=50.0)
with cols[1]:
    losses_db = st.number_input("Total losses $L_{tot}$ (dB)", value=10.0, help="Propagation + system + processing.")
    bandwidth_mhz = st.number_input("Noise bandwidth $B$ (MHz)", min_value=0.001, value=5.0, help="Receiver IF bandwidth.")
    noise_figure_db = st.number_input("Noise figure NF (dB)", min_value=0.0, value=3.0, help="Receiver NF or Fn.")
    required_snr_db = st.number_input("Required SNR (dB)", value=13.0, help="Choose per PD/FAR and Swerling case margins.")

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

st.subheader("Link results")
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
st.subheader("FSPL and clearance")
st.latex(r"\text{FSPL (dB)} = 32.45 + 20\log_{10}(R_{\text{km}}) + 20\log_{10}(f_{\text{MHz}})")

col1, col2 = st.columns(2)
with col1:
    distance_km = st.number_input("Path length $d$ (km)", min_value=0.1, value=20.0, help="TX-RX separation.")
    freq_ghz_clear = st.number_input("Frequency for clearance $f$ (GHz)", min_value=0.1, value=5.0, key="prop_f", help="Sets $\lambda=0.3/f$.")
    zone = st.number_input("Fresnel zone number $n$", min_value=1, value=1, step=1)
with col2:
    rain_loss_db_km = st.number_input("Rain/atmospheric loss (dB/km)", min_value=0.0, value=0.05, help="Rain + gaseous loss per km.")
    misc_loss_db = st.number_input("Other path losses (dB)", min_value=0.0, value=2.0, help="Knife-edge, foliage, mismatch.")

fresnel = fresnel_radius_m(distance_km, freq_ghz_clear, zone)
bulge = earth_bulge_m(distance_km)
fspl_value = fspl_db(distance_km, freq_ghz_clear)
total_env_loss = distance_km * rain_loss_db_km + misc_loss_db

st.metric("First Fresnel zone radius (m)", f"{fresnel:.2f}")
st.metric("Earth bulge at midpoint (m)", f"{bulge:.2f}")
st.metric("Free-space path loss (dB)", f"{fspl_value:.2f}")
st.metric("Atmospheric + misc. loss (dB)", f"{total_env_loss:.2f}")
st.caption("Maintain ≈60% Fresnel clearance and account for bulge/obstacles for fade margin.")

st.subheader("Propagation notes")
st.markdown(
    r"""
    * **Fresnel zone distance:** beyond the first-zone distance, two-ray interference dominates; below it, FSPL applies.
    * **Two-ray model:** LOS + ground reflection combine with phase \(\phi = 2\pi (d_2-d_1)/\lambda\); destructive cases yield \(-40\log R\) slope.
    * **Knife-edge diffraction:** Fresnel–Kirchhoff parameter \(v = h\sqrt{2/\lambda\,(1/d_1 + 1/d_2)}\); loss \(L_{KED} \approx 1.27v^2 + 9v + 6\) dB for \(0<v<2.4\).
    * **Earth bulge:** midpoint height \(H \approx d^2/12.75\) (m) for distance \(d\) in km.
    * **Atmospheric attenuation:** often negligible below 10 GHz; above, include rain plus gaseous peaks.
    * **Antenna beams for command-guided missiles:** capture, guidance, and track beams widen from launch to terminal phases.
    """
)
