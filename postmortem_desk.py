"""Source-backed portfolio and realized-trade review."""

import pandas as pd
import streamlit as st

from moomoo_journal_analytics import get_journal_analytics_data
from portfolio_holdings import get_active_holdings


def render_postmortem_dashboard(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
):
    st.subheader("Semakan portfolio dan jurnal")
    st.caption(
        "Ringkasan ini hanya menggunakan pegangan dan transaksi yang tersedia dalam "
        "snapshot Google Sheets; ia bukan nasihat pelaburan."
    )

    holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
    analytics = get_journal_analytics_data(vault_data)
    metrics = analytics["metrics"]

    portfolio_value = (
        float(pd.to_numeric(holdings["Nilai_Semasa_MYR"], errors="coerce").sum())
        if not holdings.empty
        else None
    )
    portfolio_pnl = (
        float(pd.to_numeric(holdings["Untung_Rugi_MYR"], errors="coerce").sum(min_count=1))
        if not holdings.empty
        else None
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric(
        "Nilai pasaran pegangan",
        "Tiada data" if portfolio_value is None else f"RM {portfolio_value:,.2f}",
    )
    metric_columns[1].metric(
        "Untung/rugi belum realisasi",
        "Tiada data" if portfolio_pnl is None or pd.isna(portfolio_pnl) else f"RM {portfolio_pnl:,.2f}",
    )
    metric_columns[2].metric(
        "Untung/rugi realisasi jurnal",
        "Tiada data"
        if metrics["net_pnl_myr"] is None
        else f"RM {metrics['net_pnl_myr']:,.2f}",
    )
    metric_columns[3].metric(
        "Rekod dagangan dengan P&L",
        f"{metrics['total_trades']:,}" if metrics["total_trades"] else "Tiada data",
    )

    if holdings.empty:
        st.info("Butiran pegangan tidak tersedia dalam snapshot semasa.")
    else:
        position_data = holdings.copy()
        if portfolio_value and portfolio_value > 0:
            position_data["Pemberat_Pct"] = (
                pd.to_numeric(position_data["Nilai_Semasa_MYR"], errors="coerce")
                / portfolio_value
                * 100
            )
        st.subheader("Pegangan daripada snapshot")
        st.dataframe(
            position_data[
                [
                    "Ticker",
                    "Pasaran",
                    "Unit",
                    "Nilai_Semasa_MYR",
                    "Untung_Rugi_MYR",
                    "ROI_Pct",
                ]
                + (["Pemberat_Pct"] if "Pemberat_Pct" in position_data else [])
            ],
            width="stretch",
            hide_index=True,
        )

    if metrics["total_trades"]:
        st.subheader("Ringkasan jurnal sumber")
        st.dataframe(analytics["discipline"], width="stretch", hide_index=True)
        if metrics["max_drawdown"] is not None:
            st.caption(
                "Susutan maksimum berasaskan turutan rekod jurnal yang diterima; "
                "ia bukan ukuran NAV broker."
            )
            st.metric("Susutan P&L jurnal", f"RM {metrics['max_drawdown']:,.2f}")
    else:
        st.info("Analisis dagangan belum tersedia kerana jurnal tiada P&L realisasi yang sah.")

    st.subheader("Nota semakan")
    with st.form("source_backed_postmortem_form"):
        observation = st.text_area(
            "Pemerhatian berdasarkan data sumber",
            placeholder="Catat perkara yang mahu disemak; jangan anggap sebagai rekod transaksi.",
        )
        next_action = st.text_area(
            "Tindakan susulan",
            placeholder="Contoh: semak rekod, risiko, atau pelan dagangan secara manual.",
        )
        if st.form_submit_button("Simpan nota untuk sesi ini", width="stretch"):
            st.session_state["postmortem_review_note"] = {
                "observation": observation.strip(),
                "next_action": next_action.strip(),
            }
            st.success("Nota disimpan dalam sesi Streamlit ini sahaja.")

    saved_note = st.session_state.get("postmortem_review_note")
    if saved_note:
        st.write("**Pemerhatian:**", saved_note["observation"] or "—")
        st.write("**Tindakan susulan:**", saved_note["next_action"] or "—")
