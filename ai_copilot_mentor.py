"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 2: AI CO-PILOT "MENTOR DAGANGAN DDNK" (INTERACTIVE AI TRADING ADVISOR)
Penasihat Disiplin Keras: Saringan Ketat 3 Tiang DDNK (Mind 60%, Money 30%, Method 10%)
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from risk_calculator_audio import play_audio_trigger

def audit_stock_entry_decision(
    ticker: str,
    market: str,
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    capital_available: float,
    wyckoff_phase: str,
    catalyst_reason: str,
    is_fomo_news: bool
) -> dict:
    """
    Enjin Logik AI Mentor DDNK: Menyemak 3 Tiang Disiplin & Menjana Keputusan Muktamad.
    """
    risk_unit = max(entry_price - stop_loss, 0.001)
    reward_unit = max(take_profit - entry_price, 0.001)
    rr_ratio = round(reward_unit / risk_unit, 2)
    
    # 1. Audit Mind (60%)
    mind_passed = not is_fomo_news and wyckoff_phase in ["Fasa C (Spring Shakeout)", "Fasa D (Mark-Up Breakout)"]
    mind_feedback = []
    if is_fomo_news:
        mind_feedback.append("❌ TERJEBAK FOMO: Anda membeli kerana heboh berita/hype. Ingat tragedi DJT (-RM 5,866)!")
    else:
        mind_feedback.append("✅ DISIPLIN EMOSI: Sifar unsur FOMO. Entri dirancang secara tenang.")
        
    if wyckoff_phase == "Fasa B (Ujian Lantai)":
        mind_feedback.append("⚠️ WYCKOFF AWAL: Saham masih menguji lantai. Belum ada pengesahan jerung.")
    elif wyckoff_phase == "Fasa C (Spring Shakeout)":
        mind_feedback.append("✅ WYCKOFF IDEAL: Fasa Spring (Shakeout of weak hands) memberi risiko terendah.")
    elif wyckoff_phase == "Fasa D (Mark-Up Breakout)":
        mind_feedback.append("✅ WYCKOFF MOMENTUM: Jerung memborong dan menolak harga melepasi rintangan.")
    else:
        mind_feedback.append("❌ WYCKOFF BAHAYA: Saham sudah di Fasa E (Terlajak Pucuk). Risiko terperangkap seperti kaunter HL!")

    # 2. Audit Money (30%)
    money_passed = rr_ratio >= 2.50
    money_feedback = []
    if rr_ratio >= 2.50:
        money_feedback.append(f"✅ NISBAH R:R MEMUASKAN: {rr_ratio}x (Melepasi penanda aras minimum 2.50x).")
    else:
        money_feedback.append(f"❌ NISBAH R:R TIDAK BERBALOI: {rr_ratio}x (Kurang daripada 2.50x). Potensi untung tidak sepadan dengan risiko!")

    # 3. Audit Method (10%)
    method_passed = len(catalyst_reason.strip()) >= 5
    method_feedback = []
    if method_passed:
        method_feedback.append(f"✅ PEMANGKIN JELAS: {catalyst_reason}")
    else:
        method_feedback.append("❌ TIADA PEMANGKIN SAH: Membeli tanpa asas pemangkin institusi adalah spekulasi buta.")

    # Keputusan Akhir AI Mentor
    all_passed = mind_passed and money_passed and method_passed
    
    return {
        "ticker": ticker.upper(),
        "market": market,
        "rr_ratio": rr_ratio,
        "mind_passed": mind_passed,
        "money_passed": money_passed,
        "method_passed": method_passed,
        "all_passed": all_passed,
        "mind_feedback": mind_feedback,
        "money_feedback": money_feedback,
        "method_feedback": method_feedback
    }

