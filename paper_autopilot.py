"""Honest status for the currently unavailable paper-trading engine."""

import streamlit as st


def render_paper_autopilot_ui():
    st.subheader("Simulasi paper trading")
    st.info(
        "Enjin simulasi harga dan pengurusan pesanan paper belum dikonfigurasikan. "
        "Tiada baki, posisi, kadar menang atau P&L contoh dipaparkan. Gunakan "
        "persekitaran demo broker jika perlukan simulasi pesanan."
    )
