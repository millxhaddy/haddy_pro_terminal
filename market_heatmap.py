"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PETA HABA PASARAN (MARKET HEATMAP) & JALUR SEBUT HARGA BERJALAN (TICKER TAPE)
Visualisasi Gaya TradingView & Finviz (Plotly Treemap & CSS Marquee Engine)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_ticker_tape_marquee():
    """Keep compatibility with older imports without showing fabricated quotes."""
    st.caption("Ticker harga langsung tidak dipaparkan kerana tiada feed pasaran berlesen disambungkan.")

def generate_heatmap_dataset(df_master: pd.DataFrame) -> pd.DataFrame:
    """
    Build a treemap from the user's actual holdings, not sample market-cap or quote data.
    """
    columns = [
        "Pasaran", "Sektor", "Ticker", "Nama", "Nilai_Pegangan_MYR",
        "Perubahan_Pct", "Label",
    ]
    if not isinstance(df_master, pd.DataFrame) or df_master.empty:
        return pd.DataFrame(columns=columns)

    required = {"Ticker", "Pasaran", "Sektor", "Nilai_Semasa_MYR", "ROI_Pct"}
    if not required.issubset(df_master.columns):
        return pd.DataFrame(columns=columns)

    result = pd.DataFrame(
        {
            "Pasaran": df_master["Pasaran"].map(
                lambda value: "🇺🇸 Wall Street US" if "US" in str(value).upper()
                else "🇲🇾 Bursa Malaysia"
            ),
            "Sektor": df_master["Sektor"].fillna("").replace("", "Tidak dikategorikan"),
            "Ticker": df_master["Ticker"].astype(str),
            "Nama": df_master["Nama_Syarikat"].astype(str)
            if "Nama_Syarikat" in df_master
            else df_master["Ticker"].astype(str),
            "Nilai_Pegangan_MYR": pd.to_numeric(
                df_master["Nilai_Semasa_MYR"], errors="coerce"
            ),
            "Perubahan_Pct": pd.to_numeric(df_master["ROI_Pct"], errors="coerce"),
        }
    )
    result = result.dropna(subset=["Nilai_Pegangan_MYR", "Perubahan_Pct"])
    result = result[result["Nilai_Pegangan_MYR"] > 0]
    result["Label"] = result.apply(
        lambda row: f"<b>{row['Ticker']}</b><br>ROI belum realisasi {row['Perubahan_Pct']:+.2f}%",
        axis=1,
    )
    return result[columns]

def render_market_treemap(df: pd.DataFrame, market_filter: str = "Semua Pasaran"):
    """
    Menjana Peta Haba Pokok (Treemap) Plotly mengikut Saiz Permodalan & Peratus Perubahan Harian.
    """
    df_plot = df.copy()
    if "Bursa" in market_filter:
        df_plot = df_plot[df_plot["Pasaran"] == "🇲🇾 Bursa Malaysia"]
    elif "Wall" in market_filter or "US" in market_filter:
        df_plot = df_plot[df_plot["Pasaran"] == "🇺🇸 Wall Street US"]
    if df_plot.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tiada pegangan untuk pasaran yang dipilih.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
        return fig

    color_limit = max(
        1.0,
        float(pd.to_numeric(df_plot["Perubahan_Pct"], errors="coerce").abs().max()),
    )

    fig = px.treemap(
        df_plot,
        path=["Pasaran", "Sektor", "Ticker"],
        values="Nilai_Pegangan_MYR",
        color="Perubahan_Pct",
        color_continuous_scale=[
            (0.00, "#D32F2F"),   # Merah Menyala (-3.0%)
            (0.35, "#B71C1C"),   # Merah Gelap (-1.0%)
            (0.50, "#263238"),   # Neutral / Flat (0.0%)
            (0.65, "#1B5E20"),   # Hijau Gelap (+1.0%)
            (1.00, "#00E676")    # Hijau Neon (+3.0%)
        ],
        color_continuous_midpoint=0.0,
        range_color=[-color_limit, color_limit],
        title=f"🗺️ Agihan Pegangan & ROI Belum Realisasi ({market_filter})",
        hover_data={"Perubahan_Pct": ":+.2f%", "Nilai_Pegangan_MYR": ":,.2f", "Sektor": True, "Pasaran": False}
    )

    fig.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b>",
        textfont=dict(color="#FFFFFF", family="sans-serif", size=13),
        marker=dict(pad=dict(t=25, l=4, r=4, b=4)),
        hovertemplate="<b>%{label}</b><br>Sektor: %{customdata[2]}<br>ROI belum realisasi: <b>%{customdata[0]:+.2f}%</b><br>Nilai pegangan MYR: %{customdata[1]:,.2f}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=580,
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_colorbar=dict(
            title="ROI %",
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
        hovertemplate="Sektor: <b>%{y}</b><br>Purata ROI pegangan: <b>%{x:+.2f}%</b><extra></extra>"
    ))

    fig.update_layout(
        title=dict(text="📊 Purata ROI Belum Realisasi Mengikut Sektor", font=dict(color="#FFFFFF", size=14)),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=450,
        margin=dict(l=30, r=50, t=40, b=30),
        xaxis=dict(title="Purata ROI belum realisasi (%)", gridcolor="#222B3D", ticksuffix="%"),
        yaxis=dict(gridcolor="#222B3D", tickfont=dict(color="#FFFFFF", size=11))
    )
    return fig

def render_market_heatmap_tab(df_holdings: pd.DataFrame):
    """
    Portfolio heatmap based on verified holdings values and unrealized P&L.
    """
    st.header("🗺️ Peta Haba Portfolio")
    st.caption("Saiz kotak = nilai pegangan; warna = ROI belum realisasi. Bukan perubahan harga harian.")
    df_heat = generate_heatmap_dataset(df_holdings)
    if df_heat.empty:
        st.info("Peta haba tersedia selepas pegangan dengan nilai dan kos yang sah dimuatkan daripada Google Sheets.")
        return

    m_choice = st.radio(
        "Pilih liputan portfolio:",
        ["🌐 Semua Pasaran", "🇲🇾 Bursa Malaysia", "🇺🇸 Wall Street US"],
        horizontal=True,
    )

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
        st.subheader("Ringkasan pegangan")
        st.metric("Bilangan pegangan", f"{len(df_heat):,}")
        st.metric("Nilai pegangan dalam snapshot", f"RM {df_heat['Nilai_Pegangan_MYR'].sum():,.2f}")
        st.caption("Sektor dan ROI mengikut snapshot semasa; masa sebut harga bergantung pada data sumber.")
