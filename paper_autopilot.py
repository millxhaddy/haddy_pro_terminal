"""
HADDY PRO - TERMINAL MILLX
MODUL 2: BOT SIMULASI DAGANGAN AUTOMATIK (PAPER-TRADING AUTO-PILOT BOT)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def initialize_paper_engine():
    if "paper_balance" not in st.session_state:
        st.session_state["paper_balance"] = 100000.00
    if "paper_positions" not in st.session_state:
        st.session_state["paper_positions"] = [
            {"Tarikh": "28-10-2026", "Ticker": "KLSE:SUNCON", "Pasaran": "Bursa", "Unit": 2500, "Harga Beli": 3.95, "SL": 3.75, "TP": 4.46, "Nilai (MYR)": 9875.00, "Status": "Berjalan"},
            {"Tarikh": "28-10-2026", "Ticker": "NASDAQ:NVDA", "Pasaran": "US", "Unit": 15, "Harga Beli": 141.20, "SL": 134.00, "TP": 161.36, "Nilai (MYR)": 8635.72, "Status": "Berjalan"}
        ]
    if "paper_history" not in st.session_state:
        st.session_state["paper_history"] = [
            {"Tarikh Keluar": "27-10-2026", "Ticker": "KLSE:YTLPOWR", "Unit": 2000, "Beli": 4.60, "Jual": 4.98, "Untung (MYR)": 760.00, "ROI": "+8.26%", "Status": "TP Capai"},
            {"Tarikh Keluar": "25-10-2026", "Ticker": "NASDAQ:MRVL", "Unit": 30, "Beli": 85.00, "Jual": 82.50, "Untung (MYR)": -305.80, "ROI": "-2.94%", "Status": "Cut Loss SOP"}
        ]

def render_paper_autopilot_ui():
    initialize_paper_engine()
    st.subheader("🤖 Bot Simulasi Dagangan Automatik (Paper-Trading Auto-Pilot)")
    st.caption("Ujian strategi pasaran langsung tanpa risiko modal sebenar.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Baki Tunai Maya", f"RM {st.session_state['paper_balance']:,.2f}")
    c2.metric("Posisi Berjalan", f"{len(st.session_state['paper_positions'])} Posisi")
    
    total_closed = len(st.session_state["paper_history"])
    wins = len([x for x in st.session_state["paper_history"] if x["Untung (MYR)"] > 0])
    win_rate = (wins / total_closed * 100) if total_closed > 0 else 0
    c3.metric("Paper Win Rate", f"{win_rate:.1f}%", f"{wins}/{total_closed} Menang")
    
    total_paper_pnl = sum([x["Untung (MYR)"] for x in st.session_state["paper_history"]])
    c4.metric("Untung Bersih Maya", f"RM {total_paper_pnl:,.2f}")

    st.markdown("---")
    st.markdown("#### 📦 Posisi Simulasi Aktif (Paper Holdings):")
    st.dataframe(pd.DataFrame(st.session_state["paper_positions"]), width="stretch", hide_index=True)

    st.markdown("---")
    st.markdown("#### 📜 Sejarah Transaksi Selesai (Paper History):")
    st.dataframe(pd.DataFrame(st.session_state["paper_history"]), width="stretch", hide_index=True)

    if st.button("🔄 Tetapkan Semula Modal Maya (Reset RM 100,000)"):
        st.session_state["paper_balance"] = 100000.00
        st.session_state["paper_positions"] = []
        st.session_state["paper_history"] = []
        st.rerun()
