"""Historical strategy simulation using only source-backed OHLCV data."""

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from advanced_quant_suite import _parse_market_date, _parse_numeric_series


def run_ddnk_backtest(
    df_candles: pd.DataFrame,
    initial_capital: float,
    risk_per_trade: float,
) -> dict:
    """Simulate a fixed EMA-cross rule against supplied historical candles."""
    if not math.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError("Modal permulaan mesti positif.")
    if not math.isfinite(risk_per_trade) or not 0 < risk_per_trade <= 1:
        raise ValueError("Risiko setiap dagangan mesti antara 0 dan 100%.")
    required = {"Date", "Close", "High", "Low"}
    if not required.issubset(df_candles.columns):
        return {}
    df = df_candles[list(required)].copy()
    df = df.dropna(subset=["Date", "Close", "High", "Low"]).sort_values("Date")
    if len(df) < 30:
        return {}
    if (df[["Close", "High", "Low"]] <= 0).any().any():
        return {}

    df = df.reset_index(drop=True)
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
    capital = initial_capital
    position = 0
    entry_price = stop_loss = take_profit = 0.0
    trades = []
    equity_curve = [capital, capital]

    for index in range(2, len(df)):
        price = float(df.loc[index, "Close"])
        high = float(df.loc[index, "High"])
        low = float(df.loc[index, "Low"])
        date = df.loc[index, "Date"]

        if position == 0:
            crossed_up = (
                df.loc[index - 1, "EMA20"] > df.loc[index - 1, "EMA50"]
                and df.loc[index - 2, "EMA20"] <= df.loc[index - 2, "EMA50"]
            )
            if crossed_up:
                entry_price = price
                stop_loss = price * 0.98
                take_profit = price * 1.05
                risk_amount = capital * risk_per_trade
                risk_sized = int(risk_amount / (entry_price - stop_loss))
                affordable = int(capital / entry_price)
                position = min(risk_sized, affordable)
                if position:
                    entry_date = date
        elif low <= stop_loss:
            pnl = position * (stop_loss - entry_price)
            capital += pnl
            trades.append(
                {
                    "Tarikh masuk": entry_date,
                    "Tarikh keluar": date,
                    "Sebab keluar": "Stop",
                    "Entri": entry_price,
                    "Keluar": stop_loss,
                    "P&L (RM)": pnl,
                }
            )
            position = 0
        elif high >= take_profit:
            pnl = position * (take_profit - entry_price)
            capital += pnl
            trades.append(
                {
                    "Tarikh masuk": entry_date,
                    "Tarikh keluar": date,
                    "Sebab keluar": "Sasaran",
                    "Entri": entry_price,
                    "Keluar": take_profit,
                    "P&L (RM)": pnl,
                }
            )
            position = 0
        equity_curve.append(capital)

    if position:
        final_price = float(df.iloc[-1]["Close"])
        pnl = position * (final_price - entry_price)
        capital += pnl
        trades.append(
            {
                "Tarikh masuk": entry_date,
                "Tarikh keluar": df.iloc[-1]["Date"],
                "Sebab keluar": "Penutup siri",
                "Entri": entry_price,
                "Keluar": final_price,
                "P&L (RM)": pnl,
            }
        )
        equity_curve[-1] = capital

    trade_frame = pd.DataFrame(trades)
    wins = int((trade_frame["P&L (RM)"] > 0).sum()) if not trade_frame.empty else 0
    win_rate = wins / len(trade_frame) * 100 if not trade_frame.empty else None
    return {
        "final_capital": capital,
        "total_pnl": capital - initial_capital,
        "win_rate": win_rate,
        "trades": trade_frame,
        "equity_curve": equity_curve,
        "dates": df["Date"].tolist(),
    }


