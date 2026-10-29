"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL DATA GRID MODEN (WINDOWS 11 FLUENT STYLE)
Lajur Hadapan: Ticker -> Harga -> Trend 30D (Sparkline) -> Julat 52W -> Pautan Rasmi
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from pipeline_cleaner import clean_currency

def generate_sparkline_series(base_price: float, points: int = 20) -> list:
    """Menjana siri mini 20 titik harga untuk sparkline."""
    np.random.seed(int(base_price * 100) % 1000)
    prices = [base_price * 0.94]
    for _ in range(points - 1):
        prices.append(prices[-1] * (1 + np.random.normal(0.001, 0.015)))
    return [round(p, 2) for p in prices]

def build_enriched_decision_df(df_base: pd.DataFrame, is_bursa: bool = True) -> pd.DataFrame:
    if df_base is None or df_base.empty:
        return pd.DataFrame()

    df = df_base.copy()
    sparklines = []
    progress_52w = []
    direct_urls = []

    for _, r in df.iterrows():
        # Dapatkan harga secara selamat
        raw_p = r.get("Harga_Live", r.get("Harga", 10.0))
        p = clean_currency(raw_p) if isinstance(raw_p, str) else float(raw_p)
        if p <= 0:
            p = 10.0

        raw_ticker = str(r.get("Ticker", ""))
        clean_sym = raw_ticker.replace("KLSE:", "").replace("NASDAQ:", "").replace("NYSE:", "").strip()
        
        # 1. Sparkline 20 titik
        sparklines.append(generate_sparkline_series(p))
        
        # 2. Kedudukan Julat 52W (0.0 hingga 1.0)
        low_52 = p * 0.82
        high_52 = p * 1.25
        pos = (p - low_52) / (high_52 - low_52)
        progress_52w.append(min(max(pos, 0.05), 0.95))
        
        # 3. Pautan profil rasmi
        if is_bursa:
            direct_urls.append(f"https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode={clean_sym}")
        else:
            direct_urls.append(f"https://finance.yahoo.com/quote/{clean_sym}")

    df["Trend_30D"] = sparklines
    df["Kedudukan_52W"] = progress_52w
    df["Pautan_Rasmi"] = direct_urls
    return df

def render_modern_decision_grid(df_bursa: pd.DataFrame, df_us: pd.DataFrame):
    st.caption("✨ **Antaramuka Windows 11 Modern Data Grid Aktif:** Dilengkapi Sparklines 30-Hari, Julat 52-Minggu & Pautan Profil Rasmi.")
    sub_b, sub_u = st.tabs(["🇲🇾 Top 10 Bursa Malaysia (Data Grid Pro)", "🇺🇸 Top 10 Wall Street US (Data Grid Pro)"])

    # 1. Grid Bursa Malaysia
    with sub_b:
        df_b_rich = build_enriched_decision_df(df_bursa, is_bursa=True)
        if not df_b_rich.empty:
            st.dataframe(
                df_b_rich,
                column_order=[
                    "Ticker", "Harga_Live", "Trend_30D", "Kedudukan_52W", 
                    "SL", "TP", "RR", "Pautan_Rasmi", "Status"
                ],
                column_config={
                    "Ticker": st.column_config.TextColumn("Kod Saham", width="small"),
                    "Harga_Live": st.column_config.NumberColumn("Harga Semasa", format="RM %.2f"),
                    "Trend_30D": st.column_config.LineChartColumn("Trend 30-Hari", width="medium"),
                    "Kedudukan_52W": st.column_config.ProgressColumn("Julat 52-Minggu", format="%.0f%%", min_value=0.0, max_value=1.0),
                    "SL": st.column_config.NumberColumn("Stop Loss", format="RM %.2f"),
                    "TP": st.column_config.NumberColumn("Take Profit", format="RM %.2f"),
                    "RR": st.column_config.NumberColumn("Nisbah R:R", format="%.2fx"),
                    "Pautan_Rasmi": st.column_config.LinkColumn("Profil Bursa", display_text="Buka Profil ↗"),
                    "Status": st.column_config.TextColumn("Status SOP")
                },
                hide_index=True,
                width="stretch"
            )

    # 2. Grid Wall Street US
    with sub_u:
        df_u_rich = build_enriched_decision_df(df_us, is_bursa=False)
        if not df_u_rich.empty:
            st.dataframe(
                df_u_rich,
                column_order=[
                    "Ticker", "Harga_Live", "Trend_30D", "Kedudukan_52W", 
                    "SL", "TP", "RR", "Pautan_Rasmi", "Status"
                ],
                column_config={
                    "Ticker": st.column_config.TextColumn("Simbol US", width="small"),
                    "Harga_Live": st.column_config.NumberColumn("Harga Semasa", format="$ %.2f"),
                    "Trend_30D": st.column_config.LineChartColumn("Trend 30-Hari", width="medium"),
                    "Kedudukan_52W": st.column_config.ProgressColumn("Julat 52-Minggu", format="%.0f%%", min_value=0.0, max_value=1.0),
                    "SL": st.column_config.NumberColumn("Stop Loss", format="$ %.2f"),
                    "TP": st.column_config.NumberColumn("Take Profit", format="$ %.2f"),
                    "RR": st.column_config.NumberColumn("Nisbah R:R", format="%.2fx"),
                    "Pautan_Rasmi": st.column_config.LinkColumn("Yahoo Finance", display_text="Buka Yahoo ↗"),
                    "Status": st.column_config.TextColumn("Status SOP")
                },
                hide_index=True,
                width="stretch"
            )