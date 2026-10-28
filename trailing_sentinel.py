"""
HADDY PRO - TERMINAL MILLX
MODUL 2: RADAR AUTOMATIK TRAILING STOP & KUNCI UNTUNG (TRAILING SENTINEL)
"""

import streamlit as st
import pandas as pd

def calculate_trailing_stops(holdings: list) -> pd.DataFrame:
    records = []
    for h in holdings:
        entry = h["entry"]
        live = h["live"]
        peak = max(h["peak"], live)
        curr = h["currency"]

        if live >= entry * 1.05:
            ts_price = peak * 0.96
            status = "🟢 KUNCI UNTUNG (Trailing Aktif)"
        elif live < entry:
            ts_price = entry * 0.97
            status = "🔴 KAWAL RISIKO (Stop Loss Ketat)"
        else:
            ts_price = entry
            status = "🟡 PULANG MODAL (Break-even Guard)"

        distance_pct = ((live - ts_price) / live) * 100

        records.append({
            "Ticker": h["ticker"],
            "Mata Wang": curr,
            "Harga Belian": f"{curr} {entry:.3f}",
            "Harga Puncak": f"{curr} {peak:.3f}",
            "Harga Live": f"{curr} {live:.3f}",
            "Had Trailing Stop": f"{curr} {ts_price:.3f}",
            "Penampan Kejatuhan": f"{distance_pct:.2f}%",
            "Tindakan Sentinel": status
        })
    return pd.DataFrame(records)

def render_trailing_sentinel_ui():
    st.subheader("🛡️ Radar Trailing Stop & Kunci Untung (Profit Protection Sentinel)")
    st.caption("Penjaga garisan keuntungan dinamik bagi mengelakkan situasi untung bertukar menjadi rugi.")

    active_positions = [
        {"ticker": "KLSE:0039 (GFM Services)", "currency": "RM", "entry": 0.175, "live": 0.175, "peak": 0.190},
        {"ticker": "NYSE:UMC (United Microelectronics)", "currency": "$", "entry": 19.260, "live": 18.650, "peak": 21.070}
    ]

    df_sentinel = calculate_trailing_stops(active_positions)
    st.dataframe(df_sentinel, width="stretch", hide_index=True)

    st.markdown("""
    - **Kaunter UMC:** Puncak tertinggi pernah mencecah **$21.07**. Paras lantai semasa berada pada **$18.00**. Jika harga mencecah paras ini, sistem mengesyorkan keluar posisi serta-merta.
    - **Kaunter GFM:** Penampan ditetapkan pada **RM 0.170** bagi melindungi kos pokok belian.
    """)
