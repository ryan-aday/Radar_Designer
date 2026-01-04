"""ISM bands, general frequency bands, and radar allocations."""
import streamlit as st

st.title("Frequency Bands & ISM Allocations")
st.markdown(
    r"""
    ### ISM bands
    Portions of spectrum reserved for industrial, scientific, and medical uses.
    Type A bands require coordination; Type B bands require services to accept interference.
    """
)

ism_rows = [
    ("6.765–6.795 MHz", "30 kHz", "A", "Special authorization"),
    ("13.553–13.567 MHz", "14 kHz", "B", "Global"),
    ("26.957–27.283 MHz", "326 kHz", "B", "CB radio, global"),
    ("40.66–40.7 MHz", "40 kHz", "B", "Global"),
    ("433.05–434.79 MHz", "1.74 MHz", "A", "Remote control, Europe"),
    ("902–928 MHz", "26 MHz", "B", "Americas"),
    ("2.4–2.5 GHz", "100 MHz", "B", "Wi‑Fi, global"),
    ("5.725–5.875 GHz", "150 MHz", "B", "Wi‑Fi, global"),
    ("24.00–24.25 GHz", "250 MHz", "B", "Global"),
    ("61.00–61.5 GHz", "500 MHz", "A", "Local acceptance"),
    ("122–123 GHz", "1 GHz", "A", "Local acceptance"),
    ("244–246 GHz", "2 GHz", "A", "Local acceptance"),
]

st.table({
    "Frequency range": [r[0] for r in ism_rows],
    "Bandwidth": [r[1] for r in ism_rows],
    "Type": [r[2] for r in ism_rows],
    "Remark": [r[3] for r in ism_rows],
})

st.markdown(
    r"""
    ### Common frequency-band lettering
    * **VLF–HF (A–C)**: 3 kHz–30 MHz
    * **VHF–UHF (D–G)**: 30 MHz–3 GHz
    * **SHF–EHF (H–M)**: 3 GHz–300 GHz
    """
)

st.markdown(
    r"""
    ### Radar-frequency examples
    Representative allocations used by surveillance, weather, and navigation radars.
    """
)

radar_rows = [
    ("3–40 MHz", "Over-the-horizon"),
    ("46–68 MHz", "Wind profilers"),
    ("150–350 MHz", "Anti-stealth"),
    ("420–450 MHz", "Early warning"),
    ("850–950 MHz", "Long-range surveillance"),
    ("1.215–1.35 GHz", "Long-range air defense / ATC"),
    ("2.7–3.1 GHz", "Radar and navigation"),
    ("3.1–3.41 GHz", "Airborne surveillance"),
    ("4.2–4.4 GHz", "Radio altimeters"),
    ("5.25–5.725 GHz", "Tactical, VTS, weapon control"),
    ("5.725–5.85 GHz", "Weather"),
    ("8.5–10 GHz", "Precision approach, air defense"),
    ("9.3–9.5 GHz", "Airborne weather, multifunction"),
    ("9.5–9.8 GHz", "Spaceborne"),
    ("10.0–10.5 GHz", "Civil/military"),
    ("13.25–14.0 GHz", "Military, ship berthing"),
    ("15.4–15.7 GHz", "Ground movement"),
    ("15.7–17.2 GHz", "Military"),
    ("17.2–17.7 GHz", "Missile control"),
    ("24.0–24.5 GHz", "Satellite rain radar, ISM"),
    ("31.8–33.4 GHz", "Airborne"),
    ("33.4–35.2 GHz", "Short-range motion"),
    ("35.2–36.0 GHz", "Satellite rain radar"),
    ("59.0–64.0 GHz", "Airborne"),
    ("76.0–77.5 GHz", "Road transport radars"),
    ("92.0–95.0 GHz", "Short-range"),
    ("94.0–94.1 GHz", "Cloud profiler"),
    ("237.9–238.0 GHz", "Spaceborne cloud radar"),
]

st.table({
    "Frequency range": [r[0] for r in radar_rows],
    "Application": [r[1] for r in radar_rows],
})

st.caption("Drop frequency-band and radar-allocation figures here for quick reference.")
