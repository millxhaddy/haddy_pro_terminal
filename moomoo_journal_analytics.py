"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 17 & 18: PENJANA PESANAN MOOMOO & ANALITIK DISIPLIN JURNAL DAGANGAN
========================================================================================
"""

import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px
from pipeline_cleaner import clean_currency

# --------------------------------------------------------------------------------------
# FASA 17: PENJANA RENTETAN PESANAN BROKER MOOMOO (ORDER STRING GENERATOR)
# --------------------------------------------------------------------------------------
def generate_moomoo_order_payload(
    ticker: str,
    market: str,
    order_type: str,
    units: int,
    limit_price: float,
    stop_loss_price: float,
    take_profit_price: float,
    session: str = "Regular Hours"
) -> dict:
    """
    Menjana payload teks berformat rasmi Moomoo OpenD / Universal Account.
    """
    currency = "MYR" if "BURSA" in market.upper() or "KLSE" in ticker.upper() else "USD"
    lots = units // 100 if currency == "MYR" else units
    
    order_summary_text = (
        f"MOOMOO ORDER TICKET\n"
        f"----------------------------------------\n"
        f"Account       : Universal Account (8702)\n"
        f"Symbol        : {ticker.upper()}\n"
        f"Market        : {market}\n"
        f"Action        : BUY (Long Entry)\n"
        f"Order Type    : {order_type}\n"
        f"Quantity      : {units:,} Units ({lots} Lots)\n"
        f"Limit Price   : {currency} {limit_price:.2f}\n"
        f"Stop Loss     : {currency} {stop_loss_price:.2f}\n"
        f"Target TP     : {currency} {take_profit_price:.2f}\n"
        f"Time-In-Force : Day Order\n"
        f"Session       : {session}\n"
        f"Discipline    : DDNK 3M Compliant (SL Locked)\n"
        f"----------------------------------------"
    )
    
    return {
        "summary_text": order_summary_text,
        "ticker": ticker.upper(),
        "units": units,
        "lots": lots,
        "currency": currency,
        "total_cost": units * limit_price
    }

def render_moomoo_order_generator():
    """
    Antara muka interaktif penjana pesanan Moomoo dengan salin pantas.
    """
    st.markdown("""
    <style>
        .order-card {
            background: linear-gradient(135deg, #1A1F2C 0%, #151A26 100%);
            border: 1px solid #2B354C;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns([5, 5])

    with col_in:
        st.markdown('<div class="order-card">', unsafe_allow_html=True)
        st.subheader("🛒 Konfigurasi Pesanan Broker Moomoo")
        
        m_type = st.radio("Pilih Pasaran Broker:", ["🇲🇾 Bursa Malaysia (Universal MY)", "🇺🇸 Wall Street US (Universal US)"], horizontal=True)
        is_bursa = "Bursa" in m_type
        
        default_sym = "KLSE:TENAGA" if is_bursa else "NASDAQ:NVDA"
        default_px = 12.75 if is_bursa else 141.20
        default_sl = 12.10 if is_bursa else 134.00
        default_tp = 14.38 if is_bursa else 161.36
        default_qty = 500 if is_bursa else 25
        
        t_sym = st.text_input("Kod Saham (Ticker):", default_sym)
        o_type = st.selectbox("Jenis Pesanan Moomoo:", ["Limit Order (Had Harga - Disyorkan)", "Stop-Limit Order", "Market Order (Elakkan FOMO)"])
        
        c1, c2 = st.columns(2)
        with c1:
            qty_val = st.number_input("Kuantiti (Unit):", value=default_qty, step=100 if is_bursa else 5)
        with c2:
            lim_px = st.number_input("Had Harga Entri:", value=default_px, step=0.05, format="%.2f")
            
        c3, c4 = st.columns(2)
        with c3:
            sl_val = st.number_input("Paras Stop Loss:", value=default_sl, step=0.05, format="%.2f")
        with c4:
            tp_val = st.number_input("Sasaran Ambil Untung:", value=default_tp, step=0.05, format="%.2f")
            
        st.markdown('</div>', unsafe_allow_html=True)

    payload = generate_moomoo_order_payload(
        ticker=t_sym,
        market="Bursa Malaysia" if is_bursa else "US Wall Street",
        order_type="Limit" if "Limit" in o_type else "Market",
        units=int(qty_val),
        limit_price=lim_px,
        stop_loss_price=sl_val,
        take_profit_price=tp_val
    )

    with col_out:
        st.markdown('<div class="order-card">', unsafe_allow_html=True)
        st.subheader("📋 Tiket Pesanan Moomoo (Sedia Salin)")
        
        st.code(payload["summary_text"], language="yaml")
        
        st.metric(
            "Anggaran Nilai Transaksi",
            f"{payload['currency']} {payload['total_cost']:,.2f}",
            f"{payload['lots']} Lot ({payload['units']:,} Unit)"
        )
        
        st.success("✅ **SOP Disiplin Disahkan:** Pesanan dilengkapi paras Stop Loss terikat bagi melindungi akaun daripada penarikan modal besar.")
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# FASA 18: ANALITIK DISIPLIN & PSIKOLOGI JURNAL DAGANGAN (MIND 60%)
# --------------------------------------------------------------------------------------
def get_realized_trade_pnls(vault_data: dict | None) -> list[float]:
    """Return finite realized P&L values from the journal, skipping blanks and formula errors."""
    journal = (vault_data or {}).get("jurnal_dagangan_df")
    if not isinstance(journal, pd.DataFrame) or journal.empty:
        return []

    pnl_col = next(
        (
            column
            for column in journal.columns
            if "untung bersih" in str(column).strip().lower()
            or str(column).strip().lower() in {"pnl", "p&l", "realized pnl"}
        ),
        None,
    )
    if pnl_col is None:
        return []

    values = []
    for raw_value in journal[pnl_col]:
        parsed_value = _parse_realized_pnl(raw_value)
        if parsed_value is not None:
            values.append(parsed_value)
    return values


def _parse_realized_pnl(value) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text or text.upper() in {"-", "N/A", "NAN", "NONE"} or text.startswith("#"):
        return None
    if not any(character.isdigit() for character in text):
        return None
    parsed = float(clean_currency(value))
    return parsed if math.isfinite(parsed) else None


def get_journal_analytics_data(vault_data: dict | None = None) -> dict:
    """Calculate journal performance only from realized P&L present in the source snapshot."""
    empty_metrics = {
        "profit_factor": None,
        "win_rate_pct": None,
        "avg_win": None,
        "avg_loss": None,
        "payoff_ratio": None,
        "expectancy_myr": None,
        "max_gain": None,
        "max_drawdown": None,
        "total_trades": 0,
        "net_pnl_myr": None,
    }
    empty_discipline = pd.DataFrame(
        columns=["Kategori", "Bilangan", "Untung_Bersih_MYR", "Peratus_Bilangan"]
    )
    empty_market = pd.DataFrame(
        columns=["Pasaran", "Untung_MYR", "Rugi_MYR", "Bersih_MYR"]
    )
    journal = (vault_data or {}).get("jurnal_dagangan_df")
    trade_pnls = get_realized_trade_pnls(vault_data)
    if not trade_pnls:
        return {
            "discipline": empty_discipline,
            "metrics": empty_metrics,
            "market_pnl": empty_market,
            "trade_pnls": [],
        }

    pnl = pd.Series(trade_pnls, dtype="float64")
    winners = pnl[pnl > 0]
    losers = pnl[pnl < 0]
    gross_profit = float(winners.sum())
    gross_loss = float(abs(losers.sum()))
    categories = [
        ("Untung", winners),
        ("Rugi", losers),
        ("Pulang modal", pnl[pnl == 0]),
    ]
    discipline = pd.DataFrame(
        [
            {
                "Kategori": label,
                "Bilangan": int(len(values)),
                "Untung_Bersih_MYR": float(values.sum()),
                "Peratus_Bilangan": float(len(values) / len(pnl) * 100),
            }
            for label, values in categories
        ]
    )
    cumulative = pnl.cumsum()
    max_drawdown = float((cumulative - cumulative.cummax().clip(lower=0)).min())
    avg_win = float(winners.mean()) if not winners.empty else None
    avg_loss = float(losers.mean()) if not losers.empty else None
    metrics = {
        "profit_factor": gross_profit / gross_loss if gross_loss else None,
        "win_rate_pct": float(len(winners) / len(pnl) * 100),
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": avg_win / abs(avg_loss) if avg_win is not None and avg_loss else None,
        "expectancy_myr": float(pnl.mean()),
        "max_gain": float(pnl.max()),
        "max_drawdown": max_drawdown,
        "total_trades": int(len(pnl)),
        "net_pnl_myr": float(pnl.sum()),
    }

    market_col = next(
        (
            column
            for column in journal.columns
            if any(term in str(column).strip().lower() for term in ("pasaran", "market"))
        ),
        None,
    )
    pnl_col = next(
        (
            column
            for column in journal.columns
            if "untung bersih" in str(column).strip().lower()
            or str(column).strip().lower() in {"pnl", "p&l", "realized pnl"}
        ),
        None,
    )
    market_pnl = empty_market
    if market_col is not None and pnl_col is not None:
        rows = []
        for market, raw_value in zip(journal[market_col], journal[pnl_col]):
            value = _parse_realized_pnl(raw_value)
            if value is None:
                continue
            if value > 0:
                profit, loss = value, 0.0
            else:
                profit, loss = 0.0, value
            rows.append(
                {
                    "Pasaran": str(market).strip() or "Tidak dinyatakan",
                    "Untung_MYR": profit,
                    "Rugi_MYR": loss,
                }
            )
        if rows:
            market_pnl = pd.DataFrame(rows).groupby("Pasaran", as_index=False).agg(
                Untung_MYR=("Untung_MYR", "sum"),
                Rugi_MYR=("Rugi_MYR", "sum"),
            )
            market_pnl["Bersih_MYR"] = market_pnl["Untung_MYR"] + market_pnl["Rugi_MYR"]

    return {
        "discipline": discipline,
        "metrics": metrics,
        "market_pnl": market_pnl,
        "trade_pnls": trade_pnls,
    }


def render_journal_analytics_dashboard(vault_data: dict | None = None):
    """Render realized trade analytics from the supplied Google Sheets snapshot."""
    data = get_journal_analytics_data(vault_data)
    metrics = data["metrics"]
    if not metrics["total_trades"]:
        st.info("Analitik jurnal belum tersedia: tiada nilai Untung Bersih yang sah dalam snapshot jurnal.")
        return

    def format_metric(value, suffix=""):
        return "Tidak tersedia" if value is None else f"{value:,.2f}{suffix}"

    columns = st.columns(4)
    columns[0].metric("Profit factor", format_metric(metrics["profit_factor"], "x"))
    columns[1].metric("Kadar menang", format_metric(metrics["win_rate_pct"], "%"))
    columns[2].metric("Jangkaan per dagangan", f"RM {format_metric(metrics['expectancy_myr'])}")
    columns[3].metric("Untung/rugi realisasi", f"RM {format_metric(metrics['net_pnl_myr'])}")
    st.caption(f"Dikira daripada {metrics['total_trades']} rekod jurnal dengan P&L tersedia.")

    col_outcomes, col_markets = st.columns(2)
    with col_outcomes:
        st.subheader("Hasil dagangan dalam jurnal")
        st.dataframe(data["discipline"], width="stretch", hide_index=True)
        outcome_data = data["discipline"].loc[data["discipline"]["Bilangan"] > 0]
        if not outcome_data.empty:
            figure = px.pie(
                outcome_data,
                names="Kategori",
                values="Bilangan",
                hole=0.55,
                color="Kategori",
                color_discrete_map={
                    "Untung": "#00E676",
                    "Rugi": "#FF5252",
                    "Pulang modal": "#29B6F6",
                },
            )
            figure.update_layout(
                template="plotly_dark",
                paper_bgcolor="#141824",
                plot_bgcolor="#141824",
                height=340,
                margin=dict(l=20, r=20, t=30, b=20),
                showlegend=False,
            )
            st.plotly_chart(figure, width="stretch")
    with col_markets:
        st.subheader("Untung/rugi mengikut pasaran")
        if data["market_pnl"].empty:
            st.info("Data pasaran tidak tersedia dalam rekod jurnal yang boleh dikira.")
        else:
            st.dataframe(data["market_pnl"], width="stretch", hide_index=True)
            figure = go.Figure()
            figure.add_trace(go.Bar(x=data["market_pnl"]["Pasaran"], y=data["market_pnl"]["Untung_MYR"], name="Untung"))
            figure.add_trace(go.Bar(x=data["market_pnl"]["Pasaran"], y=data["market_pnl"]["Rugi_MYR"], name="Rugi"))
            figure.update_layout(
                template="plotly_dark",
                paper_bgcolor="#141824",
                plot_bgcolor="#141824",
                barmode="group",
                height=340,
                yaxis=dict(tickprefix="RM "),
            )
            st.plotly_chart(figure, width="stretch")
