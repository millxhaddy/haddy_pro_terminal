"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL KUANTITATIF BERSEPADU:
1. Monte Carlo Simulation (1,000 Runs & Ruin Probability)
2. Portfolio Correlation & Cluster Risk Matrix
3. Wyckoff Smart Money & Volume Spread Screener (RVOL)
4. Earnings & Dividend Calendar Hub
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
from moomoo_journal_analytics import get_realized_trade_pnls


def _parse_market_date(value):
    if pd.isna(value):
        return pd.NaT
    text = str(value).strip()
    iso_date = bool(re.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}", text))
    return pd.to_datetime(
        value,
        errors="coerce",
        format="mixed",
        dayfirst=not iso_date,
        yearfirst=iso_date,
        utc=True,
    )


def _parse_numeric_series(values: pd.Series) -> pd.Series:
    cleaned = values.astype(str).str.replace(r"[^\d.\-]", "", regex=True)
    return pd.to_numeric(cleaned.replace("", pd.NA), errors="coerce")

# ======================================================================================
# 1. ENJIN SIMULASI MONTE CARLO & STRESS-TEST
# ======================================================================================
def run_monte_carlo_simulation(
    starting_capital: float,
    trade_pnls: list[float] | None = None,
    win_rate: float | None = None,
    avg_win: float | None = None,
    avg_loss: float | None = None,
    num_simulations: int = 1000,
    num_trades: int = 100,
) -> dict:
    if starting_capital <= 0 or num_simulations <= 0 or num_trades <= 0:
        raise ValueError("Modal dan bilangan simulasi/dagangan mesti positif.")

    if trade_pnls:
        empirical_pnls = np.asarray(trade_pnls, dtype=float)
        empirical_pnls = empirical_pnls[np.isfinite(empirical_pnls)]
    elif (
        win_rate is not None
        and avg_win is not None
        and avg_loss is not None
        and 0 <= win_rate <= 1
        and avg_win >= 0
        and avg_loss >= 0
    ):
        rng = np.random.default_rng(42)
        outcomes = rng.binomial(1, win_rate, size=(num_trades, num_simulations))
        pnl_matrix = np.where(outcomes == 1, avg_win, -avg_loss)
        empirical_pnls = None
    else:
        raise ValueError("Bekalkan P&L jurnal atau statistik simulasi yang sah.")

    if empirical_pnls is not None:
        if not len(empirical_pnls):
            raise ValueError("Jurnal tidak mempunyai nilai P&L terhingga untuk simulasi.")
        rng = np.random.default_rng(42)
        pnl_matrix = rng.choice(
            empirical_pnls,
            size=(num_trades, num_simulations),
            replace=True,
        )

    equity_curves = np.vstack(
        [
            np.full(num_simulations, starting_capital),
            starting_capital + np.cumsum(pnl_matrix, axis=0),
        ]
    )

    p95 = np.percentile(equity_curves, 95, axis=1)
    p50 = np.percentile(equity_curves, 50, axis=1)
    p05 = np.percentile(equity_curves, 5, axis=1)
    ruin_threshold = starting_capital * 0.50
    min_equities = np.min(equity_curves, axis=0)
    ruin_count = np.sum(min_equities < ruin_threshold)
    ruin_prob = (ruin_count / num_simulations) * 100.0

    return {
        "trades": np.arange(num_trades + 1),
        "curves": equity_curves,
        "p95": p95,
        "p50": p50,
        "p05": p05,
        "final_median": p50[-1],
        "final_p95": p95[-1],
        "final_p05": p05[-1],
        "ruin_prob": ruin_prob
    }

