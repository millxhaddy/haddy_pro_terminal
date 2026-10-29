"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL RISIKO 3M & SISTEM AUDIO TEMPATAN (OFFLINE LOCAL SIREN & CHIME ENGINE)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

AUDIO_SOUNDS = {
    "entry_success": "chime_success.wav",
    "risk_warning": "siren_alarm.wav",
    "bell_ding": "chime_success.wav"
}

def play_audio_trigger(sound_key: str):
    """
    Memainkan audio tempatan secara serta-merta menggunakan Streamlit natif.
    """
    audio_file = AUDIO_SOUNDS.get(sound_key, "chime_success.wav")
    if os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            st.audio(f.read(), format="audio/wav", autoplay=True)

def calculate_position_size(
    account_capital: float,
    risk_pct: float,
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    market_type: str = "Bursa Malaysia",
    fx_rate: float = 4.0773
) -> dict:
    max_risk_myr = account_capital * (risk_pct / 100.0)
    risk_per_unit_native = max(entry_price - stop_loss, 0.001)
    
    multiplier = fx_rate if "US" in market_type.upper() or "WALL" in market_type.upper() else 1.0
    risk_per_unit_myr = risk_per_unit_native * multiplier
    
    units_recommended = int(max_risk_myr / risk_per_unit_myr) if risk_per_unit_myr > 0 else 0
    
    if "BURSA" in market_type.upper():
        lot_size = units_recommended // 100
        units_allocated = lot_size * 100
    else:
        lot_size = units_recommended
        units_allocated = units_recommended
        
    capital_required_native = units_allocated * entry_price
    capital_required_myr = capital_required_native * multiplier
    capital_allocation_pct = (capital_required_myr / account_capital * 100.0) if account_capital > 0 else 0.0
    
    actual_risk_myr = (units_allocated * risk_per_unit_native) * multiplier
    profit_per_unit_native = max(take_profit - entry_price, 0.0)
    projected_profit_myr = (units_allocated * profit_per_unit_native) * multiplier
    rr_ratio = (profit_per_unit_native / risk_per_unit_native) if risk_per_unit_native > 0 else 0.0

    return {
        "max_risk_myr": max_risk_myr,
        "actual_risk_myr": actual_risk_myr,
        "risk_per_unit_native": risk_per_unit_native,
        "units_allocated": units_allocated,
        "lot_size": lot_size,
        "capital_required_native": capital_required_native,
        "capital_required_myr": capital_required_myr,
        "capital_allocation_pct": capital_allocation_pct,
        "projected_profit_myr": projected_profit_myr,
        "rr_ratio": rr_ratio,
        "is_safe": capital_allocation_pct <= 25.0 and rr_ratio >= 2.50
    }

def render_3m_calculator_ui(account_capital: float = 42497.80, fx_rate: float = 4.0773):
    col_input, col_output = st.columns([5, 5])

    with col_input:
        st.subheader("⚙️ Parameter Entri & Risiko DDNK")
        market_choice = st.radio("Pilih Pasaran Entri:", ["🇲🇾 Bursa Malaysia (MYR)", "🇺🇸 Wall Street US (USD)"], horizontal=True)
        market_str = "Bursa Malaysia" if "Bursa" in market_choice else "Wall Street US"
        currency_sym = "RM" if "Bursa" in market_choice else "$"
        
        cap_val = st.number_input("Modal Semasa Akaun (MYR):", value=float(account_capital), step=1000.0, format="%.2f")
        risk_slider = st.slider("Had Toleransi Risiko (% Modal):", 0.5, 3.0, 1.5, step=0.1)
        
        default_entry = 12.75 if "Bursa" in market_choice else 141.20
        default_sl = 12.10 if "Bursa" in market_choice else 134.00
        default_tp = 14.38 if "Bursa" in market_choice else 161.36
        
        c_in1, c_in2, c_in3 = st.columns(3)
        with c_in1: entry_p = st.number_input(f"Harga Belian ({currency_sym}):", value=float(default_entry), step=0.05, format="%.2f")
        with c_in2: sl_p = st.number_input(f"Stop Loss ({currency_sym}):", value=float(default_sl), step=0.05, format="%.2f")
        with c_in3: tp_p = st.number_input(f"Take Profit ({currency_sym}):", value=float(default_tp), step=0.05, format="%.2f")

    res = calculate_position_size(cap_val, risk_slider, entry_p, sl_p, tp_p, market_str, fx_rate)

    with col_output:
        st.subheader("📋 Keputusan Saiz Lot Moomoo")
        unit_display = f"{res['lot_size']} Lot ({res['units_allocated']:,} Unit)" if "Bursa" in market_str else f"{res['units_allocated']:,} Saham"

        st.metric("Had Rugi Dilindungi (Max Loss)", f"-RM {res['actual_risk_myr']:,.2f}", f"R:R: {res['rr_ratio']:.2f}x")
        
        if res["is_safe"]:
            st.success(f"✅ SAIZ LOT DISYORKAN: {unit_display} (Modal: RM {res['capital_required_myr']:,.2f})")
        else:
            st.error(f"⚠️ AMARAN RISIKO: {unit_display} (R:R < 2.50x atau melebihi had modal!)")

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("🔔 Sahkan Entri & Main Chime", width="stretch"):
                play_audio_trigger("entry_success")
                st.success(f"Pesanan Disahkan: {unit_display}!")
                st.balloons()
        with b_c2:
            if st.button("🚨 Uji Siren Amaran Cut-Loss (SL)", width="stretch"):
                play_audio_trigger("risk_warning")
                st.warning("🚨 AMARAN KECEMASAN: Paras Stop Loss Tercetus!")
