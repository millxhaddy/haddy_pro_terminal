"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 12 & 13: KALKULATOR RISIKO 3M & SISTEM ISYARAT AUDIO INTERAKTIF
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np

# Pustaka Bunyi Isyarat Pasaran Berkelajuan Tinggi (CDN Bebas Hak Cipta)
AUDIO_SOUNDS = {
    "entry_success": "https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3", # Chime kejayaan
    "risk_warning": "https://cdn.freesound.org/previews/142/142608_24940-lq.mp3",    # Siren amaran risiko
    "bell_ding": "https://cdn.freesound.org/previews/274/274178_5121236-lq.mp3"       # Lonceng bursa
}

def play_audio_trigger(sound_key: str):
    """
    Menyuntik audio HTML5 ke dalam DOM Streamlit menggunakan st.html natif.
    """
    audio_url = AUDIO_SOUNDS.get(sound_key, AUDIO_SOUNDS["entry_success"])
    sound_html = f'<audio autoplay style="display:none;"><source src="{audio_url}" type="audio/mp3"></audio>'
    if hasattr(st, "html"):
        st.html(sound_html)
    elif hasattr(st, "iframe"):
        st.iframe(sound_html, height=0)

def calculate_position_size(
    account_capital: float,
    risk_pct: float,
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    market_type: str = "Bursa Malaysia",
    fx_rate: float = 4.0773
) -> dict:
    """
    FASA 12: Enjin Kiraan Saiz Posisi DDNK 3M Anti-Blowup.
    """
    # 1. Had Risiko Maksimum dalam Mata Wang Tempatan (MYR)
    max_risk_myr = account_capital * (risk_pct / 100.0)
    
    # 2. Risiko per unit (Jarak ke Stop Loss)
    risk_per_unit_native = max(entry_price - stop_loss, 0.001)
    
    # Jika pasaran US, tukar risiko per unit ke MYR
    multiplier = fx_rate if "US" in market_type.upper() or "WALL" in market_type.upper() else 1.0
    risk_per_unit_myr = risk_per_unit_native * multiplier
    
    # 3. Kuantiti Maksimum Unit Dilindungi
    units_recommended = int(max_risk_myr / risk_per_unit_myr) if risk_per_unit_myr > 0 else 0
    
    # 4. Pelarasan Lot Bursa (1 Lot = 100 Unit) vs Unit Saham US
    if "BURSA" in market_type.upper():
        lot_size = units_recommended // 100
        units_allocated = lot_size * 100
    else:
        lot_size = units_recommended
        units_allocated = units_recommended
        
    # 5. Jumlah Modal Diperlukan untuk Eksekusi Posisi
    capital_required_native = units_allocated * entry_price
    capital_required_myr = capital_required_native * multiplier
    capital_allocation_pct = (capital_required_myr / account_capital * 100.0) if account_capital > 0 else 0.0
    
    # 6. Kerugian Sebenar jika Kena Stop Loss
    actual_risk_myr = (units_allocated * risk_per_unit_native) * multiplier
    
    # 7. Unjuran Keuntungan Bersih jika Capai Take Profit
    profit_per_unit_native = max(take_profit - entry_price, 0.0)
    projected_profit_myr = (units_allocated * profit_per_unit_native) * multiplier
    
    # 8. Nisbah Risiko-Ganjaran (R:R Ratio)
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
    """
    Memaparkan susun atur interaktif kalkulator saiz posisi berserta maklum balas audio.
    """
    st.markdown("""
    <style>
        .calc-panel {
            background: linear-gradient(135deg, #1C2333 0%, #141A29 100%);
            border: 1px solid #2B384E;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .result-box-green {
            background-color: rgba(0, 230, 118, 0.1);
            border: 1px solid rgba(0, 230, 118, 0.3);
            border-radius: 10px;
            padding: 16px;
            margin-top: 15px;
        }
        .result-box-red {
            background-color: rgba(255, 82, 82, 0.1);
            border: 1px solid rgba(255, 82, 82, 0.3);
            border-radius: 10px;
            padding: 16px;
            margin-top: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    col_input, col_output = st.columns([5, 5])

    with col_input:
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.subheader("⚙️ Parameter Entri & Risiko DDNK")
        
        market_choice = st.radio("Pilih Pasaran Entri:", ["🇲🇾 Bursa Malaysia (MYR)", "🇺🇸 Wall Street US (USD)"], horizontal=True)
        market_str = "Bursa Malaysia" if "Bursa" in market_choice else "Wall Street US"
        currency_sym = "RM" if "Bursa" in market_choice else "$"
        
        cap_val = st.number_input("Modal Semasa Akaun (MYR):", value=float(account_capital), step=1000.0, format="%.2f")
        risk_slider = st.slider("Had Toleransi Risiko (% Modal):", min_value=0.5, max_value=3.0, value=1.5, step=0.1, help="Piawaian Institusi: Maksimum 1.0% - 2.0% modal per trade.")
        
        # Contoh nilai lalai pintar mengikut pasaran
        default_entry = 12.75 if "Bursa" in market_choice else 141.20
        default_sl = 12.10 if "Bursa" in market_choice else 134.00
        default_tp = 14.38 if "Bursa" in market_choice else 161.36
        
        c_in1, c_in2, c_in3 = st.columns(3)
        with c_in1:
            entry_p = st.number_input(f"Harga Belian ({currency_sym}):", value=float(default_entry), step=0.05, format="%.2f")
        with c_in2:
            sl_p = st.number_input(f"Stop Loss ({currency_sym}):", value=float(default_sl), step=0.05, format="%.2f")
        with c_in3:
            tp_p = st.number_input(f"Take Profit ({currency_sym}):", value=float(default_tp), step=0.05, format="%.2f")

        st.markdown('</div>', unsafe_allow_html=True)

    # Lakukan Pengiraan
    res = calculate_position_size(cap_val, risk_slider, entry_p, sl_p, tp_p, market_str, fx_rate)

    with col_output:
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.subheader("📋 Keputusan Saiz Lot Moomoo")
        
        if "Bursa" in market_str:
            unit_display = f"{res['lot_size']} Lot ({res['units_allocated']:,} Unit)"
        else:
            unit_display = f"{res['units_allocated']:,} Saham"

        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
            <div>
                <small style="color:#8E9AAF;">Had Rugi Dilindungi (Max Loss)</small><br>
                <strong style="color:#FF5252; font-size:1.3rem;">-RM {res['actual_risk_myr']:,.2f}</strong>
                <small style="color:#8E9AAF;">({(res['actual_risk_myr']/cap_val*100):.1f}% Modal)</small>
            </div>
            <div>
                <small style="color:#8E9AAF;">Potensi Untung TP</small><br>
                <strong style="color:#00E676; font-size:1.3rem;">+RM {res['projected_profit_myr']:,.2f}</strong>
            </div>
            <div>
                <small style="color:#8E9AAF;">Nisbah R:R</small><br>
                <strong style="color:#FFBB28; font-size:1.3rem;">{res['rr_ratio']:.2f}x</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if res["is_safe"]:
            st.markdown(f"""
            <div class="result-box-green">
                <h3 style="color:#00E676; margin:0;">✅ SAIZ LOT DISYORKAN: {unit_display}</h3>
                <p style="margin:5px 0 0 0; color:#E0E0E0; font-size:0.9rem;">
                    Modal Diperlukan: <b>RM {res['capital_required_myr']:,.2f}</b> ({res['capital_allocation_pct']:.1f}% daripada jumlah portfolio).
                    <br>Pematuhan SOP: <b>LULUS PENUH (R:R &ge; 2.50x & Pendedahan Modal &le; 25%)</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box-red">
                <h3 style="color:#FF5252; margin:0;">⚠️ PERINGATAN RISIKO TINGGI: {unit_display}</h3>
                <p style="margin:5px 0 0 0; color:#E0E0E0; font-size:0.9rem;">
                    Modal Diperlukan: <b>RM {res['capital_required_myr']:,.2f}</b> ({res['capital_allocation_pct']:.1f}% Modal).
                    <br>Ralat: Nisbah R:R kurang 2.50x atau saiz melebihi siling 25% modal per trade!
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Butang Tindakan Berbunyi (Fasa 13 Audio Trigger)
        st.markdown("<br>", unsafe_allow_html=True)
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("🔔 Sahkan Entri Moomoo & Mainkan Chime", width="stretch"):
                play_audio_trigger("entry_success")
                st.success(f"Pesanan Disahkan: {unit_display} pada harga {currency_sym}{entry_p:.2f}!")
                st.balloons()
        with b_c2:
            if st.button("🚨 Uji Siren Amaran Cut-Loss (SL)", width="stretch"):
                play_audio_trigger("risk_warning")
                st.warning("Amaran Had Risiko Diaktifkan: Saham mencecah paras Stop Loss!")

        st.markdown('</div>', unsafe_allow_html=True)
