"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 5: TETINGKAP PESANAN MODAL (ST.DIALOG) & ENJIN KOS TRANSAKSI BURSA / US
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np

def calculate_bursa_transaction_cost(units: int, price: float, broker_rate: float = 0.0003, min_broker: float = 3.0) -> dict:
    """
    Mengira kos transaksi sebenar Bursa Malaysia mengikut peraturan terkini:
    - Brokerage: 0.03% (Min RM 3.00)
    - Clearing Fee: 0.03% (Had Max RM 1,000)
    - Stamp Duty: RM 1.50 per RM 1,000 (Had Max RM 1,000)
    - SST: 8% ke atas Brokerage Fee
    """
    contract_val = units * price
    if contract_val <= 0:
        return {}

    # 1. Brokerage Fee
    broker_fee = max(contract_val * broker_rate, min_broker)
    
    # 2. SST 8% atas brokerage
    sst = broker_fee * 0.08
    
    # 3. Clearing Fee (0.03% capped at RM 1,000)
    clearing_fee = min(contract_val * 0.0003, 1000.0)
    
    # 4. Stamp Duty (RM 1.50 per RM 1,000 or part thereof, capped at RM 1,000)
    thousands = int(np.ceil(contract_val / 1000.0))
    stamp_duty = min(thousands * 1.50, 1000.0)
    
    total_cost_one_way = broker_fee + sst + clearing_fee + stamp_duty
    total_cost_round_trip = total_cost_one_way * 2.0  # Anggaran masuk & keluar
    
    # Harga Breakeven
    breakeven_price = price + (total_cost_round_trip / units) if units > 0 else price
    breakeven_ticks = round((breakeven_price - price) / 0.005, 1)

    return {
        "contract_val": contract_val,
        "broker_fee": broker_fee,
        "sst": sst,
        "clearing_fee": clearing_fee,
        "stamp_duty": stamp_duty,
        "total_one_way": total_cost_one_way,
        "total_round_trip": total_cost_round_trip,
        "breakeven_price": breakeven_price,
        "breakeven_ticks": breakeven_ticks
    }

def calculate_us_transaction_cost(shares: int, price_usd: float, dividend_yield_pct: float = 2.5, fx_rate: float = 4.0773) -> dict:
    """
    Mengira kos transaksi Wall Street US (Moomoo) & Cukai Dividen 30% WHT.
    """
    gross_usd = shares * price_usd
    gross_myr = gross_usd * fx_rate
    
    # Moomoo US Standard Fees
    commission = 0.99
    platform_fee = 0.99
    sec_fee = max(gross_usd * 0.0000278, 0.01)
    finra_fee = max(shares * 0.000166, 0.01)
    total_fee_usd = commission + platform_fee + sec_fee + finra_fee
    total_fee_myr = total_fee_usd * fx_rate
    
    # Kiraan Cukai Pegangan Dividen AS 30% (WHT)
    est_annual_div_gross_usd = gross_usd * (dividend_yield_pct / 100.0)
    wht_30_pct_usd = est_annual_div_gross_usd * 0.30
    est_annual_div_net_usd = est_annual_div_gross_usd - wht_30_pct_usd
    est_annual_div_net_myr = est_annual_div_net_usd * fx_rate

    return {
        "gross_usd": gross_usd,
        "gross_myr": gross_myr,
        "total_fee_usd": total_fee_usd,
        "total_fee_myr": total_fee_myr,
        "div_gross_usd": est_annual_div_gross_usd,
        "wht_tax_usd": wht_30_pct_usd,
        "div_net_usd": est_annual_div_net_usd,
        "div_net_myr": est_annual_div_net_myr
    }

