"""Tax-year journal viewer without fabricated gains or unsupported tax conclusions."""

import streamlit as st

from portfolio_workspace import get_journal_dataframe


def render_tax_ledger_ui(vault_data: dict | None = None):
    st.subheader("Rekod dagangan untuk semakan cukai")
    st.caption(
        "Ini paparan jurnal sumber, bukan pengiraan cukai atau nasihat cukai. "
        "Sahkan klasifikasi dan kewajipan semasa dengan LHDN atau penasihat cukai."
    )
    journal = get_journal_dataframe(vault_data or {})
    if journal.empty:
        st.info("Tiada rekod jurnal dalam snapshot; jumlah keuntungan/dividen tidak dianggarkan.")
        return

    st.dataframe(
        journal,
        width="stretch",
        hide_index=True,
        alt="Rekod dagangan mentah daripada jurnal Google Sheets",
    )
    st.info(
        "Ringkasan tahunan tidak dipaparkan kerana medan tarikh, pasaran, dividen, "
        "yuran dan P&L yang diperlukan belum dinormalisasi sebagai set rekod cukai."
    )
