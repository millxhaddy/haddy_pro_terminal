"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL ENJIN LIVE MOOMOO OPEND (SMART ACCOUNT ID & MULTI-CURRENCY SELECTOR)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np

def fetch_moomoo_live_account(market="US", host="127.0.0.1", port=11111):
    try:
        import moomoo
        from moomoo import OpenSecTradeContext, TrdMarket, SecurityFirm

        mkt = TrdMarket.US if str(market).upper() == "US" else TrdMarket.MY

        # Keutamaan firma: Moomoo Malaysia -> Moomoo US -> Moomoo SG
        firm_candidates = []
        if hasattr(SecurityFirm, "FUTUSECMY"):
            firm_candidates.append(("Moomoo MY", SecurityFirm.FUTUSECMY))
        firm_candidates.append(("Moomoo US", SecurityFirm.FUTUINC))
        if hasattr(SecurityFirm, "FUTUSG"):
            firm_candidates.append(("Moomoo SG", SecurityFirm.FUTUSG))

        trd_ctx = None
        target_acc_id = None
        connected_firm = ""
        last_error = ""

        for name, firm in firm_candidates:
            try:
                ctx = OpenSecTradeContext(
                    filter_trdmarket=mkt,
                    host=host,
                    port=port,
                    security_firm=firm
                )
                ret, acc_list = ctx.get_acc_list()
                if ret == 0 and not acc_list.empty:
                    trd_ctx = ctx
                    connected_firm = name
                    # Pilih akaun yang sah
                    # Utamakan akaun Universal / Margin jika ada
                    target_acc_id = int(acc_list.iloc[0]["acc_id"])
                    for _, acc_row in acc_list.iterrows():
                        # Jika ada akaun yang padan dengan 8702
                        if "8702" in str(acc_row.get("acc_id", "")) or "8702" in str(acc_row.get("trd_env", "")):
                            target_acc_id = int(acc_row["acc_id"])
                            break
                    break
                else:
                    ctx.close()
            except Exception as e:
                last_error = str(e)

        if trd_ctx is None:
            raise ConnectionError(f"Gagal berhubung ke OpenD: {last_error}")

        # 1. Sedut Baki Menggunakan acc_id Spesifik
        funds_summary = {
            "total_assets": 0.0,
            "cash": 0.0,
            "market_val": 0.0,
            "unrealized_pl": 0.0,
            "currency": "USD" if str(market).upper() == "US" else "MYR",
            "firm": connected_firm,
            "acc_id": str(target_acc_id),
            "connected": True
        }

        try:
            if target_acc_id:
                ret_acc, data_funds = trd_ctx.get_acc_details(acc_id=target_acc_id)
            else:
                ret_acc, data_funds = trd_ctx.get_acc_details()

            if ret_acc == 0 and not data_funds.empty:
                funds_summary["total_assets"] = float(data_funds.get("total_assets", [0.0])[0])
                funds_summary["cash"] = float(data_funds.get("cash", [0.0])[0])
                funds_summary["market_val"] = float(data_funds.get("market_val", [0.0])[0])
                funds_summary["unrealized_pl"] = float(data_funds.get("unrealized_pl", [0.0])[0])
                if "currency" in data_funds.columns:
                    funds_summary["currency"] = str(data_funds.get("currency", ["USD"])[0])
        except Exception as e:
            last_error += f" | funds_err: {e}"

        # 2. Sedut Pegangan Saham Menggunakan acc_id Spesifik
        positions_list = []
        try:
            if target_acc_id:
                ret_pos, data_pos = trd_ctx.get_acc_positions(acc_id=target_acc_id)
            else:
                ret_pos, data_pos = trd_ctx.get_acc_positions()

            if ret_pos == 0 and not data_pos.empty:
                for _, r in data_pos.iterrows():
                    positions_list.append({
                        "Ticker": str(r.get("code", "")),
                        "Nama": str(r.get("stock_name", "")),
                        "Kuantiti": int(r.get("qty", 0)),
                        "Kos Purata": float(r.get("cost_price", 0.0)),
                        "Harga Semasa": float(r.get("nominal_price", 0.0)),
                        "Nilai Pasaran": float(r.get("market_val", 0.0)),
                        "Untung/Rugi (Live)": float(r.get("pl_val", 0.0)),
                        "ROI (%)": float(r.get("pl_ratio", 0.0))
                    })
        except Exception as e:
            last_error += f" | pos_err: {e}"

        trd_ctx.close()

        # Jika baki bernilai 0 tapi Google Sheets ada rekod, sertakan maklumat akaun
        return {
            "status": "success",
            "connected": True,
            "firm_name": connected_firm,
            "target_acc": str(target_acc_id),
            "funds": funds_summary,
            "positions": pd.DataFrame(positions_list),
            "error_msg": last_error
        }

    except Exception as e:
        return {
            "status": "offline",
            "connected": False,
            "error_msg": str(e),
            "funds": {
                "total_assets": 55945.32,
                "cash": 18500.00,
                "market_val": 46075.32,
                "unrealized_pl": -1038.92,
                "currency": "MYR",
                "firm": "Simulasi"
            },
            "positions": pd.DataFrame([
                {"Ticker": "KLSE:0039", "Nama": "GFM Services Berhad", "Kuantiti": 56400, "Kos Purata": 0.175, "Harga Semasa": 0.175, "Nilai Pasaran": 9870.00, "Untung/Rugi (Live)": 0.00, "ROI (%)": 0.0},
                {"Ticker": "NYSE:UMC", "Nama": "United Microelectronics", "Kuantiti": 581, "Kos Purata": 19.26, "Harga Semasa": 18.65, "Nilai Pasaran": 44438.58, "Untung/Rugi (Live)": -1038.92, "ROI (%)": -2.3}
            ])
        }

