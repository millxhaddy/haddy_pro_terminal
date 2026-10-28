"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PILIHAN 4: INTEGRASI MOOMOO OPEND DESKTOP GATEWAY (BURSA & WALL STREET)
========================================================================================
"""

import streamlit as st
import pandas as pd

def check_opend_connection(host="127.0.0.1", port=11111) -> dict:
    """
    Menyemak status kesambungan ke gateway desktop Moomoo OpenD.
    """
    try:
        from moomoo import OpenQuoteContext
        ctx = OpenQuoteContext(host=host, port=port)
        ctx.close()
        return {"connected": True, "status": "🟢 TERSAMBUNG KE MOOMOO OPEND", "mode": "Live Gateway"}
    except Exception as e:
        return {"connected": False, "status": "🟡 MOD SIMULASI (OPEND STANDBY)", "mode": "Simulation / Paper Mode"}

def render_moomoo_opend_panel(fx_rate=4.0773):
    """
    Antara muka kawalan eksekusi dan diagnostik Moomoo OpenD Gateway.
    """
    st.subheader("⚡ Kawalan Eksekusi Moomoo OpenD Gateway")
    
    conn_info = check_opend_connection()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Status Gerbang OpenD", conn_info["mode"], conn_info["status"])
    with c2:
        st.metric("Akaun Sasaran", "Universal Account (8702)", "Bursa & US Wall St")
    with c3:
        st.metric("Enjin Keselamatan", "DDNK 3M Compliant", "Stop-Loss Mandatori")

    st.markdown("---")
    
    with st.expander("🛠️ Panduan Konfigurasi Moomoo OpenD Gateway"):
        st.markdown("""
        1. **Muat Turun & Buka Moomoo OpenD**: Buka aplikasi Moomoo OpenD di komputer anda.
        2. **Log Masuk Akaun**: Log masuk menggunakan akaun Moomoo yang berdaftar dengan akaun `8702`.
        3. **Port Lalai**: Pastikan tetapan listen IP ialah `127.0.0.1` dan Port `11111`.
        4. **Pelepasan Kunci**: Sahkan kod laluan dagangan (Trading Password) di OpenD sebelum menghantar pesanan automatik.
        """)
