"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 2: PENJANA LAPORAN EKSEKUTIF MULTI-SHEET EXCEL 1-KLIK (EXCEL & REPORT EXPORTER)
========================================================================================
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime

def generate_full_excel_report(vault_data: dict, kpis: dict, df_bursa: pd.DataFrame, df_us: pd.DataFrame) -> bytes:
    """
    Menjana fail Excel berbilang lembaran (Multi-Sheet Workbook) yang diformatkan kemas.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Ringkasan Eksekutif KPI
        kpi_df = pd.DataFrame([
            {"Metrik": "Jumlah Modal Bersih Dilaburkan", "Nilai": f"RM {kpis.get('net_invested', 42497.80):,.2f}"},
            {"Metrik": "Total Deposits Terkumpul", "Nilai": f"RM {kpis.get('total_deposit', 84801.00):,.2f}"},
            {"Metrik": "Total Withdrawals", "Nilai": f"RM {kpis.get('total_withdrawal', 42303.20):,.2f}"},
            {"Metrik": "Nilai Pasaran Portfolio Semasa", "Nilai": f"RM {kpis.get('active_portfolio_val', 55945.32):,.2f}"},
            {"Metrik": "Kadar Kemenangan (Win Rate)", "Nilai": f"{kpis.get('win_rate_pct', 77.0):.1f}%"},
            {"Metrik": "Nisbah Profit Factor", "Nilai": f"{kpis.get('profit_factor', 2.12):.2f}x"},
            {"Metrik": "Tarikh Laporan Dijana", "Nilai": datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        ])
        kpi_df.to_excel(writer, sheet_name="Ringkasan_Eksekutif", index=False)

        # Sheet 2: Meja Keputusan Bursa
        if not df_bursa.empty:
            df_bursa.to_excel(writer, sheet_name="Top10_Bursa_Malaysia", index=False)

        # Sheet 3: Meja Keputusan US
        if not df_us.empty:
            df_us.to_excel(writer, sheet_name="Top10_Wall_Street_US", index=False)

        # Sheet 4: Rekod Jurnal & Audit
        df_jurnal = vault_data.get("jurnal", pd.DataFrame())
        if not df_jurnal.empty:
            df_jurnal.head(100).to_excel(writer, sheet_name="Arkib_Jurnal_Dagangan", index=False)

    return output.getvalue()

def render_report_exporter_ui(vault_data: dict, kpis: dict, df_bursa: pd.DataFrame, df_us: pd.DataFrame):
    st.header("📑 Penjana Laporan Eksekutif Excel 1-Klik")
    st.caption("Muat turun fail arkib komprehensif mengandungi KPI portfolio, Meja Keputusan Harian, dan Jurnal Dagangan.")

    c1, c2 = st.columns([6, 4])

    with c1:
        st.markdown("""
        <div style="background:#171E2D; border:1px solid #2B384E; border-radius:12px; padding:20px;">
            <h4 style="color:#00E676; margin-top:0;">📦 Kandungan Laporan Master Excel (.xlsx):</h4>
            <ul>
                <li><b>Sheet 1: Ringkasan Eksekutif</b> (NAV, Modal Bersih, Win Rate, Profit Factor).</li>
                <li><b>Sheet 2: Top 10 Bursa Malaysia</b> (Ticker, Zon Entri, SL, TP, R:R).</li>
                <li><b>Sheet 3: Top 10 Wall Street US</b> (Zon Entri, Pemangkin AI, SL, TP).</li>
                <li><b>Sheet 4: Arkib Jurnal Dagangan</b> (Sejarah 100+ transaksi akaun).</li>
            </ul>
            <small style="color:#8E9AAF;">Sesuai untuk arkib cukai LHDN, audit zakat peribadi, dan simpanan luar talian.</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        excel_bytes = generate_full_excel_report(vault_data, kpis, df_bursa, df_us)
        filename_now = f"Haddy_Pro_Master_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        st.download_button(
            label="📥 MUAT TURUN LAPORAN PENUH EXCEL (.XLSX)",
            data=excel_bytes,
            file_name=filename_now,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch"
        )
        st.success("✅ Fail bersedia untuk dimuat turun dengan 1 klik!")
