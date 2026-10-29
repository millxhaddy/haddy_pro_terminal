"""
HADDY PRO - TERMINAL MILLX
MODUL 3: PENYATA KEUNTUNGAN MODAL & PENGURUSAN CUKAI LHDN (TAX LEDGER)
"""

import streamlit as st
import pandas as pd

def render_tax_ledger_ui():
    st.subheader("🏛️ Penyata Keuntungan Modal & Audit Cukai LHDN (Tax Ledger)")
    st.caption("Pengasingan keuntungan modal terealisasi mengikut tahun taksiran bagi tujuan pematuhan cukai dan rekod peribadi.")

    year_selected = st.selectbox("Pilih Tahun Taksiran:", ["2026 (Tahun Semasa)", "2025", "2024"])

    tax_summary_data = {
        "2026": {"untung_bursa": 3700.20, "untung_us": 29447.00, "dividen_myr": 2424.44, "yuran_broker": 1250.00},
        "2025": {"untung_bursa": -500.00, "untung_us": 1250.00, "dividen_myr": 1100.00, "yuran_broker": 850.00},
        "2024": {"untung_bursa": 2100.00, "untung_us": 4800.00, "dividen_myr": 650.00, "yuran_broker": 620.00}
    }
    y_key = year_selected.split()[0]
    dt = tax_summary_data.get(y_key, tax_summary_data["2026"])

    net_gain = dt["untung_bursa"] + dt["untung_us"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Keuntungan Modal Bersih", f"RM {net_gain:,.2f}")
    c2.metric("Untung Pasaran Tempatan (Bursa)", f"RM {dt['untung_bursa']:,.2f}")
    c3.metric("Untung Pasaran Asing (US)", f"RM {dt['untung_us']:,.2f}")
    c4.metric("Jumlah Dividen Diterima", f"RM {dt['dividen_myr']:,.2f}")

    st.markdown("---")
    st.markdown("#### 📋 Klasifikasi Cukai di Malaysia (Akta Cukai Pendapatan 1967):")
    st.markdown("""
    - **Keuntungan Modal Saham Bursa Malaysia:** Dikecualikan daripada Cukai Pendapatan bagi pelabur individu (*Individual Capital Gains Tax Exemption*).
    - **Pendapatan Punca Luar Negara (FSI - US Wall Street):** Tertakluk kepada syarat statutori pengecualian cukai FSI sekiranya telah dikenakan cukai pegangan (*Withholding Tax 30%* pada dividen AS).
    - **Yuran Transaksi Brokerage:** Boleh ditolak sebagai kos operasi pelaburan bagi pengiraan keuntungan bersih.
    """)

    ledger_rows = [
        {"Kategori": "Untung Kasar Saham Tempatan (Bursa)", "Amaun": f"RM {dt['untung_bursa']:,.2f}", "Status Percukaian": "Dikecualikan Cukai Individu"},
        {"Kategori": "Untung Saham Luar Negara (US Wall Street)", "Amaun": f"RM {dt['untung_us']:,.2f}", "Status Percukaian": "Pengecualian FSI Bersyarat"},
        {"Kategori": "Hasil Dividen Bersih", "Amaun": f"RM {dt['dividen_myr']:,.2f}", "Status Percukaian": "Tolak Cukai Pegangan Asing (30%)"},
        {"Kategori": "Yuran & Caj Transaksi Broker", "Amaun": f"-RM {dt['yuran_broker']:,.2f}", "Status Percukaian": "Kos Operasi / Ditolak"}
    ]
    st.dataframe(pd.DataFrame(ledger_rows), width="stretch", hide_index=True)
