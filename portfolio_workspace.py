"""Portfolio source status, confirmed trade logging, and journal exports."""

import io
import math
import re
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st

from gsheets_sync import sync_record_trade


def prepare_trade_confirmation(
    *,
    is_buy: bool,
    ticker: str,
    market: str,
    quantity: int,
    price: float,
    average_cost: float = 0.0,
    fx_rate: float = 4.0773,
    fees_myr: float = 0.0,
    notes: str = "",
) -> dict:
    """Validate a proposed transaction and prepare its review summary."""
    try:
        quantity_value = float(quantity)
        price_value = float(price)
        average_cost_value = float(average_cost)
        fx_rate_value = float(fx_rate)
        fees_value = float(fees_myr)
    except (TypeError, ValueError) as exc:
        raise ValueError("Kuantiti, harga, kadar FX dan yuran mesti nombor sah.") from exc

    ticker = ticker.strip().upper()
    if not ticker:
        raise ValueError("Ticker diperlukan.")
    if market not in {"Bursa Malaysia", "Wall Street US"}:
        raise ValueError("Pasaran tidak disokong.")
    if (
        isinstance(quantity, bool)
        or not math.isfinite(quantity_value)
        or int(quantity_value) != quantity_value
        or quantity_value <= 0
    ):
        raise ValueError("Kuantiti mesti integer positif.")
    if not math.isfinite(price_value) or price_value <= 0:
        raise ValueError("Harga transaksi mesti nombor positif.")
    if not math.isfinite(average_cost_value) or average_cost_value < 0:
        raise ValueError("Kos purata tidak sah.")
    if not math.isfinite(fx_rate_value) or fx_rate_value <= 0:
        raise ValueError("Kadar FX tidak sah.")
    if not math.isfinite(fees_value) or fees_value < 0:
        raise ValueError("Yuran mesti sifar atau positif.")

    multiplier = fx_rate_value if market == "Wall Street US" else 1.0
    pnl_myr = (
        ((price_value - average_cost_value) * quantity_value * multiplier) - fees_value
        if not is_buy
        else 0.0
    )
    return {
        "is_buy": is_buy,
        "ticker": ticker,
        "market": market,
        "quantity": int(quantity_value),
        "price": price_value,
        "average_cost": average_cost_value,
        "fees_myr": fees_value,
        "pnl_myr": round(pnl_myr, 2),
        "notes": notes.strip(),
        "notional_myr": round(price_value * quantity_value * multiplier, 2),
    }


def get_journal_dataframe(vault_data: dict) -> pd.DataFrame:
    """Return the available Sheets journal without inventing fallback records."""
    for key in ("jurnal_dagangan_df", "trades_history", "jurnal"):
        journal = vault_data.get(key)
        if isinstance(journal, pd.DataFrame) and not journal.empty:
            return journal.copy()
    return pd.DataFrame()


def _safe_spreadsheet_export(df: pd.DataFrame) -> pd.DataFrame:
    safe_df = df.copy()
    for column in safe_df.select_dtypes(include=["object", "string"]).columns:
        safe_df[column] = safe_df[column].map(
            lambda value: (
                "'" + value
                if isinstance(value, str) and re.match(r"^\s*[=+\-@]", value)
                else value
            )
        )
    return safe_df


def generate_journal_csv(df: pd.DataFrame) -> bytes:
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError("Tiada rekod jurnal untuk dieksport.")
    return _safe_spreadsheet_export(df).to_csv(index=False).encode("utf-8-sig")


def generate_journal_xlsx(df: pd.DataFrame, metadata: Optional[dict] = None) -> bytes:
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError("Tiada rekod jurnal untuk dieksport.")

    output = io.BytesIO()
    safe_df = _safe_spreadsheet_export(df)
    metadata = metadata or {}
    audit_metadata = pd.DataFrame(
        [
            {"Medan": "Masa eksport", "Nilai": datetime.now().isoformat(timespec="seconds")},
            {
                "Medan": "Sumber jurnal",
                "Nilai": metadata.get("journal_source", metadata.get("source_tier", "Tidak diketahui")),
            },
            {"Medan": "Masa ambil data", "Nilai": metadata.get("timestamp", "Tidak tersedia")},
        ]
    )
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        safe_df.to_excel(writer, sheet_name="Jurnal_Dagangan", index=False)
        audit_metadata.to_excel(writer, sheet_name="Metadata_Eksport", index=False)
    return output.getvalue()