def render_ai_copilot_ui(fx_rate: float = 4.0773, net_capital: float = 42497.80):
    st.markdown("""
    <style>
        .ai-mentor-box-green {
            background: linear-gradient(135deg, #0A2920 0%, #061813 100%);
            border: 2px solid #00E676;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 18px rgba(0, 230, 118, 0.25);
            margin-top: 15px;
        }
        .ai-mentor-box-red {
            background: linear-gradient(135deg, #2D1118 0%, #170A0E 100%);
            border: 2px solid #FF5252;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 18px rgba(255, 82, 82, 0.25);
            margin-top: 15px;
        }
        .ai-bubble {
            background-color: #1A2232;
            border-left: 4px solid #29B6F6;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 10px;
            color: #E2E8F0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🤖 AI Co-Pilot: Mentor Dagangan DDNK 3M")
    st.caption("Pemeriksaan Disiplin Keras Sebelum Menekan Butang Beli: Tiada Emosi, Tiada Kompromi, Hanya Matematik & SOP.")

    col_in, col_verdict = st.columns([5, 5])

    with col_in:
        st.subheader("📝 Borang Permohonan Entri Saham")
        with st.form("ai_copilot_form"):
            s_ticker = st.text_input("Kod Saham (Ticker):", value="KLSE:SUNCON").upper().strip()
            s_market = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                s_entry = st.number_input("Harga Beli (RM / $):", value=3.95, step=0.05, format="%.2f")
            with c2:
                s_sl = st.number_input("Stop Loss (RM / $):", value=3.75, step=0.05, format="%.2f")
            with c3:
                s_tp = st.number_input("Take Profit (RM / $):", value=4.46, step=0.05, format="%.2f")
                
            s_wyckoff = st.selectbox(
                "Fasa Kitaran Wyckoff Semasa:",
                ["Fasa C (Spring Shakeout)", "Fasa D (Mark-Up Breakout)", "Fasa B (Ujian Lantai)", "Fasa E (Terlajak Pucuk / Overbought)"]
            )
            
            s_catalyst = st.text_input("Pemangkin Utama (Catalyst):", value="Kontrak Mega Pusat Data Johor & Tempahan Rekod")
            
            st.markdown("---")
            st.markdown("<b>🔍 Soalan Ujian Kejujuran Minda (Mind 60%):</b>", unsafe_allow_html=True)
            s_fomo = st.checkbox("Saya tergesa-gesa mahu beli kerana saham ini sedang naik laju / hangat di media sosial.")
            
            submit_ai = st.form_submit_button("🤖 Minta Nasihat & Audit AI Mentor", use_container_width=True)

    with col_verdict:
        st.subheader("⚖️ Keputusan Audit & Teguran AI Mentor")
        
        # Jalankan Audit
        res = audit_stock_entry_decision(
            ticker=s_ticker,
            market=s_market,
            entry_price=s_entry,
            stop_loss=s_sl,
            take_profit=s_tp,
            capital_available=net_capital,
            wyckoff_phase=s_wyckoff,
            catalyst_reason=s_catalyst,
            is_fomo_news=s_fomo
        )

        if res["all_passed"]:
            play_audio_trigger("entry_success")
            st.markdown(f"""
            <div class="ai-mentor-box-green">
                <h2 style="color:#00E676; margin:0 0 10px 0;">🟢 LULUS BELI: DISIPLIN A+</h2>
                <h4 style="color:#FFFFFF; margin:0 0 10px 0;">Saham: {res['ticker']} ({res['market']}) | R:R: {res['rr_ratio']:.2f}x</h4>
                <p style="color:#D1FAE5; font-size:0.92rem; margin:0;">
                    <b>Ulasan Mentor:</b> Entri ini memenuhi kesemua 3 Tiang Utama DDNK. Tiada tanda FOMO, saiz risiko terkawal, dan fasa Wyckoff memihak kepada anda.
                    Anda dibenarkan membuka aplikasi Moomoo dan memasukkan pesanan <i>Limit Order</i> sekarang.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            play_audio_trigger("risk_warning")
            st.markdown(f"""
            <div class="ai-mentor-box-red">
                <h2 style="color:#FF5252; margin:0 0 10px 0;">🔴 DITOLAK: JANGAN BELI!</h2>
                <h4 style="color:#FFFFFF; margin:0 0 10px 0;">Saham: {res['ticker']} ({res['market']}) | R:R: {res['rr_ratio']:.2f}x</h4>
                <p style="color:#FECDD3; font-size:0.92rem; margin:0;">
                    <b>Teguran Keras Mentor:</b> Entri ini melanggar SOP disiplin! Jika anda teruskan juga belian ini, anda sedang mengulangi kesilapan kaunter <b>HL / DJT / MARA</b> yang telah meragut belasan ribu ringgit modal anda dahulu.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📋 Butiran Audit 3 Tiang DDNK:")
        
        st.markdown('<div class="ai-bubble"><b>🧠 Tiang 1: Mind (60% Psikologi & Emosi)</b><br>' + '<br>'.join(res['mind_feedback']) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-bubble"><b>💰 Tiang 2: Money (30% Pengurusan Risiko)</b><br>' + '<br>'.join(res['money_feedback']) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-bubble"><b>📊 Tiang 3: Method (10% Tekno-Fundamental)</b><br>' + '<br>'.join(res['method_feedback']) + '</div>', unsafe_allow_html=True)
