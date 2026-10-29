"""
HADDY PRO - TERMINAL MILLX
MODUL ENJIN DATA KEBAL: INTEGRASI PENUH DYNAMIC SYSTEM RESILIENCE (DSR)
"""
import streamlit as st
import pandas as pd
from dsr_engine import fetch_sheet_with_dsr, sync_queued_inputs

# Peta GID Rasmi bagi setiap tab Haddy Pro
TAB_GIDS = {
    "Pusat Kawalan": 1962521498,
    "Meja Keputusan": 880088,
    "Pegangan Semasa": 3003003,
    "Jurnal Dagangan": 4004004,
    "Senarai Pantau": 1948291081,
    "Kalkulator 3M": 990099,
    "Pangkalan 1000": 8888888,
    "Lejar Liabiliti": 132297070,
    "Skor Kredit": 7004529,
    "Program AKPK": 1522726426,
    "Sewa Beli Kereta": 144766196,
    "Pinjaman CIMB": 82870378,
    "Kad Kredit RHB": 1928302918,
    "PTPTN Ujrah": 721185977,
    "Yuran Kediaman": 1163122475,
    "Akaun Bank": 116986296,
    "Simpanan KWSP": 574881366,
    "Zakat Harta": 1610247390,
    "Fiqh Kewangan": 1677076971,
    "Sasaran Sejuta": 7700770,
    "Radar Makro": 319157380,
    "Sejarah Dana": 87028702,
    "Sejarah Padanan": 987654321,
    "Ringkasan Mudah": 7007007,
    "Konfigurasi Vault": 5550001,
    "Kesihatan Sistem": 9509509
}

@st.cache_data(ttl=60, show_spinner=False)
def get_worksheet_data(worksheet_name: str, header_row: int = 0) -> pd.DataFrame:
    gid = TAB_GIDS.get(worksheet_name, 0)
    df, status = fetch_sheet_with_dsr(worksheet_name, gid=gid, header_row=header_row)
    return df

def load_all_terminal_data():
    return {
        "master_db": get_worksheet_data("Pangkalan 1000", header_row=6),
        "meja_keputusan": get_worksheet_data("Meja Keputusan", header_row=6),
        "radar_makro": get_worksheet_data("Radar Makro", header_row=3),
        "funding": get_worksheet_data("Sejarah Dana", header_row=5),
        "pengurusan_hutang": get_worksheet_data("Lejar Liabiliti", header_row=7),
        "jurnal": get_worksheet_data("Jurnal Dagangan", header_row=0),
        "sasaran_sejuta": get_worksheet_data("Sasaran Sejuta", header_row=6)
    }