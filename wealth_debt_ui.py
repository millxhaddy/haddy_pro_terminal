"""Legacy entry point for source-backed asset and liability snapshots."""

import streamlit as st

from wealth_debt_engine import get_holistic_balance_sheet


def render_wealth_debt_dashboard(
    stock_portfolio_val=None,
    cash_reserve=None,
    vault_data=None,
):
    data = get_holistic_balance_sheet(
        stock_portfolio_val=stock_portfolio_val,
        cash_reserve=cash_reserve,
        vault_data=vault_data,
    )
    st.header("Ringkasan aset dan liabiliti yang dibekalkan")
    st.caption(
        "Ringkasan separa sahaja; bukan laporan nilai bersih, CCRIS, atau nasihat kewangan."
    )

    assets, liabilities = st.columns(2)
    if data["total_assets"] is None:
        assets.info("Tiada nilai aset yang dibekalkan.")
    else:
        assets.metric("Jumlah aset yang diketahui", f"RM {data['total_assets']:,.2f}")

    if data["total_liabilities"] is None:
        liabilities.info("Tiada baki liabiliti yang dapat dikenal pasti dalam snapshot.")
    else:
        liabilities.metric("Jumlah baki dalam snapshot", f"RM {data['total_liabilities']:,.2f}")

    if not data["df_assets"].empty:
        st.subheader("Aset yang dibekalkan")
        st.dataframe(data["df_assets"], width="stretch", hide_index=True)
    if not data["df_liabilities"].empty:
        st.subheader("Rekod liabiliti sumber")
        st.dataframe(data["df_liabilities"], width="stretch", hide_index=True)

    st.info("Nilai bersih tidak dikira kerana data aset, tunai dan liabiliti yang lengkap belum disahkan.")
