"""Jamming and deception references with support-jamming J/S calculator."""
import streamlit as st

from calculations import support_jamming_js_db

st.title("Jamming & Deception")
st.write(
    "Summarize noise/spot/barrage/swept/pulse deception techniques and estimate J/S for support or sidelobe jamming."
)

with st.expander("Jamming and deception notes"):
    st.markdown(
        r"""
- **Noise jamming**: continuous random noise to mask echoes.
- **Spot / swept / barrage**: concentrate power in narrow bands, sweep them, or flood the band.
- **Pulse / cover-pulse**: keyed to radar rotation or echo reception to hide followers.
- **Repeater / RGPO / VGPO**: record and delay or frequency-shift returns to walk range/velocity gates off target.
- **Blip enhancement**: boost echo to simulate larger targets.
- **Cross-eye, JAFF/CHILL**: angular errors via phase tricks or illuminating chaff clouds.
        """
    )
    st.markdown(
        r"""
Additional deception surfaces: **decoys** (active van Atta or corner), **chaff** clouds (RCS ∝ $N\,\sigma_1$), and **burn-through** occurs when radar S exceeds jammer J.
        """
    )

st.latex(r"\textbf{Self/escort J/S: } \frac{J}{S} = \frac{P_j G_j / (4\pi R_j^2)}{P_t G_t^2 \sigma / ((4\pi)^3 R_t^4)}")
st.latex(r"\textbf{Burn-through: } R_{BT} \approx \left( \frac{P_t G_t^2 \lambda^2 \sigma}{P_j G_j (4\pi)^2 (J/S)} \right)^{1/4}")

st.latex(r"\textbf{Support J/S: } J/S = ERP_J-ERP_T+11+G_M-G_S+40\log R_T - 20\log R_J -10\log f")
st.caption(
    r"Variables: $ERP_J$ jammer EIRP (W), $ERP_T$ target/comm EIRP (W), $G_M$ mainlobe gain, $G_S$ sidelobe gain, $R_T$ range to target (km), $R_J$ range to jammer (km), $f$ MHz carrier."
)

col1, col2, col3 = st.columns(3)
with col1:
    erp_j = st.number_input(r"Jammer ERP $ERP_J$ (W)", min_value=0.1, value=10000.0)
    erp_t = st.number_input(r"Target ERP $ERP_T$ (W)", min_value=0.001, value=50.0)
    freq_mhz = st.number_input(r"Carrier $f$ (MHz)", min_value=1.0, value=3000.0)
with col2:
    gm = st.number_input(r"Radar mainlobe gain $G_M$ (dBi)", value=30.0)
    gs = st.number_input(r"Radar sidelobe gain $G_S$ (dBi)", value=0.0)
with col3:
    rt = st.number_input(r"Range radar→target $R_T$ (km)", min_value=0.1, value=100.0)
    rj = st.number_input(r"Range radar→jammer $R_J$ (km)", min_value=0.1, value=50.0)

js_db = support_jamming_js_db(erp_j, erp_t, gm, gs, rt, rj, freq_mhz)
st.metric("J/S (dB)", f"{js_db:.2f}")

st.info("Positive J/S favors the jammer; reducing sidelobes, adding ECCM (LPI, agility, sidelobe blanking) lowers effective J/S.")