def _get_candles(vault_data: dict | None, ticker: str) -> pd.DataFrame:
    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame()

    def find_column(terms):
        return next(
            (column for column in source.columns if any(term in str(column).lower() for term in terms)),
            None,
        )

    ticker_col = find_column(("ticker", "symbol", "simbol"))
    date_col = find_column(("date", "tarikh", "masa"))
    close_col = find_column(("close", "tutup", "harga penutup"))
    high_col = find_column(("high", "tinggi", "harga tertinggi"))
    low_col = find_column(("low", "rendah", "harga terendah"))
    if None in (ticker_col, date_col, close_col, high_col, low_col):
        return pd.DataFrame()

    candles = source[
        [ticker_col, date_col, close_col, high_col, low_col]
    ].copy()
    candles = candles[candles[ticker_col].astype(str).str.strip() == ticker]
    candles["Date"] = candles[date_col].map(_parse_market_date)
    candles["Close"] = _parse_numeric_series(candles[close_col])
    candles["High"] = _parse_numeric_series(candles[high_col])
    candles["Low"] = _parse_numeric_series(candles[low_col])
    return candles[["Date", "Close", "High", "Low"]].dropna().sort_values("Date")


def render_backtest_ui(vault_data: dict | None = None):
    st.subheader("Backtest EMA daripada OHLCV sumber")
    st.caption(
        "Andaian tetap: EMA20/EMA50 silang ke atas, stop 2%, sasaran 5%, "
        "risiko posisi berdasarkan input. Yuran/cukai tidak dimasukkan; jika stop "
        "dan sasaran disentuh pada hari sama, stop dikira dahulu."
    )
    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        st.info("Backtest tidak tersedia: cache OHLCV kosong.")
        return
    ticker_col = next(
        (
            column
            for column in source.columns
            if any(term in str(column).lower() for term in ("ticker", "symbol", "simbol"))
        ),
        None,
    )
    if ticker_col is None:
        st.info("Backtest tidak tersedia: lajur ticker tiada.")
        return
    tickers = sorted(
        value
        for value in source[ticker_col].dropna().astype(str).str.strip().unique()
        if value
    )
    if not tickers:
        st.info("Backtest tidak tersedia: tiada ticker dalam cache.")
        return

    with st.form("historical_backtest_form"):
        ticker = st.selectbox("Ticker dalam cache OHLCV", tickers)
        capital = st.number_input(
            "Modal simulasi (RM)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
        )
        risk = st.slider("Risiko modal setiap dagangan (%)", 0.5, 5.0, 1.0, step=0.5)
        days = st.select_slider("Bilangan rekod harian terakhir", [30, 90, 180, 365, 730], value=90)
        submitted = st.form_submit_button("Jalankan backtest", width="stretch")
    if not submitted:
        st.info("Hantar input untuk menjalankan backtest pada sejarah yang tersedia.")
        return
    if capital <= 0:
        st.warning("Masukkan modal simulasi positif.")
        return

    candles = _get_candles(vault_data, ticker).tail(days)
    results = run_ddnk_backtest(
        candles,
        initial_capital=capital,
        risk_per_trade=risk / 100,
    )
    if not results:
        st.info("Tidak cukup rekod sah: sekurang-kurangnya 30 candle OHLC diperlukan.")
        return

    first, second, third = st.columns(3)
    first.metric("Modal akhir simulasi", f"RM {results['final_capital']:,.2f}")
    second.metric(
        "Untung/rugi simulasi",
        f"RM {results['total_pnl']:,.2f}",
        delta=f"{results['total_pnl'] / capital:.1%}",
    )
    third.metric(
        "Kadar menang",
        f"{results['win_rate']:.1f}%"
        if results["win_rate"] is not None
        else "Tiada dagangan",
    )
    figure = go.Figure()
    figure.add_scatter(
        x=results["dates"],
        y=results["equity_curve"],
        mode="lines",
        name="Ekuiti simulasi",
    )
    figure.update_layout(
        title="Ekuiti simulasi (tanpa yuran)",
        xaxis_title="Tarikh",
        yaxis_title="RM",
        template="plotly_dark",
    )
    st.plotly_chart(
        figure,
        width="stretch",
        alt="Keluk ekuiti backtest OHLCV",
    )
    if results["trades"].empty:
        st.info("Tiada dagangan dicetuskan oleh peraturan EMA pada tempoh ini.")
    else:
        st.dataframe(
            results["trades"],
            width="stretch",
            hide_index=True,
            alt="Dagangan simulasi daripada backtest",
        )
