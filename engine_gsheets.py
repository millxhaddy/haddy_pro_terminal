"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL ENJIN DATA KEBAL: DIRECT HIGH-SPEED CSV INGESTION DENGAN GID RASMI
========================================================================================
"""

import streamlit as st
import pandas as pd
import urllib.parse

DOC_ID = "1lyA9GEChz07i_9X_keem9TJJ2XHMMNaIEzFrqbQ3QAI"

# Peta GID Rasmi bagi setiap tab Haddy Pro
TAB_GIDS = {
    "Master Database": 8888888,
    "Meja_Keputusan_Harian": 880088,
    "Radar_Makro_&_Berita_Live": 319157380,
    "Funding_Details": 87028702,
    "Terminal_Saham": 1001001,
    "Jurnal Dagangan": 4004004,
    "Ringkasan Mudah": 7007007,
    "Sasaran_Sejuta": 7700770
}

@st.cache_data(ttl=60, show_spinner=False)
def get_worksheet_data(worksheet_name: str, header_row: int = 0) -> pd.DataFrame:
    """
    Menyedut data secara terus menggunakan endpoint Google Sheets CSV Export.
    Menggunakan GID unik numerik untuk menghapuskan sebarang ralat 400 Bad Request.
    """
    gid = TAB_GIDS.get(worksheet_name, 0)
    url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/export?format=csv&gid={gid}"
    
    try:
        # Baca terus data menggunakan pandas
        df = pd.read_csv(url, skiprows=header_row, on_bad_lines="skip")
        
        if df is None or df.empty:
            return pd.DataFrame()
            
        # Bersihkan baris & lajur kosong
        df = df.dropna(how="all")
        df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed', na=False)]
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        # Fallback jika berlaku ralat rangkaian
        try:
            encoded_name = urllib.parse.quote(worksheet_name)
            fallback_url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
            df = pd.read_csv(fallback_url, skiprows=header_row, on_bad_lines="skip")
            df = df.dropna(how="all")
            df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed', na=False)]
            df.columns = [str(col).strip() for col in df.columns]
            return df
        except Exception as err:
            st.error(f"Ralat sambungan [{worksheet_name}]: {str(err)}")
            return pd.DataFrame()

def load_all_terminal_data():
    return {
        "master_db": get_worksheet_data("Master Database", header_row=6),
        "meja_keputusan": get_worksheet_data("Meja_Keputusan_Harian", header_row=6),
        "radar_makro": get_worksheet_data("Radar_Makro_&_Berita_Live", header_row=3),
        "funding": get_worksheet_data("Funding_Details", header_row=5),
        "terminal_saham": get_worksheet_data("Terminal_Saham", header_row=8),
        "jurnal": get_worksheet_data("Jurnal Dagangan", header_row=0),
        "sasaran_sejuta": get_worksheet_data("Sasaran_Sejuta", header_row=6)
    }
