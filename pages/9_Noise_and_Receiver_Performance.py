"""Noise metrics, receiver sensitivity, and quantization references."""
import streamlit as st

from calculations import enob_from_sinad, noise_floor_dbm, sinad_from_enob

st.title("Noise & Receiver Performance")
st.write(
    "Bring the eGuide noise formulas into quick calculators to reason about sensitivity, SINAD, ENOB, and noise temperature."
)

with st.expander("Noise equations"):
    st.latex(r"\textbf{Sensitivity: } S = k T_s B_n L_n \;\;\text{with}\; MDS = -114 + 10\log_{10}(B_{\text{MHz}}) + NF")
    st.caption("$k$ Boltzmann constant, $T_s$ system temperature, $B_n$ noise bandwidth, $L_n$ losses, $NF$ noise figure.")
    st.latex(r"\textbf{Noise factor: } F_n = \frac{SNR_{in}}{SNR_{out}} \qquad \textbf{Noise figure: } NF = 10\log_{10}(F_n)")
    st.latex(r"\textbf{Noise temperature: } T_e = 290\,(10^{NF/10} - 1)\,\text{K}")
    st.latex(r"\textbf{SQNR} \approx 6.02\,N + 1.76 \qquad \textbf{ENOB} = \frac{\text{SINAD} - 1.76}{6.02}")
    st.markdown(
        "Noise types to consider: thermal, white, pink (1/f), brown (1/f²), blue, shot, dark, burst ('popcorn'), transit-time, phase noise."
    )

col1, col2, col3 = st.columns(3)
with col1:
    bw_mhz = st.number_input("Noise bandwidth $B$ (MHz)", min_value=0.001, value=1.0, format="%.3f")
    nf_db = st.number_input("Noise figure $NF$ (dB)", value=3.0, help="Receiver noise figure from LNA/backend.")
    noise_dbm = noise_floor_dbm(bw_mhz * 1e6, nf_db)
    st.metric("Noise floor / MDS (dBm)", f"{noise_dbm:.2f}")

with col2:
    sinad_db = st.number_input("SINAD (dB)", value=60.0, help="Signal-to-noise-and-distortion ratio.")
    st.latex(r"ENOB = \frac{\text{SINAD}-1.76}{6.02}")
    st.caption("Variables: SINAD includes noise + distortion; 1.76 dB quantization term; 6.02 converts dB to bits.")
    st.metric("ENOB (bits)", f"{enob_from_sinad(sinad_db):.2f}")

with col3:
    enob_bits = st.number_input("Target ENOB (bits)", min_value=1.0, value=12.0)
    st.latex(r"\text{SINAD} = 6.02\,N + 1.76")
    st.metric("Required SINAD (dB)", f"{sinad_from_enob(enob_bits):.2f}")

st.info(
    "Use low-noise amplifiers, filtering, and gain distribution to keep $F_n$ low; mitigation depends on which noise type dominates."
)
