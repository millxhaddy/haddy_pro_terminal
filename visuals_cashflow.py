"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 5: VISUALISASI ALIRAN TUNAI & EKUITI DINAMIK (PLOTLY CASH FLOW VISUALS)
========================================================================================
"""

import re

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pipeline_cleaner import clean_currency

def get_cashflow_dataframe(vault_data: dict) -> pd.DataFrame:
    """
    Aggregate completed deposits and withdrawals from the live cashflow sheet.
    No synthetic annual figures are shown when the source sheet is unavailable.
    """
    columns = ["Tahun", "Deposit", "Pengeluaran", "Aliran_Bersih", "Kumulatif_Modal"]
    source = (vault_data or {}).get("aliran_tunai")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("66_Aliran Tunai")
    if not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame(columns=columns)

    def find_column(*terms):
        return next(
            (column for column in source.columns
             if any(term in str(column).strip().lower() for term in terms)),
            None,
        )

    activity_col = find_column("jenis aktiviti", "activity", "jenis", "type")
    amount_col = find_column("jumlah", "amount", "amaun")
    status_col = find_column("status")
    date_col = find_column("tarikh", "date")
    year_col = find_column("tahun", "year")
    if activity_col is None or amount_col is None or status_col is None:
        return pd.DataFrame(columns=columns)

    completed = source[
        source[status_col].astype(str).str.strip().str.lower().isin(
            {"completed", "complete", "successful", "success", "settled"}
        )
    ].copy()
    if completed.empty:
        return pd.DataFrame(columns=columns)

    activity = completed[activity_col].astype(str).str.strip().str.lower()
    is_deposit = activity.str.contains("deposit", regex=False)
    is_withdrawal = activity.str.contains("withdraw|pengeluaran", regex=True)
    completed["_year"] = pd.NA
    if date_col is not None:
        def parse_cashflow_year(value):
            if pd.isna(value):
                return pd.NA
            date_text = str(value).strip()
            is_iso_date = bool(
                re.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:\b|T|\s)", date_text)
            )
            parsed_date = pd.to_datetime(
                value,
                errors="coerce",
                dayfirst=not is_iso_date,
                yearfirst=is_iso_date,
            )
            return pd.NA if pd.isna(parsed_date) else parsed_date.year

        completed["_year"] = completed[date_col].map(parse_cashflow_year).astype("Int64")
    if year_col is not None:
        parsed_years = pd.to_numeric(completed[year_col], errors="coerce").astype("Int64")
        completed["_year"] = completed["_year"].fillna(parsed_years)
    amount_text = completed[amount_col].astype(str).str.strip()
    valid_amount = (
        completed[amount_col].notna()
        & amount_text.str.contains(r"\d", regex=True)
        & ~amount_text.str.startswith("#")
    )
    completed["_activity"] = activity
    completed["_is_deposit"] = is_deposit
    completed["_is_withdrawal"] = is_withdrawal
    completed["_amount"] = completed[amount_col].map(
        lambda amount: abs(clean_currency(amount))
    )
    completed = completed[
        completed["_year"].notna()
        & valid_amount
        & (completed["_is_deposit"] | completed["_is_withdrawal"])
    ]
    if completed.empty:
        return pd.DataFrame(columns=columns)

    completed["_deposit"] = completed["_amount"].where(
        completed["_is_deposit"], 0.0
    )
    completed["_withdrawal"] = completed["_amount"].where(
        completed["_is_withdrawal"], 0.0
    )
    annual = completed.groupby("_year", sort=True).agg(
        Deposit=("_deposit", "sum"),
        Pengeluaran=("_withdrawal", "sum"),
    ).reset_index()
    annual["Tahun"] = annual["_year"].astype(int).astype(str)
    annual["Aliran_Bersih"] = annual["Deposit"] - annual["Pengeluaran"]
    annual["Kumulatif_Modal"] = annual["Aliran_Bersih"].cumsum()
    return annual[columns]

def render_cumulative_equity_curve(df: pd.DataFrame):
    """
    Menjana Carta Kawasan (Spline Area Chart) trajektori pertumbuhan modal kumulatif.
    """
    fig = go.Figure()
    if df is None or df.empty:
        fig.add_annotation(
            text="Tiada rekod aliran tunai selesai daripada Google Sheets.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
        return fig

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
            text="📈 Trajektori Modal Bersih Terkumpul mengikut tahun sumber",
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
    if df is None or df.empty:
        fig.add_annotation(
            text="Tiada rekod aliran tunai selesai daripada Google Sheets.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
        return fig

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
