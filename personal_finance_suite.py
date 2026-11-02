"""Personal-finance source views; no account balances are supplied by defaults."""

import pandas as pd
import streamlit as st


def _show_source_tables(vault_data: dict | None, sources: list[tuple[str, str]]) -> bool:
    vault_data = vault_data or {}
    found = False
    for label, key in sources:
        dataframe = vault_data.get(key)
        if isinstance(dataframe, pd.DataFrame) and not dataframe.empty:
            found = True
            st.subheader(label)
            st.dataframe(
                dataframe,
                width="stretch",
                hide_index=True,
                alt=f"Rekod sumber {label}",
            )
    return found


def render_personal_finance_suite(vault_data: dict | None = None):
    savings_tab, liabilities_tab, zakat_tab = st.tabs(
        ["Simpanan & persaraan", "Liabiliti", "Zakat"]
    )
    with savings_tab:
        st.caption("Paparan hanya menunjukkan rekod akaun yang disambungkan dalam snapshot.")
        if not _show_source_tables(
            vault_data,
            [
                ("Akaun simpanan", "bank_savings"),
                ("Tabung Haji", "tabung_haji"),
                ("ASNB", "asnb"),
                ("Rekod KWSP", "kwsp_accounts"),
            ],
        ):
            st.info(
                "Tiada tab simpanan, Tabung Haji, ASNB atau KWSP bersumber "
                "dikonfigurasikan. Baki akaun tidak dianggarkan."
            )

    with liabilities_tab:
        if not _show_source_tables(
            vault_data,
            [
                ("Lejar liabiliti", "10_Lejar Liabiliti"),
                ("Program AKPK", "12_Program AKPK"),
                ("Sewa beli", "13_Sewa Beli Kereta"),
                ("Pinjaman CIMB", "14_Pinjaman CIMB"),
                ("Kad kredit", "15_Kad Kredit RHB"),
            ],
        ):
            st.info("Tiada rekod liabiliti bersumber dalam snapshot.")

    with zakat_tab:
        st.info(
            "Gunakan modul Zakat berasingan dan masukkan baki tunai, liabiliti, "
            "harga emas semasa serta kaedah yang disahkan sendiri. Suite ini "
            "tidak menyediakan baki, nisab semasa atau keputusan zakat contoh."
        )
