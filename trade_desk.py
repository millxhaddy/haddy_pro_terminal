"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL INTERAKTIF: PENGURUSAN WATCHLIST, CARTA LILIN & MEJA DAGANGAN 2-HALA
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from risk_calculator_audio import play_audio_trigger
from technical_charts import render_technical_candlestick_chart
from gsheets_sync import sync_add_watchlist, sync_record_trade

def initialize_trade_session_state():
    if "user_watchlist" not in st.session_state:
        st.session_state["user_watchlist"] = [
            {"Tarikh": "28-10-2026", "Ticker": "KLSE:TENAGA", "Harga": 12.75, "SL": 12.10, "TP": 14.38, "RR": 2.50, "Status": "Boleh Beli", "Catatan": "Pusat Data AI Johor"},
            {"Tarikh": "28-10-2026", "Ticker": "NASDAQ:NVDA", "Harga": 141.20, "SL": 134.00, "TP": 161.36, "RR": 2.80, "Status": "Boleh Beli", "Catatan": "Permintaan Cip Blackwell"}
        ]
    if "recent_trade_logs" not in st.session_state:
        st.session_state["recent_trade_logs"] = []

def render_trade_desk_ui(fx_rate: float = 4.0773):
    initialize_trade_session_state()

    tab_chart, tab_watch, tab_buy, tab_sell = st.tabs([
        "🕯️ 1. Carta Lilin & Teknikal (Live Chart)",
        "⭐ 2. Urus Watchlist & Sync",
        "🟢 3. Meja Beli (Execute Buy)",
        "🔴 4. Meja Jual (Execute Sell & Journal)"
    ])

    # ----------------------------------------------------------------------------------
    # TAB 1: CARTA LILIN INTERAKTIF (PILIHAN 2)
    # ----------------------------------------------------------------------------------
    with tab_chart:
        st.subheader("🕯️ Carta Lilin Interaktif Harian (Candlestick + SMA + RSI)")
        
        c_sel1, c_sel2 = st.columns([6, 4])
        with c_sel1:
            default_candidates = [
                "KLSE:TENAGA", "KLSE:GAMUDA", "KLSE:YTLPOWR", "KLSE:SUNCON", "KLSE:IHH",
                "NASDAQ:NVDA", "NASDAQ:MSFT", "NASDAQ:AMZN", "NASDAQ:GOOGL", "NASDAQ:AVGO",
                "NYSE:UMC", "KLSE:GFM", "LAIN-LAIN"
            ]
            picked_stock = st.selectbox("Pilih Saham untuk Dianalisis:", default_candidates)
            
        with c_sel2:
            if picked_stock == "LAIN-LAIN":
                active_ticker = st.text_input("Taip Kod Saham:", "KLSE:INARI").upper().strip()
            else:
                active_ticker = picked_stock

        # Paparkan Carta Lilin Interaktif
        render_technical_candlestick_chart(active_ticker)

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
                w_price = st.number_input("Harga Live Semasa:", min_value=0.01, value=4.55, step=0.05, format="%.2f")
                w_sl = st.number_input("Stop Loss (SL):", min_value=0.01, value=4.30, step=0.05, format="%.2f")
            with w_c3:
                w_tp = st.number_input("Sasaran TP:", min_value=0.01, value=5.20, step=0.05, format="%.2f")
                w_cat = st.text_input("Pemangkin:", value="CANSLIM Gred A+ & Wyckoff Mark-Up")
                
            w_submit = st.form_submit_button("⭐ Simpan ke Watchlist & Sync", width="stretch")
            
            if w_submit and w_ticker:
                risk = max(w_price - w_sl, 0.01)
                reward = max(w_tp - w_price, 0.01)
                rr = round(reward / risk, 2)
                status_calc = "Boleh Beli" if rr >= 2.50 else "Pantau"
                
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
                st.session_state["user_watchlist"].insert(0, new_item)
                sync_add_watchlist(w_ticker, w_price, w_sl, w_tp, rr, status_calc, w_cat)
                play_audio_trigger("bell_ding")
                st.success(f"✅ {w_ticker} disimpan ke Watchlist & disegerakkan ke Google Sheets! (R:R: {rr}x)")

        st.markdown("---")
        st.subheader("📋 Senarai Pantauan Aktif")
        st.dataframe(pd.DataFrame(st.session_state["user_watchlist"]), width="stretch", hide_index=True)

    # ----------------------------------------------------------------------------------
    # TAB 3: MEJA BELI (PILIHAN 1 WRITEBACK)
    # ----------------------------------------------------------------------------------
    with tab_buy:
        st.subheader("🟢 Borang Eksekusi Belian (Simpan ke Pegangan Aktif)")
        
        with st.form("execute_buy_form"):
            b_c1, b_c2 = st.columns(2)
            with b_c1:
                b_ticker = st.text_input("Kod Saham:", value=active_ticker).upper().strip()
                b_market = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"], key="buy_mkt")
                b_price = st.number_input("Harga Belian (Entry Price):", min_value=0.01, value=12.75, step=0.05, format="%.3f")
            with b_c2:
                b_qty = st.number_input("Kuantiti (Unit):", min_value=1, value=500, step=100)
                b_notes = st.text_input("Catatan Disiplin:", "Entri patuh zon sokongan.")

            b_submit = st.form_submit_button("🛒 Sahkan & Rekod ke Google Sheets", width="stretch")
            if b_submit and b_ticker:
                mult = fx_rate if "US" in b_market else 1.0
                total_myr = b_qty * b_price * mult
                sync_record_trade(True, b_ticker, b_market, b_qty, b_price, 0.0, b_notes)
                
                st.session_state["recent_trade_logs"].insert(0, {
                    "Masa": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Jenis": "BELI (BUY)",
                    "Ticker": b_ticker,
                    "Pasaran": b_market,
                    "Kuantiti": b_qty,
                    "Harga": b_price,
                    "Jumlah_MYR": round(total_myr, 2),
                    "Status": "Posisi Terbuka",
                    "Catatan": b_notes
                })
                play_audio_trigger("entry_success")
                st.success(f"🎉 Posisi Dibuka & Disimpan ke Google Sheets: {b_qty:,} unit {b_ticker} (RM {total_myr:,.2f})")
                st.balloons()

    # ----------------------------------------------------------------------------------
    # TAB 4: MEJA JUAL (PILIHAN 1 WRITEBACK)
    # ----------------------------------------------------------------------------------
    with tab_sell:
        st.subheader("🔴 Borang Jualan Saham (Simpan ke Jurnal Dagangan)")
        
        with st.form("execute_sell_form"):
            s_c1, s_c2 = st.columns(2)
            with s_c1:
                s_ticker = st.selectbox("Pilih Saham Pegangan:", ["KLSE:0039 (GFM Services)", "NYSE:UMC (United Microelectronics)", "LAIN-LAIN"])
                s_custom = st.text_input("Atau Taip Ticker Lain:") if s_ticker == "LAIN-LAIN" else s_ticker
                s_mkt = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"], key="sell_mkt")
                s_buy_px = st.number_input("Harga Belian Asal:", min_value=0.001, value=0.175, step=0.01, format="%.3f")
            with s_c2:
                s_sell_px = st.number_input("Harga Jual (Exit Price):", min_value=0.001, value=0.220, step=0.01, format="%.3f")
                s_qty = st.number_input("Kuantiti Dijual:", min_value=1, value=10000, step=100)
                s_reason = st.selectbox("Sebab Jualan:", ["TP AND CLOSE", "Cut Loss", "Pulang Modal"])

            s_fee = st.number_input("Yuran Broker (MYR):", value=35.00, step=5.0)
            s_notes = st.text_area("Audit Disiplin:", "Disiplin mengambil untung mengikut pelan.")

            s_submit = st.form_submit_button("💰 Sahkan Jualan & Kunci ke Jurnal Dagangan", width="stretch")
            if s_submit:
                mult = fx_rate if "US" in s_mkt else 1.0
                gross = (s_sell_px - s_buy_px) * s_qty * mult
                net_pnl = gross - s_fee
                roi = (net_pnl / (s_buy_px * s_qty * mult)) * 100 if s_buy_px > 0 else 0.0

                sync_record_trade(False, str(s_custom), s_mkt, s_qty, s_sell_px, net_pnl, s_notes)
                
                st.session_state["recent_trade_logs"].insert(0, {
                    "Masa": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Jenis": "JUAL (SELL)",
                    "Ticker": str(s_custom),
                    "Pasaran": s_mkt,
                    "Kuantiti": s_qty,
                    "Harga": s_sell_px,
                    "Jumlah_MYR": round(s_qty * s_sell_px * mult, 2),
                    "Untung_Bersih_MYR": round(net_pnl, 2),
                    "ROI_Pct": f"{roi:.2f}%",
                    "Status": s_reason,
                    "Catatan": s_notes
                })
                
                if net_pnl >= 0:
                    play_audio_trigger("entry_success")
                    st.success(f"🎉 Aliran Jurnal Dikemas Kini: Untung Bersih RM {net_pnl:,.2f} (+{roi:.2f}%)")
                    st.balloons()
                else:
                    play_audio_trigger("risk_warning")
                    st.warning(f"🛡️ Cut Loss Direkodkan: Rugi Had RM {abs(net_pnl):,.2f} ({roi:.2f}%). Modal Dilindungi!")

    st.markdown("---")
    st.subheader("📜 Log Audit Aktiviti Sesi Ini")
    if st.session_state["recent_trade_logs"]:
        st.dataframe(pd.DataFrame(st.session_state["recent_trade_logs"]), width="stretch", hide_index=True)