def render_monte_carlo_ui(starting_capital: float, vault_data: dict | None = None):
    st.subheader("🎲 Simulasi Bootstrap P&L Jurnal")
    trade_pnls = get_realized_trade_pnls(vault_data)
    if not trade_pnls:
        st.info("Simulasi belum tersedia: jurnal sumber tiada P&L realisasi yang sah.")
        return
    st.caption(
        f"Simulasi mengambil sampel semula {len(trade_pnls)} P&L realisasi daripada jurnal. "
        "Ia bukan ramalan dan tidak menjamin hasil masa depan."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        sim_cap = st.number_input("Modal Permulaan Simulasi (MYR):", value=float(starting_capital), step=1000.0)
    with c2:
        sim_trades = st.slider("Unjuran Bilangan Dagangan Hadapan:", 50, 300, 100, step=25)
    with c3:
        sim_runs = st.select_slider("Bilangan Laluan Simulasi Rawak:", [500, 1000, 2500, 5000], value=1000)

    mc = run_monte_carlo_simulation(
        starting_capital=sim_cap,
        trade_pnls=trade_pnls,
        num_simulations=sim_runs,
        num_trades=sim_trades
    )

    # Paparan Metrik Hasil Simulasi
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Senario Median (50th %)", f"RM {mc['final_median']:,.2f}", f"+RM {mc['final_median']-sim_cap:,.2f}")
    with m2:
        st.metric("Senario Terbaik (95th %)", f"RM {mc['final_p95']:,.2f}", "+Prestasi Puncak")
    with m3:
        st.metric("Senario Terburuk (5th %)", f"RM {mc['final_p05']:,.2f}", "-Rintangan Maksimum", delta_color="inverse")
    with m4:
        st.metric("Anggaran baki < 50% modal", f"{mc['ruin_prob']:.2f}%")

    # Plot Carta Kipas Kebarangkalian (Probability Cone)
    fig_mc = go.Figure()
    
    # 30 sampel laluan rawak
    for i in range(min(40, sim_runs)):
        fig_mc.add_trace(go.Scatter(
            x=mc["trades"], y=mc["curves"][:, i],
            mode="lines", line=dict(color="rgba(142, 154, 175, 0.12)", width=1),
            showlegend=False, hoverinfo="skip"
        ))

    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p95"],
        mode="lines", line=dict(color="#00E676", width=2.5, dash="dash"),
        name="Senario Terbaik (95th Percentile)"
    ))
    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p50"],
        mode="lines", line=dict(color="#29B6F6", width=3),
        name="Trajektori Median (50th Percentile)"
    ))
    fig_mc.add_trace(go.Scatter(
        x=mc["trades"], y=mc["p05"],
        mode="lines", line=dict(color="#FF5252", width=2.5, dash="dash"),
        name="Senario Terburuk (5th Percentile)"
    ))

    fig_mc.update_layout(
        title=f"📈 Peta Kipas Kebarangkalian Ekuiti ({sim_trades} Dagangan Hadapan)",
        template="plotly_dark", paper_bgcolor="#141824", plot_bgcolor="#141824",
        height=420, margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(title="Bilangan Dagangan Seterusnya", gridcolor="#222B3D"),
        yaxis=dict(title="Nilai Ekuiti Bersih (MYR)", gridcolor="#222B3D", tickprefix="RM "),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_mc, width="stretch")


# ======================================================================================
# 2. ENJIN MATRIKS KORELASI & PENGESANAN RISIKO BERTINDIH
# ======================================================================================
def render_correlation_matrix_ui(vault_data: dict | None = None):
    st.subheader("⚡ Matriks Korelasi Saham & Pendedahan Risiko Kluster")
    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        st.info("Matriks tidak dipaparkan: tiada siri harga OHLCV bersumber tersedia.")
        return

    ticker_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("ticker", "symbol", "simbol"))),
        None,
    )
    date_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("date", "tarikh", "masa"))),
        None,
    )
    close_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("close", "tutup", "harga penutup"))),
        None,
    )
    if ticker_col is None or date_col is None or close_col is None:
        st.info("Matriks tidak dipaparkan: lajur ticker, tarikh dan harga tutup tiada dalam OHLCV.")
        return

    prices = source[[ticker_col, date_col, close_col]].copy()
    prices["_date"] = prices[date_col].map(_parse_market_date)
    prices["_close"] = _parse_numeric_series(prices[close_col])
    prices["_ticker"] = prices[ticker_col].astype(str).str.strip()
    prices = prices.dropna(subset=["_date", "_close"])
    prices = prices[(prices["_close"] > 0) & prices["_ticker"].ne("")]
    price_matrix = prices.pivot_table(
        index="_date",
        columns="_ticker",
        values="_close",
        aggfunc="last",
    ).sort_index()
    returns = price_matrix.pct_change(fill_method=None)
    eligible_assets = returns.columns[returns.count() >= 20]
    returns = returns[eligible_assets]
    if len(eligible_assets) < 2:
        st.info("Matriks belum tersedia: sekurang-kurangnya dua ticker dengan 20 pulangan harga diperlukan.")
        return
    df_corr = returns.corr(min_periods=20)
    df_corr = df_corr.dropna(axis=0, how="all").dropna(axis=1, how="all")
    if df_corr.shape[0] < 2:
        st.info("Matriks belum tersedia: sejarah harga bertindih tidak mencukupi.")
        return

    st.caption("Korelasi Pearson dikira daripada pulangan harga penutup yang tersedia; bukan jaminan hubungan masa depan.")
    fig_corr = px.imshow(
        df_corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        range_color=[-1.0, 1.0],
        title="Korelasi pulangan harga daripada cache OHLCV",
    )
    fig_corr.update_layout(
        template="plotly_dark", paper_bgcolor="#141824", plot_bgcolor="#141824",
        height=480, margin=dict(l=30, r=30, t=50, b=30)
    )
    st.plotly_chart(fig_corr, width="stretch")