def render_portfolio_data_status(
    holdings: pd.DataFrame,
    stale_after_minutes: int = 15,
) -> None:
    """Explain the holdings source and distinguish retrieval time from quote time."""
    source = str(holdings.attrs.get("holding_source", "unavailable"))
    retrieved_at = holdings.attrs.get(
        "holding_retrieved_at", holdings.attrs.get("timestamp")
    )
    cache_timestamp = holdings.attrs.get("holding_cache_timestamp")

    remote_data_confirmed = bool(holdings.attrs.get("remote_data_confirmed"))
    if source == "webhook" and remote_data_confirmed:
        st.success("Pegangan dibaca daripada Google Sheets Webhook.")
    elif source == "direct Google Sheets CSV" and remote_data_confirmed:
        st.success("Pegangan dibaca daripada Google Sheets CSV.")
    elif source in {"webhook", "direct Google Sheets CSV"}:
        st.warning("Snapshot pegangan sesi lama; tarikan Sheets terkini tidak disahkan.")
    elif source == "local cache":
        st.warning("Pegangan datang daripada cache setempat; ia mungkin lapuk.")
        if cache_timestamp:
            st.caption(f"Cache pegangan terakhir disimpan: {cache_timestamp}")
    else:
        st.error("Sumber pegangan Google Sheets tidak tersedia atau belum disahkan.")

    if retrieved_at:
        try:
            retrieved_time = datetime.fromisoformat(str(retrieved_at))
            now = datetime.now(retrieved_time.tzinfo) if retrieved_time.tzinfo else datetime.now()
            age_minutes = max(0.0, (now - retrieved_time).total_seconds() / 60)
            st.caption(
                f"Data diambil {age_minutes:.1f} minit lalu ({retrieved_at}); "
                "ini masa pengambilan, bukan masa sebut harga."
            )
            if age_minutes > stale_after_minutes:
                st.warning(
                    f"Snapshot melepasi had umur {stale_after_minutes} minit; "
                    "segerakkan semula sebelum menggunakannya."
                )
        except ValueError:
            st.warning("Format masa pengambilan tidak sah; kesegaran snapshot tidak dapat disahkan.")
    else:
        st.caption("Masa pengambilan data tidak tersedia.")

    if holdings.attrs.get("quote_timestamp_available", False):
        st.caption(
            "Cap masa harga terbaru dalam tab: "
            f"{holdings.attrs.get('latest_quote_timestamp')}."
        )
    else:
        st.warning(
            "Tab pegangan tiada cap masa khusus untuk harga. "
            "Kesegaran sebut harga tidak dapat disahkan daripada Google Sheets."
        )

    if holdings.empty:
        st.info("Tiada baris pegangan yang mempunyai ticker, kuantiti dan nilai sah.")


def _confirm_pending_trade() -> None:
    pending = st.session_state.get("pending_portfolio_trade")
    if not pending:
        return

    with st.container(border=True):
        action = "Belian / penambahan pegangan" if pending["is_buy"] else "Jualan / pengurangan pegangan"
        st.warning(
            f"Semak dahulu: {action} {pending['quantity']:,} unit {pending['ticker']} "
            f"pada {pending['price']:,.4f} {pending['market']} "
            f"(nilai anggaran RM {pending['notional_myr']:,.2f})."
        )
        if not pending["is_buy"]:
            st.caption(f"Untung/rugi kasar selepas yuran: RM {pending['pnl_myr']:,.2f}")
        st.caption("Ini hanya merekod transaksi ke Google Sheets/barisan luar talian; bukan pesanan broker.")
        confirm_col, cancel_col = st.columns(2)
        with confirm_col:
            confirm = st.button(
                "Sahkan dan rekod",
                type="primary",
                width="stretch",
                key="confirm_portfolio_trade",
            )
        with cancel_col:
            cancel = st.button(
                "Batal",
                width="stretch",
                key="cancel_portfolio_trade",
            )

        if cancel:
            st.session_state.pop("pending_portfolio_trade", None)
            st.info("Transaksi dibatalkan; tiada data dihantar.")
        elif confirm:
            result = sync_record_trade(
                pending["is_buy"],
                pending["ticker"],
                pending["market"],
                pending["quantity"],
                pending["price"],
                pending["pnl_myr"],
                pending["notes"],
                average_cost=pending.get("average_cost", 0.0),
                fees_myr=pending.get("fees_myr", 0.0),
            )
            st.session_state.pop("pending_portfolio_trade", None)
            if result.get("status") == "SYNCED":
                st.success("Rekod disahkan oleh Google Sheets. Segerakkan semula untuk memuatkan perubahan.")
            elif result.get("status") == "QUEUED":
                st.warning("Rekod disimpan dalam barisan luar talian; Google Sheets belum mengesahkannya.")
            else:
                st.error("Status penghantaran tidak diketahui; semak barisan sebelum mencuba semula.")


