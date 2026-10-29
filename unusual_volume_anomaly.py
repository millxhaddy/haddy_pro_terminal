"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 9: ENJIN PENGESAN ANOMALI VOLUM (RVOL) & PERANGKAP MANIPULASI PASARAN
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def get_unusual_volume_data():
    """Mengesan anomali volum luar biasa merentasi saham Bursa dan Wall Street."""
    records = [
        {
            "Ticker": "KLSE:SUNCON", "Pasaran": "Bursa Malaysia", "Harga": 3.95,
            "Volum_Semasa": "14.2M", "Purata_20D": "4.1M", "RVOL": 3.46,
            "Perubahan_Pct": "+4.2%", "Status_Anomali": "🟢 Pengumpulan Jerung (Accumulation)",
            "Risiko_Manipulasi": "Rendah (Gred Institusi)", "Tindakan": "Ikut Aliran (Buy Dip)"
        },
        {
            "Ticker": "NASDAQ:NVDA", "Pasaran": "Wall Street US", "Harga": 141.20,
            "Volum_Semasa": "68.5M", "Purata_20D": "24.1M", "RVOL": 2.84,
            "Perubahan_Pct": "+2.8%", "Status_Anomali": "🟢 Breakout Volum Tinggi",
            "Risiko_Manipulasi": "Sifar (Mega-Cap AI)", "Tindakan": "Follow Trend"
        },
        {
            "Ticker": "KLSE:YTLPOWR", "Pasaran": "Bursa Malaysia", "Harga": 4.98,
            "Volum_Semasa": "28.4M", "Purata_20D": "10.8M", "RVOL": 2.63,
            "Perubahan_Pct": "+3.1%", "Status_Anomali": "🟢 Ujian Bekalan Rendah (Spring)",
            "Risiko_Manipulasi": "Rendah (Pusat Data AI)", "Tindakan": "Kekal Posisi"
        },
        {
            "Ticker": "KLSE:KAUNTER_X (Simulasi)", "Pasaran": "Bursa Malaysia", "Harga": 0.28,
            "Volum_Semasa": "45.0M", "Purata_20D": "1.2M", "RVOL": 37.50,
            "Perubahan_Pct": "+28.5%", "Status_Anomali": "🔴 AMARAN PUMP & DUMP (SINDIKET)",
            "Risiko_Manipulasi": "KRITIKAL (Penny Stock Trap)", "Tindakan": "ELAKKAN SAMA SEKALI"
        },
        {
            "Ticker": "NYSE:UMC (Aktif)", "Pasaran": "Wall Street US", "Harga": 18.65,
            "Volum_Semasa": "12.8M", "Purata_20D": "15.2M", "RVOL": 0.84,
            "Perubahan_Pct": "-0.8%", "Status_Anomali": "⚪ Volum Rendah (Mendatar)",
            "Risiko_Manipulasi": "Sifar (Foundry Global)", "Tindakan": "Kawal Lantai $18.50"
        },
        {
            "Ticker": "KLSE:0039 (GFM)", "Pasaran": "Bursa Malaysia", "Harga": 0.175,
            "Volum_Semasa": "420K", "Purata_20D": "1.8M", "RVOL": 0.23,
            "Perubahan_Pct": "0.0%", "Status_Anomali": "⚪ Volum Kering (Hibernasi)",
            "Risiko_Manipulasi": "Rendah (Modal Mati)", "Tindakan": "Tunggu Breakout RM 0.190"
        }
    ]
    return pd.DataFrame(records)

def render_unusual_volume_scanner_ui():
    st.subheader("⚡ Pengimbas Anomali Volum (RVOL) & Perangkap Manipulasi Pasaran")
    st.caption("Mengesan Volume Spread Analysis (VSA) luar biasa di mana volum melebihi 2.0x purata, serta perisai penapis 'Pump & Dump'.")

    df_anom = get_unusual_volume_data()

    # Kad Skor Ringkasan Anomali
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Saham Dikesan Lonjakan Volum", "3 Kaunter", "RVOL > 2.5x")
    with c2:
        st.metric("Aktiviti Jerung Institusi", "SUNCON, NVDA, YTL", "Aliran Masuk Bersih")
    with c3:
        st.metric("Amaran Perangkap Sindiket", "1 Kaunter", "Risiko Manipulasi", delta_color="inverse")
    with c4:
        st.metric("Status Pegangan (UMC & GFM)", "Volum Rendah / Kering", "Tiada Panik Selling")

    st.markdown("---")

    # Jadual Interaktif Pengimbas
    st.dataframe(
        df_anom.style.map(
            lambda v: "color: #00E676; font-weight: bold;" if "🟢" in str(v) else ("color: #FF1744; font-weight: bold;" if "🔴" in str(v) else "color: #8E9AAF;"),
            subset=["Status_Anomali"]
        ).map(
            lambda v: "color: #FF1744; font-weight: bold;" if "KRITIKAL" in str(v) else "color: #00E676;",
            subset=["Risiko_Manipulasi"]
        ),
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # Panduan Logik Pengesanan
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div style="background:#0F291E; border:2px solid #00E676; border-radius:10px; padding:16px;">
            <h4 style="color:#00E676; margin-top:0;">🟢 Sinyal Akumulasi Jerung Tulen:</h4>
            <ul>
                <li><b>RVOL antara 2.0x hingga 4.0x:</b> Peningkatan volum terkawal dengan kenaikan harga sederhana (+2% hingga +5%).</li>
                <li><b>Skor Fundamental Kukuh:</b> Disokong oleh Skor CANSLIM A+ dan Piotroski F-Score >= 7.</li>
                <li><b>Tindakan Disiplin:</b> Beli semasa harga membuat ujian semula (Pullback/Retest) ke paras sokongan.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div style="background:#2A080E; border:2px solid #FF1744; border-radius:10px; padding:16px;">
            <h4 style="color:#FF1744; margin-top:0;">🔴 Ciri-Ciri Perangkap Pump & Dump:</h4>
            <ul>
                <li><b>RVOL Melampau (> 10x hingga 30x):</b> Lonjakan volum mendadak tanpa sebarang asas laporan suku tahunan rasmi.</li>
                <li><b>Saham Sen (Penny Stocks < RM0.30):</b> Kenaikan harga melampau (+20% ke +50%) dalam masa 1-2 hari.</li>
                <li><b>Tindakan Disiplin:</b> JANGAN SESEKALI MASUK! Sindiket sedang mencari pembeli naif sebelum menjatuhkan harga!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)