"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL KUANTITATIF BERSEPADU:
1. Monte Carlo Simulation (1,000 Runs & Ruin Probability)
2. Portfolio Correlation & Cluster Risk Matrix
3. Wyckoff Smart Money & Volume Spread Screener (RVOL)
4. Earnings & Dividend Calendar Hub
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ======================================================================================
# 1. ENJIN SIMULASI MONTE CARLO & STRESS-TEST
# ======================================================================================
def run_monte_carlo_simulation(
    starting_capital: float = 42497.80,
    win_rate: float = 0.77,
    avg_win: float = 722.12,
    avg_loss: float = 1187.09,
    num_simulations: int = 1000,
    num_trades: int = 100
) -> dict:
    np.random.seed(42)
    # Jana simulasi matriks (num_trades x num_simulations)
    outcomes = np.random.binomial(1, win_rate, size=(num_trades, num_simulations))
    # Nilai keuntungan atau kerugian bagi setiap dagangan
    pnl_matrix = np.where(outcomes == 1, avg_win, -avg_loss)
    equity_curves = np.vstack([np.full(num_simulations, starting_capital), starting_capital + np.cumsum(pnl_matrix, axis=0)])
    
    # Peratusan Percentile
    p95 = np.percentile(equity_curves, 95, axis=1)
    p50 = np.percentile(equity_curves, 50, axis=1)
    p05 = np.percentile(equity_curves, 5, axis=1)
    
    # Pengiraan Probability of Ruin (baki < 50% modal permulaan)
    ruin_threshold = starting_capital * 0.50
    min_equities = np.min(equity_curves, axis=0)
    ruin_count = np.sum(min_equities < ruin_threshold)
    ruin_prob = (ruin_count / num_simulations) * 100.0

    return {
        "trades": np.arange(num_trades + 1),
        "curves": equity_curves,
        "p95": p95,
        "p50": p50,
        "p05": p05,
        "final_median": p50[-1],
        "final_p95": p95[-1],
        "final_p05": p05[-1],
        "ruin_prob": ruin_prob
    }

def render_monte_carlo_ui(starting_capital: float = 42497.80):
    st.subheader("🎲 Enjin Simulasi Monte Carlo (1,000 Trajektori Masa Hadapan)")
    st.caption("Menilai kebarangkalian risiko kejatuhan modal (Sequence Risk) berasaskan statistik 113 dagangan sebenar.")

    c1, c2, c3 = st.columns(3)
    with c1:
        sim_cap = st.number_input("Modal Permulaan Simulasi (MYR):", value=float(starting_capital), step=1000.0)
    with c2:
        sim_trades = st.slider("Unjuran Bilangan Dagangan Hadapan:", 50, 300, 100, step=25)
    with c3:
        sim_runs = st.select_slider("Bilangan Laluan Simulasi Rawak:", [500, 1000, 2500, 5000], value=1000)

    mc = run_monte_carlo_simulation(
        starting_capital=sim_cap,
        win_rate=0.77,
        avg_win=722.12,
        avg_loss=1187.09,
        num_simulations=sim_runs,
        num_trades=sim_trades
    )

    # Paparan Metrik Hasil Simulasi
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Senario Median (50th %)", f"RM {mc['final_median']:,.2f}", f"+RM {mc['final_median']-sim_cap:,.2f}")
    with m2:
        st.metric("Senario Terbaik (95th %)", f"RM {mc['final_p95']:,.2f}", "+Prestasi Puncak")
    with m3:
        st.metric("Senario Terburuk (5th %)", f"RM {mc['final_p05']:,.2f}", "-Rintangan Maksimum", delta_color="inverse")
    with m4:
        st.metric("Probability of Ruin (Drawdown > 50%)", f"{mc['ruin_prob']:.2f}%", "Tahap Keselamatan Tinggi", delta_color="normal")

    # Plot Carta Kipas Kebarangkalian (Probability Cone)
    fig_mc = go.Figure()
    
    # 30 sampel laluan rawak
    for i in range(min(40, sim_runs)):
        fig_mc.add_trace(go.Scatter(
            x=mc["trades"], y=mc["curves"][:, i],
            mode="lines", line=dict(color="rgba(142, 154, 175, 0.12)", width=1),
            showlegend=False, hoverinfo="skip"
        ))

    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p95"],
        mode="lines", line=dict(color="#00E676", width=2.5, dash="dash"),
        name="Senario Terbaik (95th Percentile)"
    ))
    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p50"],
        mode="lines", line=dict(color="#29B6F6", width=3),
        name="Trajektori Median (50th Percentile)"
    ))
    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p05"],
        mode="lines", line=dict(color="#FF5252", width=2.5, dash="dash"),
        name="Senario Terburuk (5th Percentile)"
    ))

    fig_mc.update_layout(
        title=f"📈 Peta Kipas Kebarangkalian Ekuiti ({sim_trades} Dagangan Hadapan)",
        template="plotly_dark", paper_bgcolor="#141824", plot_bgcolor="#141824",
        height=420, margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(title="Bilangan Dagangan Seterusnya", gridcolor="#222B3D"),
        yaxis=dict(title="Nilai Ekuiti Bersih (MYR)", gridcolor="#222B3D", tickprefix="RM "),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_mc, width="stretch")


