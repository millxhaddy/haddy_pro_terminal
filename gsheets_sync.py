"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PENYEGERAKAN 2-HALA & INPUT QUEUEING (DSR-ENABLED WRITE PIPELINE)
========================================================================================
"""

import os
import streamlit as st
from datetime import datetime
from dsr_engine import write_transaction_with_dsr

def get_webhook_url() -> str:
    try:
        if hasattr(st, "secrets"):
            for key in ("GSHEETS_WEBHOOK_URL", "GOOGLE_SHEETS_WEBHOOK_URL", "WEBHOOK_URL"):
                value = st.secrets.get(key, "")
                if value:
                    return str(value).strip()
    except Exception:
        pass
    return os.environ.get("GSHEETS_WEBHOOK_URL", "").strip()

def get_webhook_token() -> str:
    try:
        if hasattr(st, "secrets"):
            token = st.secrets.get("HADDY_WEBHOOK_TOKEN", "")
            connections = st.secrets.get("connections", {})
            gsheets_connection = (
                connections.get("gsheets", {})
                if hasattr(connections, "get")
                else {}
            )
            token = token or (
                gsheets_connection.get("HADDY_WEBHOOK_TOKEN", "")
                if hasattr(gsheets_connection, "get")
                else ""
            )
            if token:
                return str(token).strip()
    except Exception:
        pass
    return os.environ.get("HADDY_WEBHOOK_TOKEN", "").strip()

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
    return write_transaction_with_dsr(
        "04_Senarai Pantau",
        row,
        webhook_url=get_webhook_url(),
        token=get_webhook_token(),
    )

def sync_record_trade(
    is_buy: bool,
    ticker: str,
    market: str,
    qty: int,
    price: float,
    pnl_myr: float = 0.0,
    notes: str = "",
    average_cost: float = 0.0,
    fees_myr: float = 0.0,
) -> dict:
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
        return write_transaction_with_dsr(
            "02_Pegangan Semasa",
            row,
            webhook_url=get_webhook_url(),
            action="append_row",
            token=get_webhook_token(),
        )
    else:
        row = {
            "Tarikh": datetime.now().strftime("%d-%m-%Y"),
            "Ticker": ticker,
            "Pasaran": market,
            "Harga Jual": price,
            "Kuantiti": qty,
            "Kos Purata": average_cost,
            "Yuran (MYR)": fees_myr,
            "Status": "Tutup",
            "Catatan": notes,
            "Untung Bersih (MYR)": pnl_myr
        }
        return write_transaction_with_dsr(
            "03_Jurnal Dagangan",
            row,
            webhook_url=get_webhook_url(),
            action="append_row",
            token=get_webhook_token(),
        )