def render_portfolio_manager(holdings: pd.DataFrame, fx_rate: float) -> None:
    st.subheader("Urus pegangan melalui rekod transaksi")
    st.caption(
        "Belian dan jualan direkod sebagai transaksi tambahan, bukan suntingan senyap "
        "atau penghantaran pesanan kepada broker."
    )
    buy_tab, sell_tab = st.tabs(["Catat belian", "Catat jualan"])

    with buy_tab:
        with st.form("portfolio_buy_review"):
            ticker = st.text_input("Ticker", placeholder="Contoh: KLSE:XXXX")
            market = st.selectbox("Pasaran", ["Bursa Malaysia", "Wall Street US"], key="portfolio_buy_market")
            quantity = st.number_input("Kuantiti unit", min_value=1, value=100, step=1, key="portfolio_buy_quantity")
            price_text = st.text_input(
                "Harga belian dalam mata wang pasaran",
                placeholder="Masukkan harga transaksi",
                key="portfolio_buy_price",
            )
            notes = st.text_input("Catatan audit", key="portfolio_buy_notes")
            review_buy = st.form_submit_button("Semak belian", width="stretch")
        if review_buy:
            try:
                price = float(price_text)
                st.session_state["pending_portfolio_trade"] = prepare_trade_confirmation(
                    is_buy=True,
                    ticker=ticker,
                    market=market,
                    quantity=quantity,
                    price=price,
                    fx_rate=fx_rate,
                    notes=notes,
                )
            except ValueError as exc:
                st.error(str(exc) or "Masukkan harga transaksi yang sah.")

    with sell_tab:
        if holdings.empty:
            st.info("Jualan berpandukan senarai pegangan tidak tersedia kerana tiada pegangan sah.")
        else:
            with st.form("portfolio_sell_review"):
                holding_index = st.selectbox(
                    "Pegangan",
                    options=list(range(len(holdings))),
                    format_func=lambda index: (
                        f"{holdings.iloc[index]['Ticker']} · "
                        f"{holdings.iloc[index]['Unit']:,.0f} unit tersedia"
                    ),
                    key="portfolio_sell_holding",
                )
                holding = holdings.iloc[holding_index]
                market = str(holding["Pasaran"])
                average_cost = pd.to_numeric(
                    holding["Kos_Purata"], errors="coerce"
                )
                has_average_cost = pd.notna(average_cost) and average_cost > 0
                maximum_quantity = max(1, int(holding["Unit"]))
                quantity = st.number_input(
                    "Kuantiti untuk direkod sebagai jualan",
                    min_value=1,
                    max_value=maximum_quantity,
                    value=1,
                    step=1,
                    key=f"portfolio_sell_quantity_{holding_index}",
                )
                currency_label = "RM" if market == "Bursa Malaysia" else "USD"
                price_text = st.text_input(
                    f"Harga jual yang hendak direkod ({currency_label})",
                    placeholder="Masukkan harga transaksi",
                    key=f"portfolio_sell_price_{holding_index}",
                )
                fees = st.number_input(
                    "Yuran jualan (MYR)",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key=f"portfolio_sell_fees_{holding_index}",
                )
                notes = st.text_input("Catatan audit jualan", key="portfolio_sell_notes")
                if not has_average_cost:
                    st.warning("Kos purata tiada; anggaran untung/rugi jualan tidak boleh dikira.")
                review_sell = st.form_submit_button(
                    "Semak jualan",
                    width="stretch",
                    disabled=not has_average_cost,
                )
            if review_sell:
                try:
                    price = float(price_text)
                    st.session_state["pending_portfolio_trade"] = prepare_trade_confirmation(
                        is_buy=False,
                        ticker=str(holding["Ticker"]),
                        market=market,
                        quantity=quantity,
                        price=price,
                        average_cost=float(average_cost),
                        fx_rate=fx_rate,
                        fees_myr=fees,
                        notes=notes,
                    )
                except ValueError as exc:
                    st.error(str(exc) or "Masukkan harga transaksi yang sah.")

    _confirm_pending_trade()


def render_journal_export(vault_data: dict) -> None:
    st.subheader("Jurnal dagangan dan eksport audit")
    journal = get_journal_dataframe(vault_data)
    if journal.empty:
        st.info("Tiada rekod jurnal daripada Google Sheets untuk dipaparkan atau dieksport.")
        return

    st.caption(f"{len(journal):,} rekod tersedia daripada snapshot Google Sheets.")
    st.dataframe(
        journal.tail(25),
        width="stretch",
        hide_index=True,
        alt="Pratonton rekod jurnal dagangan daripada Google Sheets",
    )
    metadata = dict(vault_data.get("_sync_metadata", {}))
    metadata["journal_source"] = metadata.get("tab_sources", {}).get(
        "jurnal_dagangan", metadata.get("source_tier", "Tidak diketahui")
    )
    export_col, audit_col = st.columns(2)
    with export_col:
        st.download_button(
            "Muat turun jurnal CSV",
            data=generate_journal_csv(journal),
            file_name=f"Haddy_Pro_Jurnal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            width="stretch",
        )
    with audit_col:
        st.download_button(
            "Muat turun jurnal Excel + metadata",
            data=generate_journal_xlsx(journal, metadata),
            file_name=f"Haddy_Pro_Jurnal_Audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )
