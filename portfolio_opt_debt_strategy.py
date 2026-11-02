"""Source-backed portfolio risk analysis and liability prioritization."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from advanced_quant_suite import _parse_market_date, _parse_numeric_series
from pipeline_cleaner import clean_currency
from portfolio_holdings import get_active_holdings


def _find_column(dataframe: pd.DataFrame, terms: tuple[str, ...]):
    return next(
        (
            column
            for column in dataframe.columns
            if any(term in str(column).strip().lower() for term in terms)
        ),
        None,
    )


def _source_ohlcv(vault_data: dict | None) -> pd.DataFrame:
    source = (vault_data or {}).get("cache_ohlcv")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("71_Cache OHLCV")
    if not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame()

    ticker_col = _find_column(source, ("ticker", "symbol", "simbol"))
    date_col = _find_column(source, ("date", "tarikh", "masa"))
    close_col = _find_column(source, ("close", "tutup", "harga penutup"))
    if ticker_col is None or date_col is None or close_col is None:
        return pd.DataFrame()

    prices = source[[ticker_col, date_col, close_col]].copy()
    prices["_ticker"] = prices[ticker_col].astype(str).str.strip()
    prices["_date"] = prices[date_col].map(_parse_market_date)
    prices["_close"] = _parse_numeric_series(prices[close_col])
    prices = prices.dropna(subset=["_date", "_close"])
    prices = prices[(prices["_ticker"] != "") & (prices["_close"] > 0)]
    prices = prices.sort_values("_date").drop_duplicates(
        ["_ticker", "_date"], keep="last"
    )
    return prices.pivot(index="_date", columns="_ticker", values="_close").sort_index()


def generate_efficient_frontier_simulation(
    num_portfolios: int = 1500,
    vault_data: dict | None = None,
    risk_free_rate_pct: float = 0.0,
    fx_rate: float = 4.0773,
) -> dict | None:
    """Estimate a long-only frontier from overlapping source-backed daily returns."""
    if num_portfolios <= 0:
        raise ValueError("Bilangan portfolio mesti positif.")
    prices = _source_ohlcv(vault_data)
    if prices.empty:
        return None

    daily_returns = prices.pct_change(fill_method=None)
    overlapping = daily_returns.dropna(axis=0, how="any")
    if len(overlapping) < 20 or overlapping.shape[1] < 2:
        return None

    assets = list(overlapping.columns)
    expected_returns = overlapping.mean().to_numpy() * 252
    covariance = overlapping.cov().to_numpy() * 252
    if not np.isfinite(expected_returns).all() or not np.isfinite(covariance).all():
        return None

    rng = np.random.default_rng(42)
    weights = rng.dirichlet(np.ones(len(assets)), size=num_portfolios)
    annual_returns = weights @ expected_returns
    annual_volatility = np.sqrt(
        np.einsum("ij,jk,ik->i", weights, covariance, weights)
    )
    sharpe_ratios = np.divide(
        annual_returns - risk_free_rate_pct / 100,
        annual_volatility,
        out=np.zeros_like(annual_returns),
        where=annual_volatility > 0,
    )
    max_sharpe_idx = int(np.argmax(sharpe_ratios))
    min_vol_idx = int(np.argmin(annual_volatility))

    def portfolio_result(index: int) -> dict:
        return {
            "return": annual_returns[index],
            "volatility": annual_volatility[index],
            "sharpe": sharpe_ratios[index],
            "weights": weights[index],
        }

    current = None
    holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
    if not holdings.empty:
        values_by_ticker = (
            holdings.assign(_ticker=holdings["Ticker"].astype(str).str.strip())
            .groupby("_ticker")["Nilai_Semasa_MYR"]
            .sum()
        )
        matched_values = np.array(
            [float(values_by_ticker.get(ticker, 0.0)) for ticker in assets]
        )
        if matched_values.sum() > 0:
            current_weights = matched_values / matched_values.sum()
            current_return = float(current_weights @ expected_returns)
            current_volatility = float(
                np.sqrt(current_weights @ covariance @ current_weights)
            )
            current = {
                "return": current_return,
                "volatility": current_volatility,
                "sharpe": (
                    (current_return - risk_free_rate_pct / 100) / current_volatility
                    if current_volatility > 0
                    else 0.0
                ),
                "weights": current_weights,
            }

    return {
        "assets": assets,
        "returns": annual_returns,
        "volatilities": annual_volatility,
        "sharpe_ratios": sharpe_ratios,
        "max_sharpe": portfolio_result(max_sharpe_idx),
        "min_vol": portfolio_result(min_vol_idx),
        "current": current,
    }


def render_markowitz_efficient_frontier_ui(
    vault_data: dict | None = None,
    fx_rate: float = 4.0773,
):
    st.subheader("Frontier portfolio daripada pulangan sejarah")
    risk_free_rate_pct = st.number_input(
        "Andaian kadar bebas risiko tahunan (%)",
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=0.25,
    )
    simulation = generate_efficient_frontier_simulation(
        num_portfolios=1200,
        vault_data=vault_data,
        risk_free_rate_pct=risk_free_rate_pct,
        fx_rate=fx_rate,
    )
    if simulation is None:
        st.info(
            "Analisis tidak tersedia: perlukan sekurang-kurangnya dua ticker dengan "
            "20 pulangan harian bertindih dalam cache OHLCV."
        )
        return

    st.caption(
        "Pulangan dan kovarians dianualkan daripada sejarah yang tersedia. "
        "Hasil bukan ramalan atau cadangan agihan."
    )
    summaries = [("Max Sharpe sejarah", simulation["max_sharpe"]), ("Volatiliti minimum", simulation["min_vol"])]
    if simulation["current"] is not None:
        summaries.insert(0, ("Pegangan semasa yang sepadan", simulation["current"]))
    columns = st.columns(len(summaries))
    for column, (label, result) in zip(columns, summaries):
        column.metric(
            label,
            f"Pulangan {result['return']:.1%}",
            delta=f"Volatiliti {result['volatility']:.1%}",
        )

    figure = go.Figure()
    figure.add_scatter(
        x=simulation["volatilities"] * 100,
        y=simulation["returns"] * 100,
        mode="markers",
        marker={"color": simulation["sharpe_ratios"], "colorscale": "Viridis", "size": 6},
        name="Gabungan berat simulasi",
    )
    for label, key, symbol in (
        ("Max Sharpe sejarah", "max_sharpe", "star"),
        ("Volatiliti minimum", "min_vol", "circle"),
    ):
        result = simulation[key]
        figure.add_scatter(
            x=[result["volatility"] * 100],
            y=[result["return"] * 100],
            mode="markers",
            marker={"size": 13, "symbol": symbol},
            name=label,
        )
    current = simulation["current"]
    if current is not None:
        figure.add_scatter(
            x=[current["volatility"] * 100],
            y=[current["return"] * 100],
            mode="markers",
            marker={"size": 13, "symbol": "diamond"},
            name="Pegangan semasa sepadan",
        )
    figure.update_layout(
        title="Pulangan sejarah berbanding volatiliti tahunan",
        xaxis_title="Volatiliti sejarah (%)",
        yaxis_title="Pulangan sejarah (%)",
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=450,
    )
    st.plotly_chart(
        figure,
        width="stretch",
        alt="Gabungan portfolio berdasarkan pulangan sejarah OHLCV",
    )

    weight_rows = []
    for index, ticker in enumerate(simulation["assets"]):
        row = {
            "Ticker": ticker,
            "Max Sharpe sejarah (%)": simulation["max_sharpe"]["weights"][index] * 100,
            "Volatiliti minimum (%)": simulation["min_vol"]["weights"][index] * 100,
        }
        if current is not None:
            row["Pegangan semasa (%)"] = current["weights"][index] * 100
        weight_rows.append(row)
    st.dataframe(
        pd.DataFrame(weight_rows),
        width="stretch",
        hide_index=True,
        alt="Berat portfolio untuk gabungan yang dikira daripada data sejarah",
    )


def render_debt_payoff_strategies_ui(vault_data: dict | None = None):
    """Compare source-provided liabilities without inventing pay-off dates or rates."""
    st.subheader("Keutamaan lejar liabiliti")
    st.caption(
        "Paparan ini tidak mengira tempoh pelunasan atau penjimatan faedah. "
        "Sahkan baki, kadar dan ansuran dengan pemberi pinjaman."
    )
    source = (vault_data or {}).get("ccris_facilities")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("10_Lejar Liabiliti")
    if not isinstance(source, pd.DataFrame) or source.empty:
        st.info("Tiada rekod liabiliti dalam snapshot semasa.")
        return

    facility_col = _find_column(
        source, ("fasiliti", "facility", "institusi", "institution", "pemberi pinjaman")
    )
    balance_col = _find_column(
        source, ("baki semasa", "outstanding balance", "current balance")
    )
    rate_col = _find_column(
        source, ("kadar faedah", "kadar keuntungan", "interest rate", "profit rate", "kadar")
    )
    if balance_col is None:
        st.warning("Lajur baki tidak dikenal pasti; paparan rekod mentah sahaja.")
        st.dataframe(source, width="stretch", hide_index=True)
        return

    normalized = source.copy()
    balance_text = normalized[balance_col].astype(str).str.strip()
    valid_balance = (
        normalized[balance_col].notna()
        & balance_text.str.contains(r"\d", regex=True)
        & ~balance_text.str.startswith("#")
    )
    normalized["Baki daripada sumber (RM)"] = (
        normalized[balance_col].map(clean_currency).where(valid_balance)
    )
    if normalized["Baki daripada sumber (RM)"].notna().sum() == 0:
        st.info("Tiada amaun baki sah untuk disusun; nilai sumber tidak boleh dibaca.")
        st.dataframe(source, width="stretch", hide_index=True)
        return
    facility_name = (
        normalized[facility_col].astype(str)
        if facility_col is not None
        else pd.Series(normalized.index.astype(str), index=normalized.index)
    )
    normalized["Fasiliti"] = facility_name
    st.dataframe(
        normalized,
        width="stretch",
        hide_index=True,
        alt="Lejar liabiliti daripada Google Sheets",
    )

    snowball = normalized.sort_values("Baki daripada sumber (RM)", ascending=True)
    st.subheader("Susunan baki terendah dahulu")
    st.dataframe(
        snowball[["Fasiliti", "Baki daripada sumber (RM)"]],
        width="stretch",
        hide_index=True,
        alt="Liabiliti diisih mengikut baki sumber terendah",
    )
    if rate_col is None:
        st.info("Susunan kadar tertinggi tidak tersedia: lejar tiada lajur kadar yang dikenal pasti.")
    else:
        rate_values = normalized[rate_col].astype(str).str.replace("%", "", regex=False)
        normalized["Kadar daripada sumber (%)"] = pd.to_numeric(
            rate_values.str.replace(",", ".", regex=False), errors="coerce"
        )
        if normalized["Kadar daripada sumber (%)"].notna().any():
            avalanche = normalized.dropna(
                subset=["Kadar daripada sumber (%)"]
            ).sort_values("Kadar daripada sumber (%)", ascending=False)
            st.subheader("Susunan kadar tertinggi dahulu")
            st.dataframe(
                avalanche[
                    ["Fasiliti", "Baki daripada sumber (RM)", "Kadar daripada sumber (%)"]
                ],
                width="stretch",
                hide_index=True,
                alt="Liabiliti diisih mengikut kadar sumber tertinggi",
            )
        else:
            st.info("Data kadar wujud tetapi tiada nilai berangka yang boleh dibaca.")
