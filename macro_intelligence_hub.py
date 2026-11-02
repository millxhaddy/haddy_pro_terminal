"""Display the configured macro radar as source data without inventing live quotes."""

import pandas as pd
import streamlit as st


def get_live_macro_metrics(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
) -> dict:
    """Return no normalized metrics until a verified macro feed is configured."""
    return {}


def render_macro_intelligence_dashboard(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
):
    st.subheader("Radar makro bersumber")
    st.caption(
        "Paparan ini menunjukkan baris sumber Google Sheets sahaja. Ia tidak "
        "menarik sebut harga pasaran masa nyata atau membuat ramalan sektor."
    )
    source = (vault_data or {}).get("radar_makro")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("31_Radar Makro")
    if not isinstance(source, pd.DataFrame) or source.empty:
        st.info("Data tidak tersedia: tab 31_Radar Makro tiada baris dalam snapshot.")
        return
    st.dataframe(
        source,
        width="stretch",
        hide_index=True,
        alt="Baris mentah daripada tab Radar Makro",
    )
