"""Source-backed liability overview; no fabricated CCRIS or credit-score data."""

import pandas as pd
import plotly.express as px
import streamlit as st

from pipeline_cleaner import clean_currency


def _find_column(dataframe: pd.DataFrame, terms: tuple[str, ...]):
    return next(
        (
            column
            for column in dataframe.columns
            if any(term in str(column).strip().lower() for term in terms)
        ),
        None,
    )


def _liability_snapshot(vault_data: dict):
    source = (vault_data or {}).get("ccris_facilities")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("10_Lejar Liabiliti")
    if not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame(), None, None

    balance_col = _find_column(source, ("baki semasa", "outstanding balance", "current balance"))
    monthly_col = _find_column(source, ("ansuran bulanan", "ansuran", "monthly payment", "komitmen bulanan"))
    if balance_col is None:
        return source.copy(), None, monthly_col

    normalized = source.copy()
    def parse_amounts(column):
        raw = source[column]
        text = raw.astype(str).str.strip()
        valid = (
            raw.notna()
            & text.str.contains(r"\d", regex=True)
            & ~text.str.startswith("#")
        )
        return raw.map(clean_currency).where(valid)

    normalized["Baki_Semasa_MYR"] = parse_amounts(balance_col)
    if monthly_col is not None:
        normalized["Ansuran_Bulanan_MYR"] = parse_amounts(monthly_col)
    return normalized, "Baki_Semasa_MYR", (
        "Ansuran_Bulanan_MYR" if monthly_col is not None else None
    )


def render_debt_management_dashboard(vault_data=None, stock_portfolio_val=None):
    """Render liability and auxiliary finance data actually present in the Sheets snapshot."""
    data, balance_col, monthly_col = _liability_snapshot(vault_data)
    st.header("Liabiliti & Rekod Kredit daripada Google Sheets")
    st.caption(
        "Paparan ini bukan laporan rasmi CCRIS/Experian atau nasihat kewangan. "
        "Sahkan baki dan kadar dengan institusi kewangan."
    )

    metadata = (vault_data or {}).get("_sync_metadata", {})
    if not metadata.get("remote_data_confirmed"):
        st.warning("Sumber jauh belum disahkan; data yang dipaparkan mungkin snapshot lama/cache.")

    if data.empty:
        st.info("Tiada rekod liabiliti tersedia daripada snapshot Google Sheets.")
    elif balance_col is None:
        st.warning("Lajur baki liabiliti tidak dapat dikenal pasti; rekod mentah dipaparkan tanpa jumlah.")
        st.dataframe(data, width="stretch", hide_index=True)
    else:
        total_balance = data[balance_col].sum(min_count=1)
        if pd.isna(total_balance):
            st.warning("Tiada amaun baki sah yang boleh dijumlahkan; rekod mentah dipaparkan.")
        else:
            first, second = st.columns(2)
            first.metric("Jumlah baki dalam snapshot", f"RM {float(total_balance):,.2f}")
            if monthly_col is not None:
                total_monthly = data[monthly_col].sum(min_count=1)
                second.metric(
                    "Jumlah ansuran dalam snapshot",
                    f"RM {float(total_monthly):,.2f}"
                    if pd.notna(total_monthly)
                    else "Tidak tersedia",
                )
        st.dataframe(data, width="stretch", hide_index=True)

        facility_col = _find_column(data, ("fasiliti", "facility", "institusi", "institution"))
        if facility_col and monthly_col:
            chart_data = data[data[monthly_col] > 0]
            if not chart_data.empty:
                fig = px.pie(
                    chart_data,
                    names=facility_col,
                    values=monthly_col,
                    hole=0.45,
                    title="Komposisi ansuran daripada snapshot",
                )
                st.plotly_chart(fig, width="stretch")

    if stock_portfolio_val is not None:
        st.metric("Nilai pegangan saham (bukan nilai bersih keseluruhan)", f"RM {stock_portfolio_val:,.2f}")

    credit_data = (vault_data or {}).get("dsr_credit_metrics")
    if isinstance(credit_data, pd.DataFrame) and not credit_data.empty:
        st.subheader("Metrik kredit yang dibekalkan oleh sumber")
        st.dataframe(credit_data, width="stretch", hide_index=True)

    akpk_data = (vault_data or {}).get("akpk_dmp_facilities")
    if isinstance(akpk_data, pd.DataFrame) and not akpk_data.empty:
        st.subheader("Rekod AKPK daripada sumber")
        st.dataframe(akpk_data, width="stretch", hide_index=True)