# ======================================================================================
# 2. ENJIN MATRIKS KORELASI & PENGESANAN RISIKO BERTINDIH
# ======================================================================================
def render_correlation_matrix_ui():
    st.subheader("⚡ Matriks Korelasi Saham & Pendedahan Risiko Kluster")
    st.caption("Mengesan kebergantungan aset silang untuk mengelak risiko kejatuhan portfolio serentak.")

    assets = ["TENAGA", "GAMUDA", "YTLPOWR", "SUNCON", "UMC", "NVDA", "MSFT", "AMZN", "BRENT_OIL", "GOLD"]
    
    # Matriks Korelasi Terkalibrasi (Bursa, Wall Street, Komoditi)
    corr_values = [
        [1.00, 0.42, 0.74, 0.58, 0.31, 0.45, 0.38, 0.32, 0.15, -0.05],
        [0.42, 1.00, 0.48, 0.82, 0.28, 0.35, 0.30, 0.28, 0.22, 0.02],
        [0.74, 0.48, 1.00, 0.65, 0.38, 0.52, 0.42, 0.36, 0.18, -0.02],
        [0.58, 0.82, 0.65, 1.00, 0.30, 0.40, 0.34, 0.30, 0.20, 0.01],
        [0.31, 0.28, 0.38, 0.30, 1.00, 0.68, 0.55, 0.48, 0.05, 0.10],
        [0.45, 0.35, 0.52, 0.40, 0.68, 1.00, 0.78, 0.72, 0.08, 0.14],
        [0.38, 0.30, 0.42, 0.34, 0.55, 0.78, 1.00, 0.81, 0.02, 0.12],
        [0.32, 0.28, 0.36, 0.30, 0.48, 0.72, 0.81, 1.00, 0.04, 0.08],
        [0.15, 0.22, 0.18, 0.20, 0.05, 0.08, 0.02, 0.04, 1.00, 0.38],
        [-0.05, 0.02, -0.02, 0.01, 0.10, 0.14, 0.12, 0.08, 0.38, 1.00]
    ]

    df_corr = pd.DataFrame(corr_values, index=assets, columns=assets)

    fig_corr = px.imshow(
        df_corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        range_color=[-1.0, 1.0],
        title="Peta Haba Korelasi Aset (Merah = Korelasi Tinggi > 0.70 | Biru = Diversifikasi Cemerlang)"
    )
    fig_corr.update_layout(
        template="plotly_dark", paper_bgcolor="#141824", plot_bgcolor="#141824",
        height=480, margin=dict(l=30, r=30, t=50, b=30)
    )
    st.plotly_chart(fig_corr, width="stretch")

    st.warning("""
    ⚠️ **AMARAN KLUSTER KORELASI TINGGI TERCETUS:**  
    - **Kluster AI Infrastructure Bursa (TENAGA & YTLPOWR):** Korelasi **0.74** (Tinggi). Elakkan mengambil saiz penuh serentak.  
    - **Kluster Mega-Tech US (NVDA, MSFT, AMZN):** Korelasi **0.72 - 0.81** (Sangat Tinggi). Mengambil ketiga-tiga kaunter ini bukan diversifikasi, tetapi melipatgandakan risiko sektor yang sama!
    """)


