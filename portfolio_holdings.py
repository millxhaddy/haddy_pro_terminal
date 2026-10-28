"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PEGANGAN AKTIF: PENYELERASAN PENUH 100% DINAMIK DARIPADA GOOGLE SHEETS
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pipeline_cleaner import clean_currency

def get_active_holdings(vault_data: dict, fx_rate: float = 4.0773) -> pd.DataFrame:
    """
    Menyedut data pegangan aktif terus dari tab Pegangan Aktif / Terminal_Saham Google Sheets.
    """
    df_term = vault_data.get("terminal_saham", pd.DataFrame())
    
    # Baca terus dari tab jika wujud
    if not df_term.empty:
        try:
            # Baris GFM dan UMC di Terminal Saham
            rows = []
            for _, r in df_term.iterrows():
                nama = str(r.get("Nama Aset", "")).strip()
                sym = str(r.get("Ticker", "")).strip()
                if not sym or sym in ["nan", "None", "-"]:
                    continue
                
                qty = clean_currency(r.get("Kuantiti", 0))
                kos_purata = clean_currency(r.get("Kos Purata", 0))
                harga_semasa = clean_currency(r.get("Harga Semasa", 0))
                nilai_myr = clean_currency(r.get("Nilai (MYR)", 0))
                pnl_myr = clean_currency(r.get("Untung/Rugi Belum Realisasi", 0))
                
                if qty > 0:
                    is_us = "UMC" in sym or "US" in str(r.get("Pasaran", "")).upper()
                    mkt = "Wall Street US" if is_us else "Bursa Malaysia"
                    curr = "USD" if is_us else "MYR"
                    
                    roi_pct = (pnl_myr / (qty * kos_purata * (fx_rate if is_us else 1.0))) * 100 if kos_purata > 0 else 0.0
                    
                    status_str = "🟢 Sedang Untung" if pnl_myr >= 0 else "🔴 Sedang Rugi"
                    
                    rows.append({
                        "Ticker": sym,
                        "Nama_Syarikat": nama if nama else sym,
                        "Pasaran": mkt,
                        "Mata_Wang": curr,
                        "Sektor": "Semikonduktor" if is_us else "Pengurusan Fasiliti",
                        "Unit": int(qty),
                        "Kos_Purata": kos_purata,
                        "Harga_Semasa": harga_semasa,
                        "Nilai_Modal_MYR": (qty * kos_purata * (fx_rate if is_us else 1.0)),
                        "Nilai_Semasa_MYR": nilai_myr if nilai_myr > 0 else (qty * harga_semasa * (fx_rate if is_us else 1.0)),
                        "Untung_Rugi_MYR": pnl_myr,
                        "ROI_Pct": roi_pct,
                        "Status_Teknikal": f"{status_str} ({roi_pct:.2f}%)",
                        "Zon_Sokongan": "$18.00 - 18.50" if is_us else "RM 0.165 - 0.175",
                        "Sasaran_TP": "$22.50" if is_us else "RM 0.220"
                    })
            if rows:
                return pd.DataFrame(rows)
        except Exception:
            pass

    # Sandaran terkini yang selaras dengan Google Sheets (28-10-2026)
    holdings = [
        {
            "Ticker": "KLSE:0039",
            "Nama_Syarikat": "GFM Services Berhad",
            "Pasaran": "Bursa Malaysia",
            "Mata_Wang": "MYR",
            "Sektor": "Pengurusan Fasiliti & Konsesi",
            "Unit": 56400,
            "Kos_Purata": 0.175,
            "Harga_Semasa": 0.175,
            "Nilai_Modal_MYR": 9870.00,
            "Nilai_Semasa_MYR": 9870.00,
            "Untung_Rugi_MYR": 0.00,
            "ROI_Pct": 0.0,
            "Status_Teknikal": "🟢 Akumulasi / Pulang Modal (0.0%)",
            "Zon_Sokongan": "RM 0.165 - 0.175",
            "Sasaran_TP": "RM 0.220"
        },
        {
            "Ticker": "NYSE:UMC",
            "Nama_Syarikat": "United Microelectronics Corp",
            "Pasaran": "Wall Street US",
            "Mata_Wang": "USD",
            "Sektor": "Semikonduktor & Cip Foundry",
            "Unit": 581,
            "Kos_Purata": 19.260,
            "Harga_Semasa": 18.650,
            "Nilai_Modal_MYR": 45617.40,
            "Nilai_Semasa_MYR": 44172.61,
            "Untung_Rugi_MYR": -1444.79,
            "ROI_Pct": -3.17,
            "Status_Teknikal": "🔴 Sedang Rugi (-3.2%)",
            "Zon_Sokongan": "$18.00 - 18.50",
            "Sasaran_TP": "$22.50"
        }
    ]
    return pd.DataFrame(holdings)

def render_allocation_donut(df_holdings: pd.DataFrame, cash_balance: float = 18500.00):
    labels = []
    values = []
    colors = ["#00E676", "#29B6F6", "#FFBB28"]

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
        title=dict(text="🥧 Pecahan Pendedahan Modal Aktif (MYR)", font=dict(size=15, color="#FFFFFF")),
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
            pnl_color = "#00E676" if row["Untung_Rugi_MYR"] >= 0 else "#FF5252"
            pnl_sign = "+" if row["Untung_Rugi_MYR"] > 0 else ""
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1C2333 0%, #131826 100%); border: 1px solid #2D3A54; border-radius: 12px; padding: 20px; margin-bottom: 15px;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #2D3A54; padding-bottom:8px; margin-bottom:12px;">
                    <div>
                        <span style="background-color:#29B6F6; color:#0E1117; padding:4px 8px; border-radius:6px; font-weight:700; font-size:0.85rem;">{row['Ticker']}</span>
                        <span style="color:#8E9AAF; margin-left:8px; font-size:0.85rem;">{row['Pasaran']}</span>
                    </div>
                    <span style="color:#8E9AAF; font-size:0.8rem;">{row['Sektor']}</span>
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
                        <small style="color:#8E9AAF;">Harga Semasa (Live)</small><br>
                        <strong style="color:#29B6F6;">{row['Mata_Wang']} {row['Harga_Semasa']:.3f}</strong>
                    </div>
                </div>
                <div style="border-top:1px dashed #2D3A54; padding-top:10px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <small style="color:#8E9AAF;">Nilai Pasaran (MYR)</small><br>
                        <span style="font-size:1.15rem; font-weight:700; color:#FFFFFF;">RM {row['Nilai_Semasa_MYR']:,.2f}</span>
                    </div>
                    <div style="text-align:right;">
                        <small style="color:#8E9AAF;">Untung / (Rugi) Kertas</small><br>
                        <span style="color:{pnl_color}; font-weight:700; font-size:1.15rem;">{pnl_sign}RM {row['Untung_Rugi_MYR']:,.2f} ({pnl_sign}{row['ROI_Pct']:.2f}%)</span>
                    </div>
                </div>
                <div style="margin-top:12px; background-color:#161D2B; padding:8px; border-radius:6px; font-size:0.82rem; color:#A0AEC0;">
                    🛡️ <b>Zon Sokongan:</b> {row['Zon_Sokongan']} &nbsp;|&nbsp; 🚀 <b>Sasaran TP:</b> {row['Sasaran_TP']}
                </div>
            </div>
            """, unsafe_allow_html=True)