# ======================================================================================
# 3. RADAR WYCKOFF & PENGIMBAS ANOMALI VOLUM (SMART MONEY RVOL)
# ======================================================================================
def get_wyckoff_rvol_data(vault_data: dict | None = None) -> pd.DataFrame:
    """Calculate RVOL from the latest source-backed OHLCV rows per ticker."""
    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame()

    ticker_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("ticker", "symbol", "simbol"))),
        None,
    )
    date_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("date", "tarikh", "masa"))),
        None,
    )
    volume_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("volume", "volum"))),
        None,
    )
    close_col = next(
        (c for c in source.columns if any(t in str(c).lower() for t in ("close", "tutup", "harga penutup"))),
        None,
    )
    if ticker_col is None or date_col is None or volume_col is None:
        return pd.DataFrame()

    history = source[[ticker_col, date_col, volume_col] + ([close_col] if close_col else [])].copy()
    history["_date"] = history[date_col].map(_parse_market_date)
    history["_volume"] = _parse_numeric_series(history[volume_col])
    history["_ticker"] = history[ticker_col].astype(str).str.strip()
    history = history.dropna(subset=["_date", "_volume"])
    history = history[history["_volume"] >= 0].sort_values("_date")
    if close_col:
        history["Harga tutup"] = _parse_numeric_series(history[close_col])

    results = []
    for ticker, rows in history.groupby("_ticker", sort=False):
        rows = rows.tail(21).copy()
        if len(rows) < 21:
            continue
        average_volume = rows["_volume"].iloc[:-1].mean()
        if average_volume <= 0:
            continue
        latest = rows.iloc[-1]
        result = {
            "Ticker": ticker,
            "Tarikh": latest["_date"],
            "Volum terkini": latest["_volume"],
            "Purata volum 20 hari": average_volume,
            "RVOL 20 hari": latest["_volume"] / average_volume,
        }
        if close_col:
            result["Harga tutup"] = latest.get("Harga tutup")
        results.append(result)
    if not results:
        return pd.DataFrame()
    return pd.DataFrame(results).sort_values("RVOL 20 hari", ascending=False)


def render_wyckoff_rvol_screener(vault_data: dict | None = None):
    st.subheader("🎯 Pengimbas anomali volum (RVOL)")
    results = get_wyckoff_rvol_data(vault_data)
    if results.empty:
        st.info(
            "RVOL tidak tersedia: perlukan ticker, tarikh dan sekurang-kurangnya "
            "21 rekod volum OHLCV bersumber."
        )
        return
    st.caption(
        "RVOL membandingkan volum rekod terakhir dengan purata 20 rekod sebelumnya; "
        "ia bukan bukti manipulasi atau isyarat beli/jual."
    )
    st.dataframe(
        results,
        width="stretch",
        hide_index=True,
        alt="Nisbah volum relatif dikira daripada cache OHLCV",
    )


# ======================================================================================
# 4. KALENDAR EARNINGS & UNJURAN DIVIDEN
# ======================================================================================
def render_earnings_dividend_hub(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
):
    st.subheader("📅 Kalendar Laporan Pendapatan (Earnings) & Unjuran Dividen")
    earnings = (vault_data or {}).get("cache_earnings")
    if not isinstance(earnings, pd.DataFrame) or earnings.empty:
        earnings = (vault_data or {}).get("72_Cache Earnings")
    if isinstance(earnings, pd.DataFrame) and not earnings.empty:
        st.subheader("Data earnings daripada cache Google Sheets")
        st.dataframe(earnings, width="stretch", hide_index=True)
    else:
        st.info("Kalendar earnings tidak tersedia: tab 72_Cache Earnings tiada data.")
    st.subheader("Dividen")
    st.info("Unjuran dividen tidak dipaparkan kerana sumber jadual dividen berserta DPS/tarikh belum dikonfigurasikan.")
