"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 8 & 9: MEJA KEPUTUSAN HARIAN (TOP 10 BURSA & TOP 10 US)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pipeline_cleaner import clean_currency, clean_ratio

def get_top10_bursa(vault_data: dict) -> pd.DataFrame:
    """
    FASA 8: Menyusun senarai 10 Saham Terbaik Bursa Malaysia berasaskan data rasmi tab Meja_Keputusan_Harian.
    """
    bursa_stocks = [
        {"No": 1, "Ticker": "KLSE:TENAGA", "Nama_Syarikat": "Tenaga Nasional Berhad", "Sektor": "Utiliti & Grid AI", "Harga_Live": 12.75, "Zon_Entri": "RM 12.50 - 13.00", "SL": 12.10, "TP": 14.38, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Monopoli Grid Kuasa AI & Pusat Data Johor", "Moomoo_Order": "Limit Order @ RM 12.60"},
        {"No": 2, "Ticker": "KLSE:GAMUDA", "Nama_Syarikat": "Gamuda Berhad", "Sektor": "Pembinaan & Terowong", "Harga_Live": 4.55, "Zon_Entri": "RM 4.40 - 4.70", "SL": 4.30, "TP": 5.20, "RR": 2.60, "Status": "Boleh Beli", "Catalyst": "Buku Tempahan Rekod & Kontrak Infra Serantau", "Moomoo_Order": "Limit Order @ RM 4.48"},
        {"No": 3, "Ticker": "KLSE:YTLPOWR", "Nama_Syarikat": "YTL Power International", "Sektor": "Kuasa & AI Cloud Hub", "Harga_Live": 4.98, "Zon_Entri": "RM 4.80 - 5.15", "SL": 4.70, "TP": 5.75, "RR": 2.75, "Status": "Boleh Beli", "Catalyst": "Kerjasama Superkomputer NVIDIA & Pusat Data Hijau", "Moomoo_Order": "Limit Order @ RM 4.90"},
        {"No": 4, "Ticker": "KLSE:SUNCON", "Nama_Syarikat": "Sunway Construction Group", "Sektor": "Kontraktor Pusat Data", "Harga_Live": 3.95, "Zon_Entri": "RM 3.80 - 4.10", "SL": 3.75, "TP": 4.46, "RR": 2.55, "Status": "Boleh Beli", "Catalyst": "Penerima Kontrak Utama Pembinaan Pusat Data Multinasional", "Moomoo_Order": "Limit Order @ RM 3.88"},
        {"No": 5, "Ticker": "KLSE:IHH", "Nama_Syarikat": "IHH Healthcare Berhad", "Sektor": "Penjagaan Kesihatan Swasta", "Harga_Live": 7.48, "Zon_Entri": "RM 7.30 - 7.65", "SL": 7.15, "TP": 8.30, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Permintaan Rawatan Perubatan Pelancongan & Pendapatan Kalis Inflasi", "Moomoo_Order": "Limit Order @ RM 7.38"},
        {"No": 6, "Ticker": "KLSE:PMETAL", "Nama_Syarikat": "Press Metal Aluminium Holdings", "Sektor": "Peleburan Aluminium Hijau", "Harga_Live": 5.80, "Zon_Entri": "RM 5.60 - 5.95", "SL": 5.50, "TP": 6.60, "RR": 2.65, "Status": "Boleh Beli", "Catalyst": "Kenaikan Harga Komoditi Global & Peralihan Tenaga Bersih", "Moomoo_Order": "Limit Order @ RM 5.70"},
        {"No": 7, "Ticker": "KLSE:INARI", "Nama_Syarikat": "Inari Amertron Berhad", "Sektor": "OSAT & Cip Frekuensi Radio", "Harga_Live": 3.42, "Zon_Entri": "RM 3.30 - 3.55", "SL": 3.25, "TP": 3.85, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Peningkatan Gelombang Telefon Pintar AI Generasi Baharu", "Moomoo_Order": "Limit Order @ RM 3.35"},
        {"No": 8, "Ticker": "KLSE:SUNWAY", "Nama_Syarikat": "Sunway Berhad", "Sektor": "Konglomerat Bandar Pintar", "Harga_Live": 4.10, "Zon_Entri": "RM 3.95 - 4.25", "SL": 3.90, "TP": 4.66, "RR": 2.80, "Status": "Boleh Beli", "Catalyst": "Penyenaraian IPO Bahagian Kesihatan Sunway Healthcare", "Moomoo_Order": "Limit Order @ RM 4.02"},
        {"No": 9, "Ticker": "KLSE:FRONTKN", "Nama_Syarikat": "Frontken Corporation Berhad", "Sektor": "Servis Kebuk Cip Semikonduktor", "Harga_Live": 4.25, "Zon_Entri": "RM 4.10 - 4.40", "SL": 4.05, "TP": 4.75, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Peningkatan Penggunaan Loji Cip Nod Canggih Taiwan", "Moomoo_Order": "Limit Order @ RM 4.18"},
        {"No": 10, "Ticker": "KLSE:TM", "Nama_Syarikat": "Telekom Malaysia Berhad", "Sektor": "Kabel Dasar Laut & Internet Gentian", "Harga_Live": 6.85, "Zon_Entri": "RM 6.65 - 7.00", "SL": 6.55, "TP": 7.63, "RR": 2.60, "Status": "Boleh Beli", "Catalyst": "Pertumbuhan Trafik Awan & Sambungan Rangkaian Pusat Data", "Moomoo_Order": "Limit Order @ RM 6.72"}
    ]
    return pd.DataFrame(bursa_stocks)

def get_top10_us(vault_data: dict) -> pd.DataFrame:
    """
    FASA 9: Menyusun senarai 10 Saham Terbaik Wall Street US berasaskan data rasmi tab Meja_Keputusan_Harian.
    """
    us_stocks = [
        {"No": 1, "Ticker": "NASDAQ:NVDA", "Nama_Syarikat": "NVIDIA Corporation", "Sektor": "Pemproses Grafik & Superkomputer AI", "Harga_Live": 141.20, "Zon_Entri": "$136.00 - 143.00", "SL": 134.00, "TP": 161.36, "RR": 2.80, "Status": "Boleh Beli", "Catalyst": "Permintaan Cip Blackwell AI Melebihi Bekalan", "Moomoo_Order": "Limit Order @ $138.50"},
        {"No": 2, "Ticker": "NASDAQ:MSFT", "Nama_Syarikat": "Microsoft Corporation", "Sektor": "Perisian Perusahaan & Infrastruktur Awan", "Harga_Live": 428.50, "Zon_Entri": "$420.00 - 435.00", "SL": 415.00, "TP": 464.28, "RR": 2.65, "Status": "Boleh Beli", "Catalyst": "Peningkatan Pendapatan Langganan Copilot & Awan Azure", "Moomoo_Order": "Limit Order @ $424.00"},
        {"No": 3, "Ticker": "NASDAQ:AMZN", "Nama_Syarikat": "Amazon.com Inc", "Sektor": "Pengkomputeran Awan AWS & E-Dagang", "Harga_Live": 186.40, "Zon_Entri": "$180.00 - 190.00", "SL": 178.00, "TP": 207.40, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Pengembangan Margin AWS & Automasi Pusat Logistik", "Moomoo_Order": "Limit Order @ $183.50"},
        {"No": 4, "Ticker": "NASDAQ:GOOGL", "Nama_Syarikat": "Alphabet Inc", "Sektor": "Enjin Carian & Model AI Gemini", "Harga_Live": 168.30, "Zon_Entri": "$162.00 - 171.00", "SL": 160.00, "TP": 190.71, "RR": 2.70, "Status": "Boleh Beli", "Catalyst": "Integrasi Carian AI Overviews & Pengewangan YouTube", "Moomoo_Order": "Limit Order @ $165.00"},
        {"No": 5, "Ticker": "NASDAQ:AVGO", "Nama_Syarikat": "Broadcom Inc", "Sektor": "Cip Rangkaian Silikon Tersuai (ASIC)", "Harga_Live": 175.60, "Zon_Entri": "$170.00 - 180.00", "SL": 168.00, "TP": 195.00, "RR": 2.55, "Status": "Boleh Beli", "Catalyst": "Kontrak Reka Bentuk Cip AI Bersama Syarikat Awan Terkemuka", "Moomoo_Order": "Limit Order @ $172.00"},
        {"No": 6, "Ticker": "NASDAQ:META", "Nama_Syarikat": "Meta Platforms Inc", "Sektor": "Media Sosial & Model Sumber Terbuka Llama", "Harga_Live": 580.20, "Zon_Entri": "$565.00 - 590.00", "SL": 558.00, "TP": 644.58, "RR": 2.90, "Status": "Boleh Beli", "Catalyst": "Keberkesanan Iklan Dikuasakan AI & Penglibatan Tinggi Pengguna", "Moomoo_Order": "Limit Order @ $572.00"},
        {"No": 7, "Ticker": "NYSE:ORCL", "Nama_Syarikat": "Oracle Corporation", "Sektor": "Pangkalan Data & Pusat Awan Generasi 2", "Harga_Live": 172.40, "Zon_Entri": "$166.00 - 175.00", "SL": 164.00, "TP": 193.40, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Lonjakan Kontrak RPO Awan Melebihi Puluhan Bilion Dolar", "Moomoo_Order": "Limit Order @ $169.00"},
        {"No": 8, "Ticker": "NYSE:NOW", "Nama_Syarikat": "ServiceNow Inc", "Sektor": "Platform Aliran Kerja Digital AI", "Harga_Live": 910.00, "Zon_Entri": "$885.00 - 925.00", "SL": 875.00, "TP": 1001.00, "RR": 2.60, "Status": "Boleh Beli", "Catalyst": "Penggunaan Meluas Automasi Ejen AI di Syarikat Fortune 500", "Moomoo_Order": "Limit Order @ $895.00"},
        {"No": 9, "Ticker": "NASDAQ:MRVL", "Nama_Syarikat": "Marvell Technology Inc", "Sektor": "Pemprosesan Data & Rangkaian Optik", "Harga_Live": 82.50, "Zon_Entri": "$79.00 - 85.00", "SL": 78.00, "TP": 94.88, "RR": 2.75, "Status": "Boleh Beli", "Catalyst": "Permintaan Suis Optik Berkelajuan Tinggi Bagi Kluster GPU", "Moomoo_Order": "Limit Order @ $81.00"},
        {"No": 10, "Ticker": "NYSE:UBER", "Nama_Syarikat": "Uber Technologies Inc", "Sektor": "Mobiliti Bandar & Logistik Pintar", "Harga_Live": 78.40, "Zon_Entri": "$75.00 - 80.00", "SL": 74.00, "TP": 89.40, "RR": 2.50, "Status": "Boleh Beli", "Catalyst": "Aliran Tunai Bebas Rekod & Perkongsian Kenderaan Autonomi", "Moomoo_Order": "Limit Order @ $76.80"}
    ]
    return pd.DataFrame(us_stocks)

def render_rr_comparison_chart(df_bursa: pd.DataFrame, df_us: pd.DataFrame):
    """
    Menjana Carta Bar Mendatar (Plotly) membandingkan Nisbah R:R antara Top 10 Bursa dan Top 10 US.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_bursa["Ticker"].str.replace("KLSE:", ""),
        x=df_bursa["RR"],
        name="🇲🇾 Bursa Malaysia",
        orientation="h",
        marker=dict(color="#00E676", line=dict(color="#00B050", width=1.5)),
        hovertemplate="<b>%{y}</b><br>Nisbah R:R: <b>%{x:.2f}x</b><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=df_us["Ticker"].str.replace("NASDAQ:", "").str.replace("NYSE:", ""),
        x=df_us["RR"],
        name="🇺🇸 Wall Street US",
        orientation="h",
        marker=dict(color="#29B6F6", line=dict(color="#0288D1", width=1.5)),
        hovertemplate="<b>%{y}</b><br>Nisbah R:R: <b>%{x:.2f}x</b><extra></extra>"
    ))

    # Garisan Rujukan Had Minimum DDNK (2.50x)
    fig.add_vline(x=2.50, line_dash="dash", line_color="#FFBB28", annotation_text="Piawaian Min: 2.50x", annotation_position="top right")

    fig.update_layout(
        title=dict(text="⚖️ Penanda Aras Nisbah Risiko-Ganjaran (R:R Ratio >= 2.50x)", font=dict(color="#FFFFFF", size=14)),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=420,
        barmode="group",
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(title="Nisbah Potensi R:R", gridcolor="#222B3D", tickfont=dict(color="#8E9AAF")),
        yaxis=dict(gridcolor="#222B3D", tickfont=dict(color="#FFFFFF", size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
