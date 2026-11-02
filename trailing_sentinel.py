"""
HADDY PRO - TERMINAL MILLX
MODUL 2: RADAR AUTOMATIK TRAILING STOP & KUNCI UNTUNG (TRAILING SENTINEL)
"""

import streamlit as st
import pandas as pd
import math

from advanced_quant_suite import _parse_market_date, _parse_numeric_series
from portfolio_holdings import get_active_holdings

def calculate_trailing_stops(holdings: list) -> pd.DataFrame:
    records = []
    for h in holdings:
        entry = float(h["entry"])
        live = float(h["live"])
        peak = max(float(h["peak"]), live)
        if not all(math.isfinite(value) and value > 0 for value in (entry, live, peak)):
            raise ValueError("Harga entri, semasa dan puncak mesti positif dan terhingga.")
        curr = h["currency"]

        if live >= entry * 1.05:
            ts_price = peak * 0.96
            status = "Ambang trailing ilustrasi tercapai"
        elif live < entry:
            ts_price = entry * 0.97
            status = "Harga semasa di bawah kos purata"
        else:
            ts_price = entry
            status = "Harga semasa melebihi kos purata"

        distance_pct = ((live - ts_price) / live) * 100

        records.append({
            "Ticker": h["ticker"],
            "Mata Wang": curr,
            "Harga Belian": f"{curr} {entry:.3f}",
            "Harga Puncak": f"{curr} {peak:.3f}",
            "Harga Live": f"{curr} {live:.3f}",
            "Had Trailing Stop": f"{curr} {ts_price:.3f}",
            "Penampan Kejatuhan": f"{distance_pct:.2f}%",
            "Tindakan Sentinel": status
        })
    return pd.DataFrame(records)

def render_trailing_sentinel_ui(
    vault_data: dict | None = None,
    fx_rate: float = 4.0773,
):
    st.subheader("Semakan paras trailing daripada pegangan sumber")
    st.caption(
        "Ilustrasi menggunakan ambang tetap: aktif selepas +5%, jarak 4% daripada "
        "puncak; jika rugi, 3% di bawah kos. Bukan arahan transaksi dan bukan "
        "sebut harga langsung."
    )
    holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
    if holdings.empty:
        st.info("Tiada pegangan bersumber untuk disemak.")
        return

    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        st.info("Data puncak OHLCV tidak tersedia; trailing tidak dikira.")
        return

    def find_column(terms):
        return next(
            (column for column in source.columns if any(term in str(column).lower() for term in terms)),
            None,
        )

    ticker_col = find_column(("ticker", "symbol", "simbol"))
    date_col = find_column(("date", "tarikh", "masa"))
    high_col = find_column(("high", "tinggi", "harga tertinggi"))
    close_col = find_column(("close", "tutup", "harga penutup"))
    peak_col = high_col or close_col
    if ticker_col is None or date_col is None or peak_col is None:
        st.info("Data puncak OHLCV tidak lengkap; trailing tidak dikira.")
        return

    history = source[[ticker_col, date_col, peak_col]].copy()
    history["_ticker"] = history[ticker_col].astype(str).str.strip()
    history["_date"] = history[date_col].map(_parse_market_date)
    history["_peak"] = _parse_numeric_series(history[peak_col])
    history = history.dropna(subset=["_date", "_peak"])
    history = history[history["_peak"] > 0]

    active_positions = []
    for _, holding in holdings.iterrows():
        ticker = str(holding["Ticker"]).strip()
        rows = history[history["_ticker"] == ticker]
        entry = holding["Kos_Purata"]
        live = holding["Harga_Semasa"]
        if rows.empty or pd.isna(entry) or pd.isna(live):
            continue
        currency = "$" if holding["Mata_Wang"] == "USD" else "RM"
        active_positions.append(
            {
                "ticker": ticker,
                "currency": currency,
                "entry": float(entry),
                "live": float(live),
                "peak": float(rows["_peak"].max()),
            }
        )
    if not active_positions:
        st.info("Tiada pegangan dengan kos, harga dan sejarah puncak OHLCV yang lengkap.")
        return
    st.dataframe(
        calculate_trailing_stops(active_positions),
        width="stretch",
        hide_index=True,
        alt="Paras trailing ilustrasi daripada pegangan dan sejarah OHLCV",
    )
