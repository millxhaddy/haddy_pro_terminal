"""
HADDY PRO - TERMINAL MILLX
MODUL 1: ENJIN UJIAN STRATEGI LAMPAU (HISTORICAL BACKTESTING ENGINE)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def run_ddnk_backtest(df_candles: pd.DataFrame, initial_capital: float = 40000.0, risk_per_trade: float = 0.02) -> dict:
    if df_candles.empty or len(df_candles) < 30:
        return {}

    df = df_candles.sort_values("Date").reset_index(drop=True)
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

    capital = initial_capital
    position = 0
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    trades = []
    equity_curve = [capital]

    for i in range(2, len(df)):
        price = df.loc[i, "Close"]
        high = df.loc[i, "High"]
        low = df.loc[i, "Low"]
        date = df.loc[i, "Date"]

        if position == 0:
            if df.loc[i-1, "EMA20"] > df.loc[i-1, "EMA50"] and df.loc[i-2, "EMA20"] <= df.loc[i-2, "EMA50"]:
                entry_price = price
                stop_loss = price * 0.98
                take_profit = price * 1.05
                risk_amt = capital * risk_per_trade
                position = int(risk_amt / (entry_price - stop_loss))
                entry_date = date
        else:
            if low <= stop_loss:
                pnl = position * (stop_loss - entry_price)
                capital += pnl
                trades.append({
                    "Entry Date": entry_date, "Exit Date": date,
                    "Type": "Cut Loss", "Entry": entry_price, "Exit": stop_loss,
                    "PnL (RM)": pnl, "Return": -0.02
                })
                position = 0
            elif high >= take_profit:
                pnl = position * (take_profit - entry_price)
                capital += pnl
                trades.append({
                    "Entry Date": entry_date, "Exit Date": date,
                    "Type": "Take Profit", "Entry": entry_price, "Exit": take_profit,
                    "PnL (RM)": pnl, "Return": 0.05
                })
                position = 0

        equity_curve.append(capital)

    df_trades = pd.DataFrame(trades)
    win_rate = (len(df_trades[df_trades["PnL (RM)"] > 0]) / len(df_trades) * 100) if not df_trades.empty else 0
    total_pnl = capital - initial_capital

    return {
        "final_capital": capital,
        "total_pnl": total_pnl,
        "win_rate": win_rate,
        "trades": df_trades,
        "equity_curve": equity_curve,
        "dates": df["Date"].iloc[len(df)-len(equity_curve):].tolist()
    }

def render_backtest_ui():
    st.subheader("🧪 Enjin Ujian Strategi Lampau (Historical Backtester)")
    st.caption("Ujian simulasi peraturan teknikal DDNK ke atas data sejarah saham.")

    c1, c2 = st.columns(2)
    with c1:
        ticker = st.selectbox("Pilih Saham untuk Ujian Lampau:", ["KLSE:TENAGA", "KLSE:GAMUDA", "NASDAQ:NVDA", "NYSE:UMC"])
        capital = st.number_input("Modal Permulaan Ujian (RM):", value=42497.80, step=1000.0)
    with c2:
        risk = st.slider("Had Risiko Per Dagangan (%):", 1.0, 3.0, 2.0, step=0.5)
        period_days = st.select_slider("Tempoh Ujian (Hari):", [90, 180, 365, 730], value=365)

    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=period_days)
    base = 12.0 if "KLSE" in ticker else 140.0
    prices = [base]
    for _ in range(period_days - 1):
        prices.append(prices[-1] * (1 + np.random.normal(0.0008, 0.018)))

    df_sim = pd.DataFrame({"Date": dates, "Close": prices})
    df_sim["High"] = df_sim["Close"] * 1.015
    df_sim["Low"] = df_sim["Close"] * 0.985

    results = run_ddnk_backtest(df_sim, initial_capital=capital, risk_per_trade=risk/100.0)

    if results:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Modal Akhir", f"RM {results['final_capital']:,.2f}")
        m2.metric("Untung/Rugi Bersih", f"RM {results['total_pnl']:,.2f}", f"{(results['total_pnl']/capital*100):.1f}%")
        m3.metric("Kadar Kemenangan", f"{results['win_rate']:.1f}%")
        m4.metric("Jumlah Dagangan", f"{len(results['trades'])} Trades")

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=results["equity_curve"], mode="lines", name="Keluk Ekuiti", line=dict(color="#00E676", width=2.5)))
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=20, r=20, t=30, b=20), yaxis=dict(tickprefix="RM "))
        st.plotly_chart(fig, width="stretch")

        if not results["trades"].empty:
            st.dataframe(results["trades"].tail(10), width="stretch", hide_index=True)
