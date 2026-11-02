"""Google Sheets-backed screening views; no generated sample securities or scores."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_institutional_screener_data(vault_data: dict) -> pd.DataFrame:
    """Return the screener sheet as received, or an empty frame when it is unavailable."""
    for key in ("screener_1000", "df_1000", "06_Pangkalan 1000"):
        source = (vault_data or {}).get(key)
        if isinstance(source, pd.DataFrame) and not source.empty:
            return source.copy()
    return pd.DataFrame()


def render_canslim_bubble_matrix(df: pd.DataFrame):
    """Plot source-provided screening metrics only when the required fields exist."""
    fig = go.Figure()
    required = {
        "Ticker",
        "Harga_Semasa",
        "Potensi_Upside_Pct",
        "CANSLIM_Score",
        "Pasaran",
    }
    if not isinstance(df, pd.DataFrame) or df.empty or not required.issubset(df.columns):
        fig.add_annotation(
            text="Tiada data saringan dan skor sah daripada tab Google Sheets.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
        return fig

    chart_data = df.copy()
    for column in ("Harga_Semasa", "Potensi_Upside_Pct", "CANSLIM_Score"):
        chart_data[column] = pd.to_numeric(chart_data[column], errors="coerce")
    chart_data = chart_data.dropna(
        subset=["Harga_Semasa", "Potensi_Upside_Pct", "CANSLIM_Score"]
    )
    if chart_data.empty:
        return render_canslim_bubble_matrix(pd.DataFrame())

    fig = px.scatter(
        chart_data.head(120),
        x="Harga_Semasa",
        y="Potensi_Upside_Pct",
        size="CANSLIM_Score",
        color="Pasaran",
        hover_name="Ticker",
        title="Saringan daripada snapshot Google Sheets",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=480,
    )
    return fig
