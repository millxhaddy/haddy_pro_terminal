"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL DATA GRID MODEN (WINDOWS 11 FLUENT STYLE)
Lajur Hadapan: Ticker -> Harga -> Trend 30D (Sparkline) -> Julat 52W -> Pautan Rasmi
========================================================================================
"""

import streamlit as st
import pandas as pd

def build_enriched_decision_df(df_base: pd.DataFrame, is_bursa: bool = True) -> pd.DataFrame:
    if df_base is None or df_base.empty:
        return pd.DataFrame()

    df = df_base.copy()
    direct_urls = []

    for _, r in df.iterrows():
        raw_ticker = str(r.get("Ticker", ""))
        clean_sym = raw_ticker.replace("KLSE:", "").replace("NASDAQ:", "").replace("NYSE:", "").strip()
        if is_bursa:
            direct_urls.append(f"https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode={clean_sym}")
        else:
            direct_urls.append(f"https://finance.yahoo.com/quote/{clean_sym}")

    df["Pautan_Rasmi"] = direct_urls
    return df

def render_modern_decision_grid(df_bursa: pd.DataFrame, df_us: pd.DataFrame):
    st.caption("Harga rujukan dan nisbah dipaparkan seperti yang diterima daripada Google Sheets; tiada sparkline atau harga pasaran rekaan.")
    sub_b, sub_u = st.tabs(["🇲🇾 Top 10 Bursa Malaysia (Data Grid Pro)", "🇺🇸 Top 10 Wall Street US (Data Grid Pro)"])

    # 1. Grid Bursa Malaysia
    with sub_b:
        df_b_rich = build_enriched_decision_df(df_bursa, is_bursa=True)
        if not df_b_rich.empty:
            columns = [
                column for column in
                ["Ticker", "Harga_Rujukan", "SL", "TP", "RR", "Status", "Pautan_Rasmi"]
                if column in df_b_rich.columns
            ]
            st.dataframe(
                df_b_rich,
                column_order=columns,
                column_config={
                    "Ticker": st.column_config.TextColumn("Kod Saham", width="small"),
                    "Harga_Rujukan": st.column_config.NumberColumn("Harga Rujukan (MYR)", format="%.2f"),
                    "SL": st.column_config.NumberColumn("Stop Loss", format="RM %.2f"),
                    "TP": st.column_config.NumberColumn("Take Profit", format="RM %.2f"),
                    "RR": st.column_config.NumberColumn("Nisbah R:R", format="%.2fx"),
                    "Pautan_Rasmi": st.column_config.LinkColumn("Profil Bursa", display_text="Buka Profil ↗"),
                    "Status": st.column_config.TextColumn("Status SOP")
                },
                hide_index=True,
                width="stretch"
            )
        else:
            st.info("Tiada rekod keputusan Bursa yang sah dalam snapshot Google Sheets.")

    # 2. Grid Wall Street US
    with sub_u:
        df_u_rich = build_enriched_decision_df(df_us, is_bursa=False)
        if not df_u_rich.empty:
            columns = [
                column for column in
                ["Ticker", "Harga_Rujukan", "SL", "TP", "RR", "Status", "Pautan_Rasmi"]
                if column in df_u_rich.columns
            ]
            st.dataframe(
                df_u_rich,
                column_order=columns,
                column_config={
                    "Ticker": st.column_config.TextColumn("Simbol US", width="small"),
                    "Harga_Rujukan": st.column_config.NumberColumn("Harga Rujukan", format="%.2f"),
                    "SL": st.column_config.NumberColumn("Stop Loss", format="$ %.2f"),
                    "TP": st.column_config.NumberColumn("Take Profit", format="$ %.2f"),
                    "RR": st.column_config.NumberColumn("Nisbah R:R", format="%.2fx"),
                    "Pautan_Rasmi": st.column_config.LinkColumn("Yahoo Finance", display_text="Buka Yahoo ↗"),
                    "Status": st.column_config.TextColumn("Status SOP")
                },
                hide_index=True,
                width="stretch"
            )
        else:
            st.info("Tiada rekod keputusan US yang sah dalam snapshot Google Sheets.")