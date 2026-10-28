"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 5: VISUALISASI ALIRAN TUNAI & EKUITI DINAMIK (PLOTLY CASH FLOW VISUALS)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def get_cashflow_dataframe(vault_data: dict) -> pd.DataFrame:
    """
    Menyusun data aliran tunai tahunan rasmi berasaskan rekod audit lembaran.
    """
    data = [
        {"Tahun": "2024", "Deposit": 25000.00, "Pengeluaran": 4902.04, "Aliran_Bersih": 20097.96, "Kumulatif_Modal": 20097.96},
        {"Tahun": "2025", "Deposit": 15000.00, "Pengeluaran": 16018.39, "Aliran_Bersih": -1018.39, "Kumulatif_Modal": 19079.57},
        {"Tahun": "2026", "Deposit": 44801.00, "Pengeluaran": 21382.77, "Aliran_Bersih": 23418.23, "Kumulatif_Modal": 42497.80}
    ]
    return pd.DataFrame(data)

def render_cumulative_equity_curve(df: pd.DataFrame):
    """
    Menjana Carta Kawasan (Spline Area Chart) trajektori pertumbuhan modal kumulatif.
    """
    fig = go.Figure()

    # Garisan & Kawasan Berlorek Kumulatif Modal
    fig.add_trace(go.Scatter(
        x=df["Tahun"],
        y=df["Kumulatif_Modal"],
        mode="lines+markers+text",
        name="Modal Bersih Terkumpul (MYR)",
        line=dict(color="#00E676", width=3, shape="spline"),
        marker=dict(size=9, color="#00E676", symbol="circle"),
        text=[f"RM {v:,.0f}" for v in df["Kumulatif_Modal"]],
        textposition="top center",
        textfont=dict(color="#FFFFFF", size=11, family="sans-serif"),
        fill="tozeroy",
        fillcolor="rgba(0, 230, 118, 0.12)",
        hovertemplate="<b>Tahun %{x}</b><br>Modal Terkumpul: <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="📈 Trajektori Pertumbuhan Modal Bersih Terkumpul (2024 - 2026)",
            font=dict(size=15, color="#FFFFFF", family="sans-serif")
        ),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=360,
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#222B3D",
            tickfont=dict(color="#8E9AAF", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#222B3D",
            tickprefix="RM ",
            tickfont=dict(color="#8E9AAF", size=11)
        ),
        showlegend=False
    )
    return fig

def render_annual_flow_breakdown(df: pd.DataFrame):
    """
    Menjana Carta Bar Berkelompok perbandingan Aliran Masuk (Deposit) vs Aliran Keluar (Pengeluaran).
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Tahun"],
        y=df["Deposit"],
        name="Deposit Masuk",
        marker_color="#00E676",
        hovertemplate="Deposit: <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=df["Tahun"],
        y=df["Pengeluaran"],
        name="Pengeluaran Keluar",
        marker_color="#FF5252",
        hovertemplate="Pengeluaran: <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=df["Tahun"],
        y=df["Aliran_Bersih"],
        name="Aliran Bersih Tahunan",
        marker_color="#29B6F6",
        hovertemplate="Aliran Bersih: <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="📊 Perbandingan Aliran Masuk vs Keluar Mengikut Tahun",
            font=dict(size=15, color="#FFFFFF", family="sans-serif")
        ),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        barmode="group",
        height=360,
        margin=dict(l=30, r=30, t=50, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#8E9AAF", size=11)
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#8E9AAF", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#222B3D",
            tickprefix="RM ",
            tickfont=dict(color="#8E9AAF", size=11)
        )
    )
    return fig
