"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PEGANGAN AKTIF: STATUS GFM RUGI (-18.6%) & UMC OVER-ALLOCATION (AUDIT UPDATE)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pipeline_cleaner import clean_currency

def get_active_holdings(vault_data=None, fx_rate: float = 4.0773) -> pd.DataFrame:
    # Nilai Tepat Selaras Lembaran Ringkasan Mudah & Pegangan Aktif Google Sheets
    holdings = [
        {
            "Ticker": "KLSE:0039",
            "Nama_Syarikat": "GFM Services Berhad",
            "Pasaran": "Bursa Malaysia",
            "Mata_Wang": "MYR",
            "Sektor": "Pengurusan Fasiliti & Konsesi",
            "Unit": 56400,
            "Kos_Purata": 0.215,
            "Harga_Semasa": 0.175,
            "Nilai_Modal_MYR": 12126.00,
            "Nilai_Semasa_MYR": 9870.00,
            "Untung_Rugi_MYR": -2256.00,
            "ROI_Pct": -18.60,
            "Status_Teknikal": "⚠️ Amaran: Rugi Teruk (-18.6%) - Audit: Gagal Cut Loss DDNK",
            "Zon_Sokongan": "RM 0.165 (Lantai Kritikal)",
            "Sasaran_TP": "RM 0.220"
        },
        {
            "Ticker": "NYSE:UMC",
            "Nama_Syarikat": "United Microelectronics",
            "Pasaran": "Wall Street US",
            "Mata_Wang": "USD",
            "Sektor": "Semikonduktor & Cip Foundry",
            "Unit": 581,
            "Kos_Purata": 19.260,
            "Harga_Semasa": 18.820,
            "Nilai_Modal_MYR": 45446.20,
            "Nilai_Semasa_MYR": 44408.00,
            "Untung_Rugi_MYR": -1038.20,
            "ROI_Pct": -2.30,
            "Status_Teknikal": "⚠️ Amaran: Rugi (-2.3%) - Audit: Pendedahan Modal Melampau (81.8%)",
            "Zon_Sokongan": "$18.50 (Lantai Kritikal)",
            "Sasaran_TP": "$22.50"
        }
    ]
    return pd.DataFrame(holdings)

def render_allocation_donut(df_holdings: pd.DataFrame, cash_balance: float = 18500.00):
    labels = []
    values = []
    colors = ["#FF5252", "#FF7043", "#00E676"]

    for _, row in df_holdings.iterrows():
        labels.append(f"{row['Nama_Syarikat']} ({row['Pasaran']})")
        values.append(row["Nilai_Semasa_MYR"])

    labels.append("Baki Tunai Tersedia (Buffer)")
    values.append(cash_balance)

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#141824", width=3)),
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        textfont=dict(color="#FFFFFF", size=12),
        hovertemplate="<b>%{label}</b><br>Nilai: <b>RM %{value:,.2f}</b><br>Porsi: <b>%{percent}</b><extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="🥧 Pecahan Pendedahan Modal: Pendedahan Ekstrim UMC (81.8% Saham Aktif)", font=dict(size=14, color="#FFFFFF")),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#8E9AAF", size=10))
    )
    return fig

def render_holdings_cards(df_holdings: pd.DataFrame):
    cols = st.columns(len(df_holdings))
    for idx, row in df_holdings.iterrows():
        with cols[idx]:
            pnl_color = "#FF5252"
            pnl_sign = ""
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2D1118 0%, #150A0E 100%); border: 2px solid #FF5252; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(255, 82, 82, 0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #3E1A22; padding-bottom:8px; margin-bottom:12px;">
                    <div>
                        <span style="background-color:#FF5252; color:#FFFFFF; padding:4px 8px; border-radius:6px; font-weight:800; font-size:0.85rem;">{row['Ticker']}</span>
                        <span style="color:#8E9AAF; margin-left:8px; font-size:0.85rem;">{row['Pasaran']}</span>
                    </div>
                    <span style="color:#FFBB28; font-size:0.8rem; font-weight:bold;">{row['Sektor']}</span>
                </div>
                <h3 style="margin-top:0; color:#FFFFFF;">{row['Nama_Syarikat']}</h3>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <div>
                        <small style="color:#8E9AAF;">Unit Pegangan</small><br>
                        <strong>{row['Unit']:,} Unit</strong>
                    </div>
                    <div>
                        <small style="color:#8E9AAF;">Kos Purata</small><br>
                        <strong>{row['Mata_Wang']} {row['Kos_Purata']:.3f}</strong>
                    </div>
                    <div>
                        <small style="color:#8E9AAF;">Harga Semasa</small><br>
                        <strong style="color:#FF5252;">{row['Mata_Wang']} {row['Harga_Semasa']:.3f}</strong>
                    </div>
                </div>
                <div style="border-top:1px dashed #3E1A22; padding-top:10px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <small style="color:#8E9AAF;">Nilai Pasaran (MYR)</small><br>
                        <span style="font-size:1.15rem; font-weight:700; color:#FFFFFF;">RM {row['Nilai_Semasa_MYR']:,.2f}</span>
                    </div>
                    <div style="text-align:right;">
                        <small style="color:#8E9AAF;">Kerugian Kertas Semasa</small><br>
                        <span style="color:{pnl_color}; font-weight:700; font-size:1.15rem;">RM {row['Untung_Rugi_MYR']:,.2f} ({row['ROI_Pct']:.2f}%)</span>
                    </div>
                </div>
                <div style="margin-top:12px; background-color:#1E0B10; border-left:4px solid #FF1744; padding:8px; border-radius:4px; font-size:0.82rem; color:#FECDD3;">
                    🚨 <b>STATUS AUDIT:</b> {row['Status_Teknikal']}<br>
                    🛡️ <b>Had Lantai Mandatori:</b> {row['Zon_Sokongan']}
                </div>
            </div>
            """, unsafe_allow_html=True)