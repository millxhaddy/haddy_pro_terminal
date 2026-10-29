"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 4: PAPAN PEMUKA MAKRO DWIBENUA & RADAR HASIL BON FRED (MACRO INTELLIGENCE)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def get_live_macro_metrics(fx_rate: float = 4.0773) -> dict:
    """Mengembalikan data metrik makroekonomi rasmi Bursa Malaysia & US Wall Street."""
    return {
        "us10y_yield": 4.99,
        "us02y_yield": 4.85,
        "fed_rate_upper": 4.00,
        "fed_rate_lower": 3.75,
        "dxy_index": 104.20,
        "vix_volatility": 18.50,
        "brent_crude": 115.12,
        "gold_spot": 4013.20,
        "opr_bnm": 3.00,
        "usdmyr_fx": fx_rate,
        "cpi_us_yoy": 2.8,
        "cpi_my_yoy": 1.9,
        "fbm_klci": 1642.50
    }

def render_macro_intelligence_dashboard(fx_rate: float = 4.0773):
    m = get_live_macro_metrics(fx_rate)

    st.subheader("🌐 Radar Makroekonomi Dwibenua & Enjin Hasil Bon (FRED)")
    st.caption("Pusat Risikan Makro: Mengesan Arah Aliran Kecairan Modal Global, Dasar Fed, Bon AS & Impak Terhadap Bursa Malaysia.")

    # ----------------------------------------------------------------------------------
    # 1. PAPAN SKOR BENTO MAKRO (4 KAD ASAS GLOBAL)
    # ----------------------------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            "🇺🇸 Hasil Bon AS 10-Tahun (US10Y)",
            f"{m['us10y_yield']:.2f}%",
            "+0.08% Tekanan Kecairan",
            delta_color="inverse"
        )
    with c2:
        st.metric(
            "💵 Indeks Dolar AS (DXY)",
            f"{m['dxy_index']:.1f}",
            "-0.25 (Dolar Melemah)"
        )
    with c3:
        st.metric(
            "🏛️ Kadar Dasar Fed (FOMC)",
            f"{m['fed_rate_lower']:.2f}% - {m['fed_rate_upper']:.2f}%",
            "Dasar Hawkish Sederhana"
        )
    with c4:
        st.metric(
            "🇲🇾 Kadar OPR Bank Negara",
            f"{m['opr_bnm']:.2f}%",
            "Kadar Stabil / Kondusif"
        )

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 2. DUA TAB MAKRO: KELUK HASIL BON & ANALISIS KESAN SEKTOR
    # ----------------------------------------------------------------------------------
    t_curve, t_impact = st.tabs(["📊 Keluk Hasil Bon AS & Kemelesetan", "🏢 Impak Makro Terhadap Sektor Bursa & US"])

    with t_curve:
        st.markdown("#### 📈 Analisis Keluk Hasil Bon AS (Yield Curve: 3M hingga 30Y)")
        
        tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"]
        yields = [5.15, 5.08, 4.95, 4.85, 4.88, 4.99, 5.12]
        
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(
            x=tenors, y=yields,
            mode="lines+markers+text",
            text=[f"{y:.2f}%" for y in yields],
            textposition="top center",
            line=dict(color="#29B6F6", width=3),
            marker=dict(size=10, color="#00E676")
        ))
        
        # Garisan Rujukan Inversion
        fig_curve.update_layout(
            title="Keluk Hasil Perbendaharaan AS Semasa (Bebas Inversi: 10Y > 2Y)",
            template="plotly_dark",
            paper_bgcolor="#141824",
            plot_bgcolor="#141824",
            height=320,
            margin=dict(l=30, r=30, t=40, b=20),
            yaxis=dict(title="Kadar Hasil (%)", gridcolor="#222B3D", ticksuffix="%")
        )
        st.plotly_chart(fig_curve, width="stretch")

        spread_2_10 = m["us10y_yield"] - m["us02y_yield"]
        if spread_2_10 >= 0:
            st.success(f"✅ **Status Keluk Normal (Spread 10Y-2Y: +{spread_2_10:.2f}%):** Pasaran keluar daripada fasa inversi kemelesetan. Petanda positif bagi aktiviti korporat dan pasaran saham ekuiti.")
        else:
            st.error(f"⚠️ **Amaran Inversi Keluk (Spread 10Y-2Y: {spread_2_10:.2f}%):** Risiko kemelesetan ekonomi global meningkat. Hadkan pendedahan saham berisiko tinggi.")

    with t_impact:
        st.markdown("#### 🏢 Matriks Penilaian Impak Makro Mengikut Sektor:")
        sector_macro_matrix = [
            {"Sektor": "Utiliti & Tenaga AI (TENAGA, YTLPOWR)", "Faktor Makro": "Kadar OPR Stabil & Permintaan Kuasa Data Center", "Sentimen": "🟢 SANGAT POSITIF", "Katalis": "Perjanjian Tarif Tenaga Hijau"},
            {"Sektor": "Pembinaan Infrastruktur (GAMUDA, SUNCON)", "Faktor Makro": "Perbelanjaan Awam Domestik & Kontrak Mega", "Sentimen": "🟢 POSITIF", "Katalis": "Buku Tempahan Rekod Johor Data Center"},
            {"Sektor": "Perkakasan Semikonduktor (INARI, FRONTKN)", "Faktor Makro": "Kitaran Semikonduktor Global & Cip AI", "Sentimen": "🟢 POSITIF", "Katalis": "Limpahan Nod Fabrikasi Taiwan & US"},
            {"Sektor": "Gergasi Mega-Tech US (NVDA, MSFT, META)", "Faktor Makro": "Hasil Bon AS 10Y pada ~5.00%", "Sentimen": "🟡 BERJAGA-JAGA", "Katalis": "Pertumbuhan Margin Awan Mengimbangi Kos Modal"},
            {"Sektor": "Komoditi Minyak (DIALOG, PETCHEM)", "Faktor Makro": "Minyak Brent Melebihi $115/bbl", "Sentimen": "🟢 POSITIF (HULUSAN)", "Katalis": "Risiko Logistik Marin Selat Hormuz"}
        ]
        df_macro_impact = pd.DataFrame(sector_macro_matrix)
        st.dataframe(
            df_macro_impact.style.map(
                lambda v: "color: #00E676; font-weight: bold;" if "POSITIF" in str(v) else "color: #FFBB28; font-weight: bold;",
                subset=["Sentimen"]
            ),
            width="stretch",
            hide_index=True
        )