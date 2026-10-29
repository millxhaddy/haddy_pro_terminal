"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 14, 15 & 16: MULTIMEDIA VIDEO, RADAR MAKRO FOMC & TOLOK GEOPOLITIK
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Senarai Saluran Suapan Video Pasaran Antarabangsa
LIVE_STREAMS = {
    "Analisis Pasaran Global (Yahoo Finance Live)": "https://www.youtube.com/watch?v=WPqXO_JqH_o",
    "Suapan Pasaran & Kewangan Dunia (DW Business / CNBC Focus)": "https://www.youtube.com/watch?v=V0I_3TEns3g",
    "Liputan Pasaran Semikonduktor & AI Terkini": "https://www.youtube.com/watch?v=k1D_mGf00g4"
}

def get_macro_intelligence_data(vault_data: dict) -> dict:
    """
    FASA 15: Menyusun data risikan makro daripada tab Radar_Makro_&_Berita_Live.
    """
    fomc_events = [
        {"Masa": "16:30 MYT", "Peristiwa": "Keputusan Dasar FOMC Fed", "Butiran": "Kadar faedah sasaran dijangka kekal pada 3.75% - 4.00%. Pendirian berhati-hati terhadap inflasi.", "Impak": "🔴 Hawkish"},
        {"Masa": "15:00 MYT", "Peristiwa": "Hasil Bon AS 10-Tahun", "Butiran": "Mencecah 4.99% mencerminkan tekanan kecairan global dan pengukuhan Dolar AS.", "Impak": "🟡 Ketat"},
        {"Masa": "14:15 MYT", "Peristiwa": "Indeks Inflasi Teras PCE", "Butiran": "Pertumbuhan tahunan 2.8% mengehadkan ruang penurunan kadar faedah agresif.", "Impak": "🟡 Stabil"}
    ]
    
    geopolitical_events = [
        {"Masa": "16:00 MYT", "Kawasan": "Selat Hormuz / Teluk Parsi", "Peristiwa": "Kawalan ketat laluan kapal tangki minyak meningkatkan premium risiko logistik.", "Risiko": "🔴 Kritikal"},
        {"Masa": "14:45 MYT", "Kawasan": "Pasaran Tenaga Eropah", "Peristiwa": "Permintaan gas asli melonjak susulan kebimbangan gangguan bekalan musim sejuk.", "Risiko": "🟡 Sederhana"},
        {"Masa": "11:30 MYT", "Kawasan": "Perdagangan Selat Melaka", "Peristiwa": "Trafik kargo kontena meningkat 12% menyokong pendapatan sektor pelabuhan Bursa.", "Risiko": "🟢 Positif"}
    ]
    
    corporate_news = [
        {"Masa": "16:15 MYT", "Syarikat": "Tenaga Nasional Berhad", "Pengumuman": "Memeterai perjanjian bekalan kuasa elektrik fasa kedua AI Data Center Johor bernilai tinggi.", "Kategori": "🟢 Bullish AI"},
        {"Masa": "15:30 MYT", "Syarikat": "Gamuda Berhad", "Pengumuman": "Buku tempahan pembinaan serantau melepasi rekod RM 32 Bilion.", "Kategori": "🟢 Rekod Kontrak"},
        {"Masa": "13:20 MYT", "Syarikat": "YTL Power International", "Pengumuman": "Penempatan kluster GPU NVIDIA Blackwell pertama di hab kuasa hijau Kulai berjalan lancar.", "Kategori": "🟢 Pemangkin AI"}
    ]
    
    return {
        "fomc": pd.DataFrame(fomc_events),
        "geopolitics": pd.DataFrame(geopolitical_events),
        "corporate": pd.DataFrame(corporate_news)
    }

def render_geopolitical_gauges():
    """
    FASA 16: Menjana 3 Tolok Interaktif Separuh Bulatan (Plotly Half-Donut Gauges)
    untuk Minyak Mentah Brent, Volatiliti VIX, dan Emas Safe-Haven.
    """
    fig = go.Figure()

    # 1. Tolok Minyak Mentah Brent ($/bbl)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=115.12,
        delta={'reference': 95.0, 'position': "top", 'prefix': "+$"},
        title={'text': "<b>Minyak Brent ($/bbl)</b><br><span style='font-size:0.75rem;color:#FF5252;'>Risiko Perang & Selat Hormuz</span>", 'font': {'size': 13, 'color': '#FFFFFF'}},
        domain={'x': [0.0, 0.31], 'y': [0, 1]},
        gauge={
            'axis': {'range': [50, 150], 'tickcolor': "#8E9AAF", 'ticksuffix': "$"},
            'bar': {'color': "#FF5252", 'thickness': 0.35},
            'bgcolor': "#1A1F2C",
            'steps': [
                {'range': [50, 80], 'color': "rgba(0, 230, 118, 0.25)"},
                {'range': [80, 105], 'color': "rgba(255, 187, 40, 0.25)"},
                {'range': [105, 150], 'color': "rgba(255, 82, 82, 0.45)"}
            ],
            'threshold': {'line': {'color': "#FF1744", 'width': 3}, 'thickness': 0.8, 'value': 120}
        }
    ))

    # 2. Tolok Indeks Ketakutan Volatiliti (VIX)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=18.50,
        delta={'reference': 25.0, 'position': "top", 'prefix': "Zon: "},
        title={'text': "<b>Indeks Volatiliti (VIX)</b><br><span style='font-size:0.75rem;color:#00E676;'>Sentimen Pasaran Sederhana</span>", 'font': {'size': 13, 'color': '#FFFFFF'}},
        domain={'x': [0.34, 0.65], 'y': [0, 1]},
        gauge={
            'axis': {'range': [10, 50], 'tickcolor': "#8E9AAF"},
            'bar': {'color': "#00E676", 'thickness': 0.35},
            'bgcolor': "#1A1F2C",
            'steps': [
                {'range': [10, 20], 'color': "rgba(0, 230, 118, 0.35)"},
                {'range': [20, 30], 'color': "rgba(255, 187, 40, 0.35)"},
                {'range': [30, 50], 'color': "rgba(255, 82, 82, 0.55)"}
            ],
            'threshold': {'line': {'color': "#FF1744", 'width': 3}, 'thickness': 0.8, 'value': 30}
        }
    ))

    # 3. Tolok Emas Fizikal Safe-Haven ($/oz)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=4013.20,
        delta={'reference': 3650.0, 'position': "top", 'prefix': "+$"},
        title={'text': "<b>Emas Spot ($/oz)</b><br><span style='font-size:0.75rem;color:#FFD700;'>Lindung Nilai Inflasi Rekod</span>", 'font': {'size': 13, 'color': '#FFFFFF'}},
        domain={'x': [0.68, 1.0], 'y': [0, 1]},
        gauge={
            'axis': {'range': [2500, 4500], 'tickcolor': "#8E9AAF", 'ticksuffix': "$"},
            'bar': {'color': "#FFD700", 'thickness': 0.35},
            'bgcolor': "#1A1F2C",
            'steps': [
                {'range': [2500, 3200], 'color': "rgba(255, 215, 0, 0.15)"},
                {'range': [3200, 3800], 'color': "rgba(255, 215, 0, 0.35)"},
                {'range': [3800, 4500], 'color': "rgba(255, 215, 0, 0.55)"}
            ],
            'threshold': {'line': {'color': "#00E676", 'width': 3}, 'thickness': 0.8, 'value': 4000}
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=260,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    return fig
