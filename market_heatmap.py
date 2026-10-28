"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PETA HABA PASARAN (MARKET HEATMAP) & JALUR SEBUT HARGA BERJALAN (TICKER TAPE)
Visualisasi Gaya TradingView & Finviz (Plotly Treemap & CSS Marquee Engine)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_ticker_tape_marquee():
    """
    Menjana Jalur Sebut Harga Berjalan (Ticker Tape) ala Bloomberg Terminal di atas halaman.
    """
    st.markdown("""
    <style>
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #10141D 0%, #1A2232 50%, #10141D 100%);
            border-top: 1px solid #2B384E;
            border-bottom: 1px solid #2B384E;
            padding: 8px 0;
            white-space: nowrap;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
            margin-bottom: 15px;
        }
        .ticker-move {
            display: inline-block;
            white-space: nowrap;
            animation: ticker 35s linear infinite;
        }
        .ticker-move:hover {
            animation-play-state: paused;
        }
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-50%, 0, 0); }
        }
        .ticker-item {
            display: inline-block;
            padding: 0 16px;
            font-size: 0.85rem;
            font-family: 'Consolas', 'Courier New', monospace;
            font-weight: 700;
        }
        .t-green { color: #00E676; }
        .t-red { color: #FF5252; }
        .t-blue { color: #29B6F6; }
        .t-yellow { color: #FFD700; }
    </style>

    <div class="ticker-wrap">
        <div class="ticker-move">
            <span class="ticker-item">🇲🇾 FBM KLCI: <span class="t-green">1,642.50 ▲ +0.45%</span></span>
            <span class="ticker-item">🇺🇸 S&P 500: <span class="t-green">5,864.20 ▲ +0.72%</span></span>
            <span class="ticker-item">🇺🇸 NASDAQ: <span class="t-green">18,518.60 ▲ +0.95%</span></span>
            <span class="ticker-item">💱 USD/MYR: <span class="t-blue">4.0773 ▼ -0.12%</span></span>
            <span class="ticker-item">🛢️ BRENT: <span class="t-red">115.12 ▲ +1.85%</span></span>
            <span class="ticker-item">🥇 GOLD: <span class="t-yellow">$4,013.20 ▲ +0.65%</span></span>
            <span class="ticker-item">🔋 TENAGA: <span class="t-green">RM 12.75 ▲ +1.20%</span></span>
            <span class="ticker-item">🤖 NVDA: <span class="t-green">$141.20 ▲ +2.45%</span></span>
            <span class="ticker-item">💻 MSFT: <span class="t-green">$428.50 ▲ +1.10%</span></span>
            <span class="ticker-item">🏭 UMC: <span class="t-red">$18.65 ▼ -0.80%</span></span>
            <span class="ticker-item">🏗️ GAMUDA: <span class="t-green">RM 4.55 ▲ +1.80%</span></span>
            <span class="ticker-item">⚡ YTLPOWR: <span class="t-green">RM 4.98 ▲ +2.10%</span></span>
            <!-- Gandingan Loop untuk Kelancaran Animasi -->
            <span class="ticker-item">🇲🇾 FBM KLCI: <span class="t-green">1,642.50 ▲ +0.45%</span></span>
            <span class="ticker-item">🇺🇸 S&P 500: <span class="t-green">5,864.20 ▲ +0.72%</span></span>
            <span class="ticker-item">🇺🇸 NASDAQ: <span class="t-green">18,518.60 ▲ +0.95%</span></span>
            <span class="ticker-item">💱 USD/MYR: <span class="t-blue">4.0773 ▼ -0.12%</span></span>
            <span class="ticker-item">🛢️ BRENT: <span class="t-red">115.12 ▲ +1.85%</span></span>
            <span class="ticker-item">🥇 GOLD: <span class="t-yellow">$4,013.20 ▲ +0.65%</span></span>
            <span class="ticker-item">🔋 TENAGA: <span class="t-green">RM 12.75 ▲ +1.20%</span></span>
            <span class="ticker-item">🤖 NVDA: <span class="t-green">$141.20 ▲ +2.45%</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_heatmap_dataset(df_master: pd.DataFrame) -> pd.DataFrame:
    """
    Menyusun dataset berstruktur hierarki untuk Plotly Treemap.
    """
    np.random.seed(88)
    
    # Kumpulan Saham Bursa Malaysia Terpilih
    bursa_stocks = [
        ("TENAGA", "Utiliti & Grid AI", 75000, 1.20),
        ("YTLPOWR", "Utiliti & Grid AI", 42000, 2.10),
        ("GAMUDA", "Infrastruktur & Data Center", 38000, 1.80),
        ("SUNCON", "Infrastruktur & Data Center", 18000, 2.80),
        ("IHH", "Penjagaan Kesihatan Swasta", 65000, 0.40),
        ("KPJ", "Penjagaan Kesihatan Swasta", 12000, -0.50),
        ("PMETAL", "Peleburan Logam & Aluminium", 48000, -1.20),
        ("INARI", "Semikonduktor & OSAT", 14000, 3.10),
        ("FRONTKN", "Semikonduktor & OSAT", 11000, 1.45),
        ("SUNWAY", "Konglomerat Bandar Pintar", 26000, 1.10),
        ("TM", "Telekomunikasi Gentian", 25000, 0.30),
        ("MAXIS", "Telekomunikasi Gentian", 27000, -0.60),
        ("PETCHEM", "Tenaga & Petrokimia", 36000, -2.40),
        ("DIALOG", "Tenaga & Petrokimia", 15000, 0.80),
        ("KLK", "Perladangan Lestari", 24000, -0.90),
        ("GFM", "Pengurusan Fasiliti", 3500, 0.00)
    ]
    
    # Kumpulan Saham Wall Street US Terpilih
    us_stocks = [
        ("NVDA", "Semikonduktor & Perkakasan AI", 3450000, 2.45),
        ("AVGO", "Semikonduktor & Perkakasan AI", 820000, 1.65),
        ("AMD", "Semikonduktor & Perkakasan AI", 240000, -1.80),
        ("MRVL", "Semikonduktor & Perkakasan AI", 75000, 2.10),
        ("UMC", "Semikonduktor & Perkakasan AI", 23000, -0.80),
        ("MSFT", "Awan & Perisian Enterprise", 3180000, 1.10),
        ("GOOGL", "Awan & Perisian Enterprise", 2100000, 0.75),
        ("ORCL", "Awan & Perisian Enterprise", 460000, 3.40),
        ("NOW", "Awan & Perisian Enterprise", 185000, 1.25),
        ("CRM", "Awan & Perisian Enterprise", 280000, -0.40),
        ("AMZN", "E-Dagang & Infrastruktur Awan", 1950000, 1.35),
        ("META", "Media Sosial & AI Ekosistem", 1480000, 2.90),
        ("UBER", "Mobiliti & Logistik Pintar", 160000, 0.60),
        ("PLTR", "Analitik Ketenteraan & AI", 95000, 4.20),
        ("CRWD", "Keselamatan Siber Bersepadu", 78000, -1.10),
        ("PANW", "Keselamatan Siber Bersepadu", 115000, 0.85)
    ]
    
    rows = []
    for sym, sec, mcap, chg in bursa_stocks:
        rows.append({
            "Pasaran": "🇲🇾 Bursa Malaysia",
            "Sektor": sec,
            "Ticker": f"KLSE:{sym}",
            "Nama": sym,
            "Market_Cap": mcap,
            "Perubahan_Pct": chg,
            "Label": f"<b>{sym}</b><br>{chg:+.2f}%"
        })
        
    for sym, sec, mcap, chg in us_stocks:
        rows.append({
            "Pasaran": "🇺🇸 Wall Street US",
            "Sektor": sec,
            "Ticker": f"NASDAQ:{sym}" if sym in ["NVDA", "MSFT", "AMZN", "GOOGL", "AVGO", "META", "MRVL", "AMD", "CRWD", "PANW"] else f"NYSE:{sym}",
            "Nama": sym,
            "Market_Cap": mcap,
            "Perubahan_Pct": chg,
            "Label": f"<b>{sym}</b><br>{chg:+.2f}%"
        })
        
    return pd.DataFrame(rows)

def render_market_treemap(df: pd.DataFrame, market_filter: str = "Semua Pasaran"):
    """
    Menjana Peta Haba Pokok (Treemap) Plotly mengikut Saiz Permodalan & Peratus Perubahan Harian.
    """
    df_plot = df.copy()
    if "Bursa" in market_filter:
        df_plot = df_plot[df_plot["Pasaran"] == "🇲🇾 Bursa Malaysia"]
    elif "Wall" in market_filter or "US" in market_filter:
        df_plot = df_plot[df_plot["Pasaran"] == "🇺🇸 Wall Street US"]

    fig = px.treemap(
        df_plot,
        path=["Pasaran", "Sektor", "Ticker"],
        values="Market_Cap",
        color="Perubahan_Pct",
        color_continuous_scale=[
            (0.00, "#D32F2F"),   # Merah Menyala (-3.0%)
            (0.35, "#B71C1C"),   # Merah Gelap (-1.0%)
            (0.50, "#263238"),   # Neutral / Flat (0.0%)
            (0.65, "#1B5E20"),   # Hijau Gelap (+1.0%)
            (1.00, "#00E676")    # Hijau Neon (+3.0%)
        ],
        color_continuous_midpoint=0.0,
        range_color=[-3.0, 3.0],
        title=f"🗺️ Peta Haba Pasaran Mengikut Sektor & Permodalan ({market_filter})",
        hover_data={"Perubahan_Pct": ":+.2f%", "Market_Cap": ":,d", "Sektor": True, "Pasaran": False}
    )

    fig.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b>",
        textfont=dict(color="#FFFFFF", family="sans-serif", size=13),
        marker=dict(pad=dict(t=25, l=4, r=4, b=4)),
        hovertemplate="<b>%{label}</b><br>Sektor: %{customdata[2]}<br>Perubahan Harian: <b>%{customdata[0]}</b><extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=580,
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_colorbar=dict(
            title="Perubahan %",
            ticksuffix="%",
            tickfont=dict(color="#8E9AAF"),
            title_font=dict(color="#FFFFFF", size=11)
        )
    )
    return fig

def render_sector_rotation_bar(df: pd.DataFrame):
    """
    Menjana carta bar penggiliran sektor (Sector Rotation Momentum).
    """
    sec_summary = df.groupby(["Pasaran", "Sektor"])["Perubahan_Pct"].mean().reset_index()
    sec_summary = sec_summary.sort_values(by="Perubahan_Pct", ascending=True)

    fig = go.Figure()
    colors = ["#00E676" if x >= 0 else "#FF5252" for x in sec_summary["Perubahan_Pct"]]

    fig.add_trace(go.Bar(
        y=sec_summary["Sektor"] + " (" + sec_summary["Pasaran"].str.split().str[0] + ")",
        x=sec_summary["Perubahan_Pct"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.2f}%" for v in sec_summary["Perubahan_Pct"]],
        textposition="outside",
        textfont=dict(color="#FFFFFF", size=11),
        hovertemplate="Sektor: <b>%{y}</b><br>Purata Aliran: <b>%{x:+.2f}%</b><extra></extra>"
    ))

    fig.update_layout(
        title=dict(text="📊 Aliran Dana Sektor: Sektor Menang vs Sektor Kalah", font=dict(color="#FFFFFF", size=14)),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=450,
        margin=dict(l=30, r=50, t=40, b=30),
        xaxis=dict(title="Purata Perubahan Harian (%)", gridcolor="#222B3D", ticksuffix="%"),
        yaxis=dict(gridcolor="#222B3D", tickfont=dict(color="#FFFFFF", size=11))
    )
    return fig

def render_market_heatmap_tab():
    """
    Antara muka penuh tab Peta Haba Pasaran.
    """
    st.header("🗺️ Peta Haba Pasaran (Market Heatmap & Sector Flow)")
    st.caption("Pantau putaran modal institusi, sektor paling untung, dan sebut harga langsung bergaya Finviz / TradingView.")

    # Data Peta Haba
    df_heat = generate_heatmap_dataset(pd.DataFrame())

    # Butang Pemilih Pasaran
    col_sel1, col_sel2 = st.columns([4, 6])
    with col_sel1:
        m_choice = st.radio("Pilih Liputan Peta Haba:", ["🌐 Semua Pasaran (Global)", "🇲🇾 Bursa Malaysia", "🇺🇸 Wall Street US"], horizontal=True)

    # 1. Paparkan Treemap
    fig_tree = render_market_treemap(df_heat, market_filter=m_choice)
    st.plotly_chart(fig_tree, width="stretch")

    st.markdown("---")

    # 2. Penggiliran Sektor
    col_sec1, col_sec2 = st.columns([6, 4])
    with col_sec1:
        fig_sec = render_sector_rotation_bar(df_heat)
        st.plotly_chart(fig_sec, width="stretch")

    with col_sec2:
        st.subheader("💡 Rumusan Risikan Sektor Hari Ini")
        st.markdown("""
        - **Pemimpin Pasaran Terkuat:** Sektor **Semikonduktor & Perkakasan AI** (dipacu NVDA +2.45% & PLTR +4.20%) dan **Infrastruktur Data Center Bursa** (SUNCON +2.80% & YTLPOWR +2.10%).
        - **Sektor Tertekan:** Sektor **Petrokimia & Perladangan** mengalami aliran keluar susulan ketidaktentuan harga komoditi global.
        - **Tindakan SOP DDNK:** Tumpukan modal pada sektor hijau di fasa Wyckoff Mark-Up; elakkan kaunter merah yang masih mencari lantai sokongan.
        """)
