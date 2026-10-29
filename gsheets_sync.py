"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PENYEGERAKAN 2-HALA & INPUT QUEUEING (DSR-ENABLED WRITE PIPELINE)
========================================================================================
"""

import streamlit as st
from datetime import datetime
from dsr_engine import write_transaction_with_dsr, sync_queued_inputs

def get_webhook_url() -> str:
    try:
        if hasattr(st, "secrets") and "GSHEETS_WEBHOOK_URL" in st.secrets:
            return str(st.secrets["GSHEETS_WEBHOOK_URL"]).strip()
    except Exception:
        pass
    return ""

def sync_add_watchlist(ticker: str, price: float, sl: float, tp: float, rr: float, status: str, catalyst: str) -> dict:
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
    return write_transaction_with_dsr("04_Senarai Pantau", row, webhook_url=get_webhook_url())

def sync_record_trade(is_buy: bool, ticker: str, market: str, qty: int, price: float, pnl_myr: float = 0.0, notes: str = "") -> dict:
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
        return write_transaction_with_dsr("02_Pegangan Semasa", row, webhook_url=get_webhook_url())
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
        return write_transaction_with_dsr("03_Jurnal Dagangan", row, webhook_url=get_webhook_url())