# FUNGSI MODAL DIALOG POP-UP INTERAKTIF
@st.dialog("🛒 Tetingkap Pesanan Pantas & Kiraan Kos Terperinci")
def open_quick_order_modal(default_ticker: str = "KLSE:TENAGA", default_price: float = 12.75, fx_rate: float = 4.0773):
    st.caption("Kira kos bersih duti setem, yuran penjelasan & cukai dividen secara automatik sebelum membuat tempahan.")

    mkt = st.radio("Pilih Pasaran:", ["🇲🇾 Bursa Malaysia (MYR)", "🇺🇸 Wall Street US (USD)"], horizontal=True)
    is_bursa = "Bursa" in mkt

    c1, c2 = st.columns(2)
    with c1:
        sym = st.text_input("Kod Saham (Ticker):", value=default_ticker).upper().strip()
        px = st.number_input(f"Harga Had ({'RM' if is_bursa else '$'}):", value=float(default_price), step=0.01, format="%.2f")
    with c2:
        default_qty = 500 if is_bursa else 25
        qty = st.number_input(f"Kuantiti ({'Unit (Lot x100)' if is_bursa else 'Unit Saham'}):", value=int(default_qty), step=100 if is_bursa else 5)
        sl_val = st.number_input("Paras Stop Loss:", value=float(px * 0.95), step=0.01, format="%.2f")

    st.markdown("---")

    if is_bursa:
        res = calculate_bursa_transaction_cost(qty, px)
        if res:
            st.markdown("#### 📋 Pecahan Yuran Transaksi Rasmi Bursa Malaysia:")
            b_c1, b_c2, b_c3 = st.columns(3)
            b_c1.metric("Nilai Kontrak", f"RM {res['contract_val']:,.2f}")
            b_c2.metric("Jumlah Kos Masuk-Keluar", f"RM {res['total_round_trip']:,.2f}", "Broker + Duti Setem + SST")
            b_c3.metric("Harga Pulang Modal (Breakeven)", f"RM {res['breakeven_price']:.3f}", f"+{res['breakeven_ticks']} Ticks")

            with st.expander("🔍 Rincian Yuran (Regulatory Breakdown)", expanded=False):
                st.write(f"- Yuran Brokerage (0.03%): **RM {res['broker_fee']:,.2f}**")
                st.write(f"- Cukai SST (8%): **RM {res['sst']:,.2f}**")
                st.write(f"- Yuran Penjelasan (0.03%): **RM {res['clearing_fee']:,.2f}**")
                st.write(f"- Duti Setem (RM 1.50/k, max RM1k): **RM {res['stamp_duty']:,.2f}**")
    else:
        res_u = calculate_us_transaction_cost(qty, px, fx_rate=fx_rate)
        if res_u:
            st.markdown("#### 📋 Pecahan Yuran Transaksi US & Cukai Dividen 30% WHT:")
            u_c1, u_c2, u_c3 = st.columns(3)
            u_c1.metric("Nilai Saham (USD)", f"${res_u['gross_usd']:,.2f}", f"~RM {res_u['gross_myr']:,.2f}")
            u_c2.metric("Yuran Transaksi Moomoo", f"${res_u['total_fee_usd']:.2f}", f"~RM {res_u['total_fee_myr']:.2f}")
            u_c3.metric("Dividen Bersih (Lepas WHT 30%)", f"${res_u['div_net_usd']:,.2f}/thn", f"~RM {res_u['div_net_myr']:,.2f}")

            with st.expander("🔍 Rincian Cukai Dividen AS (30% Withholding Tax)", expanded=False):
                st.write(f"- Anggaran Dividen Kasar (2.5% yield): **${res_u['div_gross_usd']:,.2f}**")
                st.write(f"- Potongan Cukai WHT 30% Kerajaan AS: **-${res_u['wht_tax_usd']:,.2f}**")
                st.write(f"- Dividen Bersih Masuk Akaun: **${res_u['div_net_usd']:,.2f} (RM {res_u['div_net_myr']:,.2f})**")

    st.markdown("---")
    if st.button("🚀 Sahkan & Salin Pesanan ke Broker", width="stretch"):
        st.success(f"Pesanan {qty:,} unit {sym} disahkan! Sedia disalin ke aplikasi Moomoo.")