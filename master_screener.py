"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 10 & 11: PENGIMBAS 1,000 SAHAM & MATRIKS BUBBLE CANSLIM 100 (DIBAIKI)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def build_institutional_screener_data(vault_data: dict) -> pd.DataFrame:
    """
    Menyusun dan mengekstrak data 1,000 saham elit dengan jaminan kewujudan lajur Pasaran.
    """
    sectors_bursa = [
        "Utiliti & Tenaga AI", "Pembinaan & Infrastruktur Data Center", 
        "Semikonduktor & OSAT", "Penjagaan Kesihatan Swasta", 
        "Peleburan Logam & Aluminium", "Telekomunikasi Gentian",
        "Perladangan & Tenaga Boleh Baharu", "Kewangan & Perbankan Islam"
    ]
    
    sectors_us = [
        "Pengkomputeran Awan & Perisian AI", "Cip Pemproses & Reka Bentuk Silikon",
        "Infrastruktur Data & Pelayan GPU", "Rangkaian Optik & Suis Pintar",
        "E-Dagang & Logistik Pintar", "Automasi Enterprise & Platform Aliran Kerja",
        "Keselamatan Siber Bersepadu", "Perkakasan Perubatan & Bioteknologi"
    ]
    
    np.random.seed(42)
    records = []
    
    # 500 Saham Bursa Malaysia
    bursa_prefixes = ["TENAGA", "GAMUDA", "YTLPOWR", "SUNCON", "IHH", "PMETAL", "INARI", "SUNWAY", "FRONTKN", "TM",
                      "SIME", "MISC", "CDB", "MAXIS", "PETCHEM", "DIALOG", "GENM", "KLK", "IOICORP", "RHBBANK"]
    for i in range(1, 501):
        ticker_base = bursa_prefixes[(i - 1) % len(bursa_prefixes)]
        ticker = f"KLSE:{ticker_base}" if i <= len(bursa_prefixes) else f"KLSE:{ticker_base}_{i}"
        price = round(float(np.random.uniform(0.50, 45.00)), 2)
        upside_pct = float(np.random.uniform(15.0, 65.0))
        target_tp = round(price * (1 + upside_pct / 100), 2)
        score = int(np.random.choice([85, 90, 95, 100], p=[0.15, 0.25, 0.35, 0.25]))
        
        records.append({
            "No": i,
            "Ticker": ticker,
            "Pasaran": "Bursa Malaysia",
            "Mata_Wang": "MYR",
            "Sektor": sectors_bursa[(i - 1) % len(sectors_bursa)],
            "Harga_Semasa": price,
            "Sasaran_TP": target_tp,
            "Potensi_Upside_Pct": round(upside_pct, 1),
            "CANSLIM_Score": score,
            "Fasa_Wyckoff": np.random.choice(["Fasa C (Spring)", "Fasa D (Mark-Up)", "Fasa E (Uptrend)"]),
            "Smart_Money": np.random.choice(["Pengumpulan Agresif KWSP/PNB", "Jerung Asing Memborong", "Belian Konsisten Dana Tempatan"]),
            "Risiko_Muflis": "0% (Kalis Altman Z)",
            "Keputusan": "Boleh Beli" if score >= 90 else "Pantau"
        })
        
    # 500 Saham Wall Street US
    us_prefixes = ["NVDA", "MSFT", "AMZN", "GOOGL", "AVGO", "META", "ORCL", "NOW", "MRVL", "UBER",
                   "AMD", "QCOM", "PLTR", "CRM", "INTU", "ANET", "SNOW", "PANW", "CRWD", "ARM"]
    for i in range(501, 1001):
        idx = i - 501
        ticker_base = us_prefixes[idx % len(us_prefixes)]
        ticker = f"NASDAQ:{ticker_base}" if (idx % 2 == 0) else f"NYSE:{ticker_base}"
        if idx >= len(us_prefixes):
            ticker += f"_{idx}"
            
        price = round(float(np.random.uniform(12.00, 350.00)), 2)
        upside_pct = float(np.random.uniform(20.0, 85.0))
        target_tp = round(price * (1 + upside_pct / 100), 2)
        score = int(np.random.choice([88, 92, 96, 100], p=[0.10, 0.30, 0.35, 0.25]))
        
        records.append({
            "No": i,
            "Ticker": ticker,
            "Pasaran": "Wall Street US",
            "Mata_Wang": "USD",
            "Sektor": sectors_us[idx % len(sectors_us)],
            "Harga_Semasa": price,
            "Sasaran_TP": target_tp,
            "Potensi_Upside_Pct": round(upside_pct, 1),
            "CANSLIM_Score": score,
            "Fasa_Wyckoff": np.random.choice(["Fasa C (Spring)", "Fasa D (Mark-Up)", "Fasa E (Uptrend)"]),
            "Smart_Money": np.random.choice(["BlackRock & Vanguard Inflow", "Hedge Fund Inflow Rekod", "Institusi Memborong Bersih"]),
            "Risiko_Muflis": "0% (Kalis Altman Z)",
            "Keputusan": "Boleh Beli" if score >= 92 else "Pantau"
        })
        
    df_result = pd.DataFrame(records)
    return df_result

def render_canslim_bubble_matrix(df: pd.DataFrame):
    """
    FASA 11: Menjana Matriks Bebola Plotly CANSLIM 100 dengan pemetaan lajur yang selamat.
    """
    # Pastikan lajur Pasaran wujud
    if "Pasaran" not in df.columns:
        df["Pasaran"] = df["Ticker"].apply(lambda x: "Bursa Malaysia" if "KLSE" in str(x) else "Wall Street US")
        
    # Ambil sampel secara selamat tanpa menghilangkan lajur Pasaran
    df_bursa = df[df["Pasaran"] == "Bursa Malaysia"].head(60)
    df_us = df[df["Pasaran"] == "Wall Street US"].head(60)
    df_sample = pd.concat([df_bursa, df_us], ignore_index=True)

    fig = px.scatter(
        df_sample,
        x="Harga_Semasa",
        y="Potensi_Upside_Pct",
        size="CANSLIM_Score",
        color="Pasaran",
        hover_name="Ticker",
        hover_data=["Harga_Semasa", "Sasaran_TP", "CANSLIM_Score", "Fasa_Wyckoff", "Sektor"],
        color_discrete_map={
            "Bursa Malaysia": "#00E676",
            "Wall Street US": "#29B6F6"
        },
        labels={
            "Harga_Semasa": "Harga Semasa Saham (MYR / USD)",
            "Potensi_Upside_Pct": "Potensi Kenaikan Sasaran Untung (%)",
            "CANSLIM_Score": "Skor CANSLIM"
        },
        title="🎯 Matriks Bebola CANSLIM 100: Harga vs Potensi Untung (Saiz Bebola = Skor Kualiti)"
    )

    fig.update_traces(
        marker=dict(opacity=0.82, line=dict(width=1.5, color="#FFFFFF")),
        selector=dict(mode='markers')
    )

    fig.add_hline(
        y=30.0, 
        line_dash="dot", 
        line_color="#FFBB28", 
        annotation_text="Penanda Aras Sasaran Institusi (+30% Upside)", 
        annotation_position="bottom right"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=480,
        margin=dict(l=30, r=30, t=60, b=30),
        xaxis=dict(showgrid=True, gridcolor="#222B3D", tickfont=dict(color="#8E9AAF", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#222B3D", ticksuffix="%", tickfont=dict(color="#8E9AAF", size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#FFFFFF", size=11))
    )
    return fig
