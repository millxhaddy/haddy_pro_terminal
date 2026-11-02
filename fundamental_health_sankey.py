"""Display source-backed fundamental and cash-flow data without synthetic scores."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from visuals_cashflow import get_cashflow_dataframe


def get_piotroski_altman_data(vault_data: dict | None = None) -> list[dict]:
    """Return raw fundamental-cache rows; do not infer financial-strength scores."""
    source = (vault_data or {}).get("cache_fundamental")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("70_Cache Fundamental")
    if not isinstance(source, pd.DataFrame):
        return []
    return source.to_dict("records")


def render_annual_cashflow_chart(cashflow: pd.DataFrame):
    """Plot completed deposits and withdrawals reported by the cash-flow source."""
    fig = go.Figure()
    if cashflow.empty:
        fig.add_annotation(
            text="Tiada rekod aliran tunai selesai daripada sumber.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
    else:
        fig.add_bar(x=cashflow["Tahun"], y=cashflow["Deposit"], name="Deposit selesai")
        fig.add_bar(
            x=cashflow["Tahun"],
            y=cashflow["Pengeluaran"],
            name="Pengeluaran selesai",
        )
        fig.update_layout(barmode="group")
    fig.update_layout(
        title="Deposit dan pengeluaran tahunan daripada rekod sumber",
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        yaxis_title="RM",
        height=420,
    )
    return fig


def render_fundamental_health_and_sankey_ui(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
):
    st.subheader("Fundamental dan aliran tunai bersumber")
    fundamental_tab, cashflow_tab = st.tabs(
        ["Cache fundamental", "Aliran tunai selesai"]
    )

    with fundamental_tab:
        fundamental_rows = get_piotroski_altman_data(vault_data)
        if not fundamental_rows:
            st.info(
                "Data fundamental tidak tersedia. Skor Piotroski/Altman tidak "
                "dikira tanpa penyata kewangan bersumber dan sejarah perbandingan."
            )
        else:
            st.caption(
                "Baris mentah daripada cache Google Sheets; skor kesihatan atau "
                "risiko muflis tidak disimpulkan daripada data ini."
            )
            st.dataframe(
                pd.DataFrame(fundamental_rows),
                width="stretch",
                hide_index=True,
                alt="Data mentah cache fundamental",
            )

    with cashflow_tab:
        cashflow = get_cashflow_dataframe(vault_data or {})
        if cashflow.empty:
            st.info(
                "Carta tidak tersedia: tiada rekod deposit/pengeluaran selesai "
                "yang boleh dikenal pasti dalam snapshot."
            )
        else:
            st.plotly_chart(
                render_annual_cashflow_chart(cashflow),
                width="stretch",
                alt="Deposit dan pengeluaran selesai mengikut tahun",
            )
            st.dataframe(
                cashflow,
                width="stretch",
                hide_index=True,
                alt="Ringkasan tahunan aliran tunai selesai",
            )
