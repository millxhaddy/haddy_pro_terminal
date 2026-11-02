"""Source-backed relative-volume scanner."""

import pandas as pd
import streamlit as st

from advanced_quant_suite import get_wyckoff_rvol_data


def get_unusual_volume_data(vault_data: dict | None = None) -> pd.DataFrame:
    """Return OHLCV-derived RVOL rows, or an empty frame when source data is absent."""
    return get_wyckoff_rvol_data(vault_data)


def render_unusual_volume_scanner_ui(vault_data: dict | None = None):
    st.subheader("Pengimbas volum luar biasa")
    results = get_unusual_volume_data(vault_data)
    if results.empty:
        st.info(
            "Tiada hasil RVOL: sumber memerlukan ticker, tarikh dan sekurang-kurangnya "
            "21 rekod volum."
        )
        return
    st.caption(
        "Lonjakan volum ialah pemerhatian statistik sahaja; data ini tidak "
        "mengesahkan aktiviti institusi atau manipulasi pasaran."
    )
    st.dataframe(
        results,
        width="stretch",
        hide_index=True,
        alt="Pengimbas volum relatif daripada OHLCV bersumber",
    )
