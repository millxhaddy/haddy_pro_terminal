"""Google Sheets-backed portfolio holdings and allocation views."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Optional
from pipeline_cleaner import clean_currency

def get_active_holdings(vault_data=None, fx_rate: float = 4.0773) -> pd.DataFrame:
    """Normalize active positions from the Google Sheets holdings tab."""
    columns = [
        "Ticker", "Nama_Syarikat", "Pasaran", "Mata_Wang", "Sektor", "Unit",
        "Kos_Purata", "Harga_Semasa", "Nilai_Modal_MYR", "Nilai_Semasa_MYR",
        "Untung_Rugi_MYR", "ROI_Pct", "Status_Teknikal", "Zon_Sokongan", "Sasaran_TP",
    ]
    metadata = (vault_data or {}).get("_sync_metadata", {})
    tab_sources = metadata.get("tab_sources", {})
    cache_timestamps = metadata.get("tab_cache_timestamps", {})
    metadata = dict(metadata)
    metadata["holding_source"] = tab_sources.get(
        "pegangan_semasa", metadata.get("source_tier", "Unknown")
    )
    metadata["holding_cache_timestamp"] = cache_timestamps.get("pegangan_semasa")
    metadata["holding_retrieved_at"] = (
        metadata["holding_cache_timestamp"]
        if metadata["holding_source"] == "local cache"
        else metadata.get("timestamp")
    )
    source_df = (vault_data or {}).get("active_holdings_raw_df")
    if not isinstance(source_df, pd.DataFrame):
        source_df = (vault_data or {}).get("pegangan_semasa")
    if not isinstance(source_df, pd.DataFrame) or source_df.empty:
        result = pd.DataFrame(columns=columns)
        result.attrs.update(metadata)
        result.attrs["quote_timestamp_available"] = False
        return result

    def find_column(*terms):
        return next(
            (column for column in source_df.columns if any(term in str(column).lower() for term in terms)),
            None,
        )

    ticker_col = find_column("ticker", "simbol")
    qty_col = find_column("kuantiti", "quantity", "unit", "shares")
    if ticker_col is None or qty_col is None:
        result = pd.DataFrame(columns=columns)
        result.attrs.update(metadata)
        result.attrs["quote_timestamp_available"] = False
        return result

    name_col = find_column("nama syarikat", "company")
    market_col = find_column("pasaran", "market")
    sector_col = find_column("sektor", "sector")
    price_col = find_column("harga rujukan", "harga semasa", "live price", "current price")
    cost_col = find_column("kos purata", "average cost", "harga beli")
    market_value_col = find_column("nilai pasaran", "market value")
    pnl_col = find_column("untung/rugi belum realisasi", "unrealized", "p&l")
    support_col = find_column("had entri", "sokongan", "support")
    target_col = find_column("harga jual", "sasaran", "target")
    status_col = find_column("keputusan akhir", "status")
    timestamp_col = find_column(
        "masa sebut harga",
        "quote time",
        "price timestamp",
        "kemas kini harga",
    )

    normalized_rows = []
    for _, row in source_df.iterrows():
        ticker = str(row.get(ticker_col, "")).strip()
        if not ticker or ticker.lower() in {"nan", "none", "-"}:
            continue

        quantity = clean_currency(row.get(qty_col))
        average_cost = clean_currency(row.get(cost_col)) if cost_col else 0.0
        market_value = clean_currency(row.get(market_value_col)) if market_value_col else 0.0
        pnl_raw = row.get(pnl_col) if pnl_col else None
        pnl_text = str(pnl_raw).strip().upper() if pnl_raw is not None else ""
        pnl_is_missing = (
            pnl_raw is None
            or pd.isna(pnl_raw)
            or pnl_text in {"", "-", "N/A", "NAN"}
        )
        pnl_has_formula_error = pnl_text.startswith("#")
        unrealized_pnl = (
            float("nan")
            if pnl_has_formula_error
            else clean_currency(pnl_raw) if not pnl_is_missing else 0.0
        )
        price = clean_currency(row.get(price_col)) if price_col else float("nan")
        raw_market = str(row.get(market_col, "")).strip() if market_col else ""
        is_us = "US" in raw_market.upper() or ticker.upper().startswith(("NYSE:", "NASDAQ:", "AMEX:"))
        market = "Wall Street US" if is_us else "Bursa Malaysia"
        currency = "USD" if is_us else "MYR"
        cost_basis_myr = quantity * average_cost * (fx_rate if is_us else 1.0)

        has_market_value = market_value > 0
        has_price = pd.notna(price) and price > 0
        if quantity <= 0 or (not has_market_value and not has_price):
            continue
        if not has_market_value and has_price:
            market_value = quantity * price * (fx_rate if is_us else 1.0)
        if pnl_is_missing and market_value > 0 and cost_basis_myr > 0:
            unrealized_pnl = market_value - cost_basis_myr
        roi_pct = (
            unrealized_pnl / cost_basis_myr * 100
            if cost_basis_myr > 0 and pd.notna(unrealized_pnl)
            else float("nan")
        )

        normalized_rows.append(
            {
                "Ticker": ticker,
                "Nama_Syarikat": str(row.get(name_col, ticker)).strip() if name_col else ticker,
                "Pasaran": market or ("Wall Street US" if is_us else "Bursa Malaysia"),
                "Mata_Wang": currency,
                "Sektor": str(row.get(sector_col, "")).strip() if sector_col else "",
                "Unit": quantity,
                "Kos_Purata": average_cost,
                "Harga_Semasa": price,
                "Nilai_Modal_MYR": cost_basis_myr,
                "Nilai_Semasa_MYR": market_value,
                "Untung_Rugi_MYR": unrealized_pnl,
                "ROI_Pct": roi_pct,
                "Status_Teknikal": str(row.get(status_col, "")).strip() if status_col else "",
                "Zon_Sokongan": str(row.get(support_col, "")).strip() if support_col else "",
                "Sasaran_TP": str(row.get(target_col, "")).strip() if target_col else "",
            }
        )

    result = pd.DataFrame(normalized_rows, columns=columns)
    if not result.empty:
        result = result.groupby(
            ["Ticker", "Pasaran"], as_index=False, sort=False
        ).agg(
            {
                "Nama_Syarikat": "first",
                "Mata_Wang": "first",
                "Sektor": "first",
                "Unit": "sum",
                "Kos_Purata": "first",
                "Harga_Semasa": "first",
                "Nilai_Modal_MYR": "sum",
                "Nilai_Semasa_MYR": "sum",
                "Untung_Rugi_MYR": lambda values: values.sum(min_count=1),
                "ROI_Pct": "first",
                "Status_Teknikal": "first",
                "Zon_Sokongan": "first",
                "Sasaran_TP": "first",
            }
        )
        for index, row in result.iterrows():
            multiplier = fx_rate if row["Mata_Wang"] == "USD" else 1.0
            cost_basis = float(row["Nilai_Modal_MYR"])
            quantity = float(row["Unit"])
            if quantity > 0 and multiplier > 0 and cost_basis > 0:
                result.at[index, "Kos_Purata"] = cost_basis / quantity / multiplier
            result.at[index, "ROI_Pct"] = (
                float(row["Untung_Rugi_MYR"]) / cost_basis * 100
                if cost_basis > 0 and pd.notna(row["Untung_Rugi_MYR"])
                else float("nan")
            )
    result.attrs.update(metadata)
    latest_quote_timestamp = None
    if timestamp_col:
        parsed_timestamps = pd.to_datetime(source_df[timestamp_col], errors="coerce")
        valid_timestamps = parsed_timestamps.dropna()
        if not valid_timestamps.empty:
            try:
                latest_quote_timestamp = valid_timestamps.max().isoformat()
            except TypeError:
                latest_quote_timestamp = None
    result.attrs["quote_timestamp_available"] = latest_quote_timestamp is not None
    result.attrs["latest_quote_timestamp"] = latest_quote_timestamp
    return result

def render_allocation_donut(df_holdings: pd.DataFrame, cash_balance: Optional[float] = None):
    labels = []
    values = []
    colors = ["#F87171", "#FB923C", "#34D399", "#60A5FA", "#A78BFA", "#22D3EE"]

    for _, row in df_holdings.iterrows():
        labels.append(f"{row['Nama_Syarikat']} ({row['Pasaran']})")
        values.append(row["Nilai_Semasa_MYR"])

    if cash_balance is not None and cash_balance > 0:
        labels.append("Baki Tunai")
        values.append(cash_balance)

    if not values:
        return go.Figure()

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(
            colors=[colors[index % len(colors)] for index in range(len(values))],
            line=dict(color="#141824", width=3),
        ),
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        textfont=dict(color="#FFFFFF", size=12),
        hovertemplate="<b>%{label}</b><br>Nilai: <b>RM %{value:,.2f}</b><br>Porsi: <b>%{percent}</b><extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="Pecahan nilai pegangan saham", font=dict(size=14, color="#FFFFFF")),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#8E9AAF", size=10))
    )
    return fig

def render_holdings_cards(df_holdings: pd.DataFrame):
    if df_holdings.empty:
        st.info("Tiada pegangan yang dapat dibaca daripada tab Google Sheets semasa.")
        return

    columns = st.columns(min(2, len(df_holdings)))
    for index, (_, row) in enumerate(df_holdings.iterrows()):
        with columns[index % len(columns)]:
            with st.container(border=True):
                st.subheader(str(row["Ticker"]))
                st.caption(f"{row['Nama_Syarikat']} · {row['Pasaran']}")
                metrics = st.columns(2)
                metrics[0].metric("Unit", f"{row['Unit']:,.0f}")
                roi_display = (
                    f"{row['ROI_Pct']:+.2f}%"
                    if pd.notna(row["ROI_Pct"])
                    else "Tidak tersedia"
                )
                pnl_display = (
                    f"RM {row['Untung_Rugi_MYR']:,.2f}"
                    if pd.notna(row["Untung_Rugi_MYR"])
                    else None
                )
                metrics[1].metric(
                    "ROI berbanding kos",
                    roi_display,
                    delta=pnl_display,
                    delta_color="normal",
                )
                price_display = (
                    f"{row['Mata_Wang']} {row['Harga_Semasa']:,.4f}"
                    if pd.notna(row["Harga_Semasa"])
                    else "Tiada data harga"
                )
                st.write(
                    f"Nilai pasaran: **RM {row['Nilai_Semasa_MYR']:,.2f}**  \n"
                    f"Harga rujukan Sheets: **{price_display}**"
                )
                if row["Status_Teknikal"]:
                    st.caption(str(row["Status_Teknikal"]))