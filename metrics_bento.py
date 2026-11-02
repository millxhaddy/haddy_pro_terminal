"""Portfolio metrics derived only from source-backed Sheets snapshots."""

import pandas as pd
import streamlit as st

from portfolio_holdings import get_active_holdings
from visuals_cashflow import get_cashflow_dataframe


def extract_portfolio_kpis(vault_data: dict, fx_rate: float = 4.0773) -> dict:
    """Calculate only metrics supported by normalized Google Sheets source data."""
    kpis = {}
    cashflow = get_cashflow_dataframe(vault_data)
    if not cashflow.empty:
        total_deposits = float(cashflow["Deposit"].sum())
        total_withdrawals = float(cashflow["Pengeluaran"].sum())
        kpis.update(
            {
                "total_deposit": total_deposits,
                "total_withdrawal": total_withdrawals,
                "net_invested": total_deposits - total_withdrawals,
            }
        )
        if total_deposits > 0:
            kpis["cash_retention_pct"] = (
                (total_deposits - total_withdrawals) / total_deposits * 100
            )

    holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
    if not holdings.empty:
        kpis["active_portfolio_val"] = float(holdings["Nilai_Semasa_MYR"].sum())
        pnl_values = pd.to_numeric(holdings["Untung_Rugi_MYR"], errors="coerce")
        cost_values = pd.to_numeric(holdings["Nilai_Modal_MYR"], errors="coerce")
        if pnl_values.notna().all() and cost_values.gt(0).all():
            kpis["unrealized_pnl"] = float(pnl_values.sum())
            cost_basis = float(cost_values.sum())
            kpis["unrealized_roi_pct"] = kpis["unrealized_pnl"] / cost_basis * 100

    journal = (vault_data or {}).get("jurnal_dagangan_df")
    if isinstance(journal, pd.DataFrame) and not journal.empty:
        kpis["total_trades"] = int(len(journal))
    return kpis


def render_bento_metrics(kpis: dict):
    """Render source-backed values and mark absent values explicitly."""
    metrics = [
        ("total_deposit", "Deposit selesai", "RM", 2),
        ("total_withdrawal", "Pengeluaran selesai", "RM", 2),
        ("net_invested", "Modal bersih", "RM", 2),
        ("active_portfolio_val", "Nilai pasaran pegangan", "RM", 2),
        ("unrealized_pnl", "Untung/rugi belum realisasi", "RM", 2),
        ("unrealized_roi_pct", "ROI belum realisasi", "%", 2),
        ("total_trades", "Rekod jurnal tersedia", "", 0),
    ]
    columns = st.columns(4)
    for index, (key, label, unit, decimals) in enumerate(metrics):
        value = kpis.get(key)
        if value is None:
            display = "Tiada data"
        elif unit == "RM":
            display = f"RM {float(value):,.{decimals}f}"
        elif unit == "%":
            display = f"{float(value):.{decimals}f}%"
        else:
            display = f"{int(value):,}"
        columns[index % len(columns)].metric(label, display)
