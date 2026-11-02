"""Source lookup and curated external video links for the macro dashboard."""

import pandas as pd


LIVE_STREAMS = {
    "Yahoo Finance video": "https://www.youtube.com/watch?v=WPqXO_JqH_o",
    "DW Business video": "https://www.youtube.com/watch?v=V0I_3TEns3g",
    "Semiconductor and AI video": "https://www.youtube.com/watch?v=k1D_mGf00g4",
}


def get_macro_intelligence_data(vault_data: dict | None = None) -> dict[str, pd.DataFrame]:
    """Return the raw macro-radar snapshot; do not synthesize dated events."""
    source = (vault_data or {}).get("radar_makro")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("31_Radar Makro")
    if not isinstance(source, pd.DataFrame):
        source = pd.DataFrame()
    return {"radar": source}