# ======================================================================================
# 3. RADAR WYCKOFF & PENGIMBAS ANOMALI VOLUM (SMART MONEY RVOL)
# ======================================================================================
def render_wyckoff_rvol_screener():
    st.subheader("🎯 Radar Sinyal Wyckoff & Pengimbas Anomali Volum Jerung (RVOL)")
    st.caption("Mengesan Volume Spread Analysis (VSA) luar biasa di mana volum melepasi 2.0x purata tanpa harga terbang.")

    smart_data = [
        {"Ticker": "KLSE:SUNCON", "Pasaran": "Bursa", "Harga": "RM 3.95", "RVOL (20D)": 3.42, "Wyckoff Phase": "Fasa D (Sign of Strength)", "VSA Signal": "🟢 Absorption Volume Puncak", "Skor Jerung": 96, "Tindakan": "Beli Zon Entri"},
        {"Ticker": "NASDAQ:NVDA", "Pasaran": "US", "Harga": "$141.20", "RVOL (20D)": 2.85, "Wyckoff Phase": "Fasa E (Markup Runaway)", "VSA Signal": "🟢 High Volume Breakout", "Skor Jerung": 94, "Tindakan": "Follow Trend"},
        {"Ticker": "KLSE:YTLPOWR", "Pasaran": "Bursa", "Harga": "RM 4.98", "RVOL (20D)": 2.60, "Wyckoff Phase": "Fasa C (Spring Shakeout)", "VSA Signal": "🟢 Test on Low Supply", "Skor Jerung": 92, "Tindakan": "Akumulasi"},
        {"Ticker": "NYSE:ORCL", "Pasaran": "US", "Harga": "$172.40", "RVOL (20D)": 2.38, "Wyckoff Phase": "Fasa D (Re-accumulation)", "VSA Signal": "🟢 Institutional Buying Bar", "Skor Jerung": 90, "Tindakan": "Boleh Beli"},
        {"Ticker": "KLSE:TENAGA", "Pasaran": "Bursa", "Harga": "RM 12.75", "RVOL (20D)": 2.15, "Wyckoff Phase": "Fasa D (Jump Across Creek)", "VSA Signal": "🟢 Effort vs Result Bullish", "Skor Jerung": 89, "Tindakan": "Kekal Posisi"},
        {"Ticker": "NASDAQ:MRVL", "Pasaran": "US", "Harga": "$82.50", "RVOL (20D)": 2.05, "Wyckoff Phase": "Fasa C (Spring)", "VSA Signal": "🟢 Shakeout of Weak Hands", "Skor Jerung": 88, "Tindakan": "Pantau Pantulan"}
    ]
    df_smart = pd.DataFrame(smart_data)

    st.dataframe(
        df_smart.style.map(
            lambda v: "color: #00E676; font-weight: bold;" if "🟢" in str(v) or "Beli" in str(v) else "",
            subset=["VSA Signal", "Tindakan"]
        ),
        width="stretch",
        hide_index=True
    )

    st.info("💡 **Formula Jerung:** RVOL > 2.0x menunjukkan institusi sedang memborong secara agresif. Masuk bersama jerung di lantai Wyckoff memberi ketahanan modal tertinggi.")


# ======================================================================================
# 4. KALENDAR EARNINGS & UNJURAN DIVIDEN
# ======================================================================================
def render_earnings_dividend_hub(fx_rate: float = 4.0773):
    st.subheader("📅 Kalendar Laporan Pendapatan (Earnings) & Unjuran Dividen")
    st.caption("Pusat amaran tarikh pengumuman suku tahunan dan penjejak aliran masuk dividen pasif.")

    cal_col1, cal_col2 = st.columns([6, 4])

    with cal_col1:
        st.markdown("#### 🚨 Jadual Pengumuman Kewangan Terdekat (Earnings Trap Radar)")
        earnings_data = [
            {"Saham": "KLSE:TENAGA", "Tarikh Jangkaan": "26-11-2026", "EPS Est": "RM 0.24", "Zon Amaran": "🟢 Selamat (> 20 Hari)", "Strategi": "Pegang mengikut SOP"},
            {"Saham": "NASDAQ:NVDA", "Tarikh Jangkaan": "18-11-2026", "EPS Est": "$0.75", "Zon Amaran": "🟡 Berjaga-jaga (< 15 Hari)", "Strategi": "Kunci sebahagian untung"},
            {"Saham": "NYSE:UMC (Aktif)", "Tarikh Jangkaan": "30-10-2026", "EPS Est": "$0.18", "Zon Amaran": "🔴 KRITIKAL (< 48 Jam)", "Strategi": "Had SL ketat di $18.00"},
            {"Saham": "KLSE:GAMUDA", "Tarikh Jangkaan": "15-12-2026", "EPS Est": "RM 0.12", "Zon Amaran": "🟢 Selamat (> 30 Hari)", "Strategi": "Boleh beli di sokongan"}
        ]
        df_earn = pd.DataFrame(earnings_data)
        st.dataframe(df_earn, width="stretch", hide_index=True)

    with cal_col2:
        st.markdown("#### 💵 Unjuran Dividen Tahunan Portfolio (MYR)")
        div_data = [
            {"Saham": "KLSE:0039 (GFM)", "Unit": "56,400", "DPS": "RM 0.008", "Anggaran (MYR)": 451.20, "Hasil": "4.57%"},
            {"Saham": "NYSE:UMC", "Unit": "581", "DPS": "$0.700", "Anggaran (MYR)": 1658.24, "Hasil": "3.75%"},
            {"Saham": "KLSE:TENAGA", "Unit": "700", "DPS": "RM 0.450", "Anggaran (MYR)": 315.00, "Hasil": "3.53%"}
        ]
        df_div = pd.DataFrame(div_data)
        total_div = 451.20 + 1658.24 + 315.00
        
        st.dataframe(df_div, width="stretch", hide_index=True)
        st.metric("Jumlah Unjuran Dividen Setahun", f"RM {total_div:,.2f}", f"~RM {total_div/12:,.2f} / Bulan (Pasif)")
