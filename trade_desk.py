"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL INTERAKTIF: PENGURUSAN WATCHLIST, CARTA LILIN & MEJA DAGANGAN 2-HALA
========================================================================================
"""

import streamlit as st
import pandas as pd
import math
from datetime import datetime
from typing import Optional
from risk_calculator_audio import play_audio_trigger
from technical_charts import render_technical_candlestick_chart
from gsheets_sync import sync_add_watchlist, sync_record_trade


def _positive_number(value) -> float:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number) or not math.isfinite(float(number)) or number <= 0:
        return 0.0
    return float(number)


def initialize_trade_session_state():
    if "user_watchlist_v2" not in st.session_state:
        st.session_state["user_watchlist_v2"] = []
    if "recent_trade_logs" not in st.session_state:
        st.session_state["recent_trade_logs"] = []

def render_trade_desk_ui(
    fx_rate: Optional[float] = None,
    holdings: Optional[pd.DataFrame] = None,
):
    initialize_trade_session_state()

    tab_chart, tab_watch, tab_buy, tab_sell = st.tabs([
        "🕯️ 1. Carta Lilin & Teknikal",
        "⭐ 2. Urus Watchlist & Sync",
        "🟢 3. Rekod Belian",
        "🔴 4. Rekod Jualan"
    ])

    # ----------------------------------------------------------------------------------
    # TAB 1: CARTA LILIN INTERAKTIF (PILIHAN 2)
    # ----------------------------------------------------------------------------------
    with tab_chart:
        st.subheader("🕯️ Carta Lilin Interaktif Harian (Candlestick + SMA + RSI)")
        
        c_sel1, c_sel2 = st.columns([6, 4])
        active_holdings = (
            holdings
            if isinstance(holdings, pd.DataFrame) and not holdings.empty
            else pd.DataFrame()
        )
        ticker_options = (
            active_holdings["Ticker"].dropna().astype(str).drop_duplicates().tolist()
            if "Ticker" in active_holdings
            else []
        )
        ticker_options.append("Ticker manual")
        with c_sel1:
            picked_stock = st.selectbox("Pilih pegangan atau ticker:", ticker_options)
            
        with c_sel2:
            if picked_stock == "Ticker manual":
                active_ticker = st.text_input("Taip Kod Saham:", "").upper().strip()
            else:
                active_ticker = picked_stock

        if active_ticker:
            render_technical_candlestick_chart(active_ticker)
        else:
            st.info("Pilih pegangan atau masukkan ticker untuk memaparkan carta.")

    # ----------------------------------------------------------------------------------
    # TAB 2: TAMBAH & URUS WATCHLIST (PILIHAN 1 WRITEBACK)
    # ----------------------------------------------------------------------------------
    with tab_watch:
        st.subheader("⭐ Tambah Saham ke Watchlist & Selaraskan ke Google Sheets")
        
        with st.form("add_watchlist_form"):
            w_c1, w_c2, w_c3 = st.columns(3)
            with w_c1:
                w_ticker = st.text_input("Kod Saham (Ticker):", value=active_ticker).upper().strip()
                w_market = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"])
            with w_c2:
                w_price = st.number_input("Harga rujukan (input manual):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
                w_sl = st.number_input("Stop Loss (input manual):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
            with w_c3:
                w_tp = st.number_input("Sasaran harga (input manual):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
                w_cat = st.text_input("Catatan (pilihan):", value="")
                
            w_submit = st.form_submit_button("⭐ Simpan ke Watchlist & Sync", width="stretch")
            
            if w_submit:
                if not w_ticker:
                    st.error("Masukkan ticker sebelum menyimpan watchlist.")
                elif not (0 < w_sl < w_price < w_tp):
                    st.error("Semak input: harga perlu positif dan susunan mesti SL < harga < sasaran.")
                else:
                    risk = w_price - w_sl
                    reward = w_tp - w_price
                    rr = round(reward / risk, 2)
                    status_calc = "Semakan manual diperlukan"
                
                    new_item = {
                        "Tarikh": datetime.now().strftime("%d-%m-%Y"),
                        "Ticker": w_ticker,
                        "Harga": w_price,
                        "SL": w_sl,
                        "TP": w_tp,
                        "RR": rr,
                        "Status": status_calc,
                        "Catatan": w_cat
                    }
                    st.session_state["user_watchlist_v2"].insert(0, new_item)
                    sync_result = sync_add_watchlist(
                        w_ticker, w_price, w_sl, w_tp, rr, status_calc, w_cat
                    )
                    play_audio_trigger("bell_ding")
                    if sync_result.get("status") == "SYNCED":
                        st.success(
                            f"✅ {w_ticker} disimpan dan disegerakkan ke Google Sheets. "
                            f"(R:R input: {rr}x; bukan saranan beli)"
                        )
                    elif sync_result.get("status") == "QUEUED":
                        st.warning(
                            f"{w_ticker} disimpan dalam barisan luar talian; "
                            "Google Sheets belum dikemas kini."
                        )
                    else:
                        st.error("Status penyegerakan tidak diketahui; semak log sebelum mencuba lagi.")

        st.markdown("---")
        st.subheader("📋 Senarai Pantauan Aktif")
        if st.session_state["user_watchlist_v2"]:
            st.dataframe(pd.DataFrame(st.session_state["user_watchlist_v2"]), width="stretch", hide_index=True)
        else:
            st.info("Watchlist sesi ini kosong. Tambah ticker dan input anda sendiri.")

    # ----------------------------------------------------------------------------------
    # TAB 3: MEJA BELI (PILIHAN 1 WRITEBACK)
    # ----------------------------------------------------------------------------------
    with tab_buy:
        st.subheader("🟢 Rekod belian dalam Google Sheets (bukan pesanan broker)")
        
        with st.form("execute_buy_form"):
            b_c1, b_c2 = st.columns(2)
            with b_c1:
                b_ticker = st.text_input("Kod Saham:", value=active_ticker).upper().strip()
                b_market = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"], key="buy_mkt")
                b_price = st.number_input("Harga belian untuk jurnal (input manual):", min_value=0.0, value=0.0, step=0.05, format="%.3f")
            with b_c2:
                b_qty = st.number_input("Kuantiti (Unit):", min_value=0, value=0, step=1)
                b_notes = st.text_input("Catatan (pilihan):", "")

            b_submit = st.form_submit_button("🛒 Sahkan & Rekod ke Google Sheets", width="stretch")
            if b_submit:
                if not b_ticker or b_price <= 0 or b_qty <= 0:
                    st.error("Masukkan ticker, harga positif dan kuantiti positif.")
                elif "US" in b_market and (
                    fx_rate is None
                    or not math.isfinite(float(fx_rate))
                    or fx_rate <= 0
                ):
                    st.error("Kadar FX USD/MYR bersumber tidak tersedia; transaksi tidak direkod.")
                else:
                    mult = fx_rate if "US" in b_market else 1.0
                    total_myr = b_qty * b_price * mult
                    sync_result = sync_record_trade(
                        True, b_ticker, b_market, b_qty, b_price, 0.0, b_notes
                    )

                    st.session_state["recent_trade_logs"].insert(0, {
                        "Masa": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        "Jenis": "BELI (BUY)",
                        "Ticker": b_ticker,
                        "Pasaran": b_market,
                        "Kuantiti": b_qty,
                        "Harga": b_price,
                        "Jumlah_MYR": round(total_myr, 2),
                        "Status": "Direkod dalam jurnal; bukan pesanan broker",
                        "Catatan": b_notes
                    })
                    play_audio_trigger("entry_success")
                    if sync_result.get("status") == "SYNCED":
                        st.success(
                            f"Transaksi {b_ticker} direkod ke Google Sheets: "
                            f"{b_qty:,} unit (RM {total_myr:,.2f}). Tiada pesanan dihantar kepada broker."
                        )
                    elif sync_result.get("status") == "QUEUED":
                        st.warning(
                            f"Transaksi {b_ticker} berada dalam barisan luar talian; "
                            "Google Sheets belum dikemas kini. Tiada pesanan broker dihantar."
                        )
                    else:
                        st.error("Status penyegerakan tidak diketahui; semak log sebelum mencuba lagi.")

    # ----------------------------------------------------------------------------------
    # TAB 4: MEJA JUAL (PILIHAN 1 WRITEBACK)
    # ----------------------------------------------------------------------------------
    with tab_sell:
        st.subheader("🔴 Rekod jualan dalam jurnal (bukan pesanan broker)")
        sell_options = (
            active_holdings["Ticker"].astype(str).tolist() + ["LAIN-LAIN"]
            if not active_holdings.empty
            else ["LAIN-LAIN"]
        )

        with st.form("execute_sell_form"):
            s_c1, s_c2 = st.columns(2)
            with s_c1:
                s_ticker = st.selectbox("Pilih Saham Pegangan:", sell_options)
                s_custom = st.text_input("Atau Taip Ticker Lain:") if s_ticker == "LAIN-LAIN" else s_ticker
                selected_holding = (
                    active_holdings.loc[active_holdings["Ticker"].astype(str) == s_ticker].iloc[0]
                    if s_ticker != "LAIN-LAIN"
                    else None
                )
                market_options = ["Bursa Malaysia", "Wall Street US"]
                default_market = (
                    str(selected_holding["Pasaran"])
                    if selected_holding is not None
                    else market_options[0]
                )
                s_mkt = st.selectbox(
                    "Pasaran:",
                    market_options,
                    index=market_options.index(default_market)
                    if default_market in market_options
                    else 0,
                    key="sell_mkt",
                )
                default_cost = (
                    _positive_number(selected_holding.get("Kos_Purata"))
                    if selected_holding is not None
                    else 0.0
                )
                s_buy_px = st.number_input(
                    "Kos purata asal (sumber pegangan atau input manual):",
                    min_value=0.0,
                    value=default_cost,
                    step=0.01,
                    format="%.4f",
                )
            with s_c2:
                default_sell_price = (
                    _positive_number(selected_holding.get("Harga_Semasa"))
                    if selected_holding is not None
                    else default_cost
                )
                s_sell_px = st.number_input(
                    "Harga jual untuk jurnal (input/semak sendiri):",
                    min_value=0.0,
                    value=default_sell_price,
                    step=0.01,
                    format="%.4f",
                )
                max_quantity = (
                    max(0, int(_positive_number(selected_holding.get("Unit"))))
                    if selected_holding is not None
                    else None
                )
                s_qty = st.number_input(
                    "Kuantiti dijual:",
                    min_value=0,
                    max_value=max_quantity,
                    value=0,
                    step=1,
                )
                s_reason = st.selectbox("Sebab jualan (pilihan):", ["TP", "Cut loss", "Pulang modal", "Lain-lain"])

            s_fee = st.number_input("Yuran transaksi (MYR, input manual):", min_value=0.0, value=0.0, step=1.0)
            s_notes = st.text_area("Catatan (pilihan):", "")

            s_submit = st.form_submit_button("💰 Sahkan Jualan & Kunci ke Jurnal Dagangan", width="stretch")
            if s_submit:
                ticker = str(s_custom).strip().upper()
                if not ticker or s_buy_px <= 0 or s_sell_px <= 0 or s_qty <= 0:
                    st.error("Masukkan ticker, kos, harga jual dan kuantiti yang semuanya positif.")
                elif "US" in s_mkt and (
                    fx_rate is None
                    or not math.isfinite(float(fx_rate))
                    or fx_rate <= 0
                ):
                    st.error("Kadar FX USD/MYR bersumber tidak tersedia; transaksi tidak direkod.")
                else:
                    mult = fx_rate if "US" in s_mkt else 1.0
                    gross = (s_sell_px - s_buy_px) * s_qty * mult
                    net_pnl = gross - s_fee
                    roi = (net_pnl / (s_buy_px * s_qty * mult)) * 100

                    sync_result = sync_record_trade(
                        False,
                        ticker,
                        s_mkt,
                        s_qty,
                        s_sell_px,
                        net_pnl,
                        s_notes,
                        average_cost=s_buy_px,
                        fees_myr=s_fee,
                    )
                
                    st.session_state["recent_trade_logs"].insert(0, {
                        "Masa": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        "Jenis": "JUAL (SELL)",
                        "Ticker": ticker,
                        "Pasaran": s_mkt,
                        "Kuantiti": s_qty,
                        "Harga": s_sell_px,
                        "Jumlah_MYR": round(s_qty * s_sell_px * mult, 2),
                        "Untung_Bersih_MYR": round(net_pnl, 2),
                        "ROI_Pct": f"{roi:.2f}%",
                        "Status": s_reason,
                        "Catatan": s_notes
                    })
                
                    if sync_result.get("status") == "SYNCED":
                        st.success(
                            f"Jualan {ticker} direkod dalam jurnal Google Sheets. "
                            f"PnL anggaran daripada input: RM {net_pnl:,.2f} ({roi:.2f}%). "
                            "Tiada pesanan dihantar kepada broker."
                        )
                    elif sync_result.get("status") == "QUEUED":
                        st.warning(
                            f"Jualan {ticker} berada dalam barisan luar talian; Google Sheets belum "
                            f"dikemas kini. PnL input: RM {net_pnl:,.2f}."
                        )
                    else:
                        st.error("Status penyegerakan tidak diketahui; semak log sebelum mencuba lagi.")

    st.markdown("---")
    st.subheader("📜 Log Audit Aktiviti Sesi Ini")
    if st.session_state["recent_trade_logs"]:
        st.dataframe(pd.DataFrame(st.session_state["recent_trade_logs"]), width="stretch", hide_index=True)