def render_moomoo_live_dashboard():
    st.subheader("⚡ Hab Akaun Moomoo Universal (8702) Secara Live")
    st.caption("Penyegerakan langsung masa nyata baki tunai, nilai pasaran saham & pegangan aktif melalui Moomoo OpenD Gateway.")

    c_mkt, c_ref = st.columns([7, 3])
    with c_mkt:
        mkt_choice = st.radio("Pilih Pasaran Akaun Moomoo:", ["🇺🇸 US Wall Street (Universal USD)", "🇲🇾 Bursa Malaysia (Universal MYR)"], horizontal=True)
    with c_ref:
        st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
        force_check = st.button("🔄 SEGERAK LIVE MOOMOO (PING)", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    mkt_code = "US" if "US" in mkt_choice else "MY"

    with st.spinner("Menghubungi Moomoo OpenD Gateway di 127.0.0.1:11111..."):
        acc_data = fetch_moomoo_live_account(market=mkt_code)

    if acc_data["connected"]:
        st.success(f"🟢 STATUS: TERSAMBUNG SECARA LIVE KE MOOMOO OPEND ({acc_data.get('firm_name', 'Moomoo Gateway')} • Acc ID: {acc_data.get('target_acc', 'Auto')})")
    else:
        st.warning("🟡 STATUS: MOD SIMULASI / OPEND STANDBY")

    funds = acc_data["funds"]
    curr = funds.get("currency", "USD" if mkt_code == "US" else "MYR")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Assets (NAV)", f"{curr} {funds.get('total_assets', 0):,.2f}")
    with k2:
        st.metric("Tunai Tersedia (Cash)", f"{curr} {funds.get('cash', 0):,.2f}")
    with k3:
        st.metric("Nilai Pasaran Saham", f"{curr} {funds.get('market_val', 0):,.2f}")
    with k4:
        pnl_val = funds.get("unrealized_pl", 0)
        st.metric("Untung/Rugi Semasa", f"{curr} {pnl_val:,.2f}", delta=f"{pnl_val:,.2f}")

    st.markdown("---")
    st.markdown("#### 📦 Senarai Pegangan Saham Aktif Sebenar (Live Holdings):")
    df_pos = acc_data["positions"]
    if not df_pos.empty:
        st.dataframe(
            df_pos.style.format({
                "Kos Purata": "{:.3f}",
                "Harga Semasa": "{:.3f}",
                "Nilai Pasaran": "{:,.2f}",
                "Untung/Rugi (Live)": "{:,.2f}",
                "ROI (%)": "{:+.2f}%"
            }).map(
                lambda v: "color: #00E676; font-weight: bold;" if float(str(v).replace('%','').replace('+','')) >= 0 else "color: #FF5252; font-weight: bold;",
                subset=["ROI (%)"]
            ),
            width="stretch",
            hide_index=True
        )
    else:
        st.info("Tiada saham aktif dikesan dalam pasaran ini.")