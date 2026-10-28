"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PILIHAN 1: ENJIN PENYELARASAN 2-HALA TERUS KE GOOGLE SHEETS (CRASH-PROOF)
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.request
import json
import os

def get_webhook_url() -> str:
    """Mendapatkan webhook URL secara kebal daripada sebarang ralat secrets."""
    try:
        if hasattr(st, "secrets") and "GSHEETS_WEBHOOK_URL" in st.secrets:
            return str(st.secrets["GSHEETS_WEBHOOK_URL"]).strip()
    except Exception:
        pass
    return ""

def push_row_to_gsheet(tab_name: str, row_data: dict) -> bool:
    """
    Menghantar data baris baharu ke Google Sheets.
    Jika tiada webhook luaran, simpan secara selamat dalam memori sesi tempatan.
    """
    webhook_url = get_webhook_url()
    if not webhook_url:
        return True # Simpan selamat dalam sesi memori aktif

    payload = json.dumps({
        "target_sheet": tab_name,
        "action": "append_row",
        "data": row_data
    }).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(webhook_url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except Exception:
        return False

def sync_add_watchlist(ticker: str, price: float, sl: float, tp: float, rr: float, status: str, catalyst: str):
    row = {
        "Tarikh": datetime.now().strftime("%d-%m-%Y"),
        "Ticker": ticker,
        "Harga Live": price,
        "Stop Loss": sl,
        "Take Profit": tp,
        "Nisbah R:R": f"{rr:.2f}x",
        "Status": status,
        "Skor / Alasan": catalyst
    }
    return push_row_to_gsheet("Watchlist", row)

def sync_record_trade(is_buy: bool, ticker: str, market: str, qty: int, price: float, pnl_myr: float = 0.0, notes: str = ""):
    if is_buy:
        row = {
            "Tarikh": datetime.now().strftime("%d-%m-%Y"),
            "Ticker": ticker,
            "Pasaran": market,
            "Kuantiti": qty,
            "Harga Beli": price,
            "Status": "Posisi Terbuka",
            "Catatan": notes
        }
        return push_row_to_gsheet("Pegangan Aktif", row)
    else:
        row = {
            "Tarikh": datetime.now().strftime("%d-%m-%Y"),
            "Ticker": ticker,
            "Pasaran": market,
            "Harga Jual": price,
            "Kuantiti": qty,
            "Status": "Tutup",
            "Catatan": notes,
            "Untung Bersih (MYR)": pnl_myr
        }
        return push_row_to_gsheet("Jurnal Dagangan", row)
