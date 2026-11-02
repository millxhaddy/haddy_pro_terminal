"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 2: AI CO-PILOT "MENTOR DAGANGAN DDNK" (INTERACTIVE AI TRADING ADVISOR)
Penasihat Disiplin Keras: Saringan Ketat 3 Tiang DDNK (Mind 60%, Money 30%, Method 10%)
========================================================================================
"""

import streamlit as st

def audit_stock_entry_decision(
    ticker: str,
    market: str,
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    wyckoff_phase: str,
    catalyst_reason: str,
    is_fomo_news: bool
) -> dict:
    """
    Enjin Logik AI Mentor DDNK: Menyemak 3 Tiang Disiplin & Menjana Keputusan Muktamad.
    """
    prices_valid = (
        entry_price > 0
        and stop_loss > 0
        and stop_loss < entry_price
        and take_profit > entry_price
    )
    risk_unit = entry_price - stop_loss if prices_valid else 0.0
    reward_unit = take_profit - entry_price if prices_valid else 0.0
    rr_ratio = round(reward_unit / risk_unit, 2) if prices_valid else 0.0
    
    # 1. Audit Mind (60%)
    mind_passed = (
        not is_fomo_news
        and wyckoff_phase in ["Fasa C (Spring Shakeout)", "Fasa D (Mark-Up Breakout)"]
    )
    mind_feedback = []
    if is_fomo_news:
        mind_feedback.append("❌ FOMO ditandakan dalam jawapan anda.")
    else:
        mind_feedback.append("✅ FOMO tidak ditandakan dalam jawapan anda.")
        
    if wyckoff_phase == "Fasa B (Ujian Lantai)":
        mind_feedback.append("⚠️ Fasa B dipilih; fasa pasaran tidak disahkan oleh aplikasi.")
    elif wyckoff_phase == "Fasa C (Spring Shakeout)":
        mind_feedback.append("✅ Fasa C dipilih pengguna; aplikasi tidak mengesahkan corak carta.")
    elif wyckoff_phase == "Fasa D (Mark-Up Breakout)":
        mind_feedback.append("✅ Fasa D dipilih pengguna; aplikasi tidak mengesahkan corak carta.")
    else:
        mind_feedback.append("❌ Fasa belum disahkan atau Fasa E dipilih.")

    # 2. Audit Money (30%)
    money_passed = prices_valid and rr_ratio >= 2.50
    money_feedback = []
    if not prices_valid:
        money_feedback.append(
            "❌ Harga perlu sah: entri dan stop loss positif, stop loss di bawah entri, "
            "dan sasaran di atas entri."
        )
    elif rr_ratio >= 2.50:
        money_feedback.append(f"✅ Nisbah ganjaran/risiko input ialah {rr_ratio}x (ambang 2.50x).")
    else:
        money_feedback.append(f"❌ Nisbah ganjaran/risiko input ialah {rr_ratio}x (di bawah ambang 2.50x).")

    # 3. Audit Method (10%)
    method_passed = len(catalyst_reason.strip()) >= 5
    method_feedback = []
    if method_passed:
        method_feedback.append(f"✅ Nota pemangkin dibekalkan pengguna: {catalyst_reason}")
    else:
        method_feedback.append("❌ Nota pemangkin tidak dibekalkan.")

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

def render_ai_copilot_ui():
    st.header("Semakan senarai dagangan")
    st.caption(
        "Semakan matematik berdasarkan input anda sahaja. Fasa carta dan pemangkin "
        "tidak disahkan; hasil bukan nasihat atau arahan beli/jual."
    )

    col_in, col_verdict = st.columns([5, 5])

    with col_in:
        st.subheader("Input senario")
        with st.form("ai_copilot_form"):
            s_ticker = st.text_input("Kod saham (ticker):", value="").upper().strip()
            s_market = st.selectbox("Pasaran:", ["Bursa Malaysia", "Wall Street US"])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                s_entry = st.number_input("Harga entri (RM / $):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
            with c2:
                s_sl = st.number_input("Stop loss (RM / $):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
            with c3:
                s_tp = st.number_input("Sasaran (RM / $):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
                
            s_wyckoff = st.selectbox(
                "Fasa Kitaran Wyckoff Semasa:",
                ["Belum dinilai", "Fasa C (Spring Shakeout)", "Fasa D (Mark-Up Breakout)", "Fasa B (Ujian Lantai)", "Fasa E (Terlajak Pucuk / Overbought)"]
            )
            
            s_catalyst = st.text_input("Nota pemangkin (input sendiri):", value="")
            
            st.markdown("---")
            st.markdown("<b>🔍 Soalan Ujian Kejujuran Minda (Mind 60%):</b>", unsafe_allow_html=True)
            s_fomo = st.checkbox("Saya tergesa-gesa mahu beli kerana saham ini sedang naik laju / hangat di media sosial.")
            
            submit_ai = st.form_submit_button("Semak input", width="stretch")

    with col_verdict:
        st.subheader("Hasil semakan")
        if not submit_ai:
            st.info("Isi andaian sendiri dan pilih “Semak input” untuk melihat nisbah serta checklist.")
        elif not s_ticker:
            st.warning("Masukkan ticker sebelum menyemak.")
        else:
            res = audit_stock_entry_decision(
                ticker=s_ticker,
                market=s_market,
                entry_price=s_entry,
                stop_loss=s_sl,
                take_profit=s_tp,
                wyckoff_phase=s_wyckoff,
                catalyst_reason=s_catalyst,
                is_fomo_news=s_fomo,
            )
            st.metric("Nisbah ganjaran/risiko input", f"{res['rr_ratio']:.2f}x")
            if res["all_passed"]:
                st.success(
                    "Input melepasi ambang checklist yang dipilih. Ini bukan "
                    "pengesahan pasaran atau cadangan transaksi."
                )
            else:
                st.warning(
                    "Satu atau lebih input tidak melepasi checklist; semakan ini "
                    "bukan arahan untuk membeli atau menjual."
                )
            st.markdown("**Semakan emosi**")
            for feedback in res["mind_feedback"]:
                st.write(feedback)
            st.markdown("**Semakan nisbah**")
            for feedback in res["money_feedback"]:
                st.write(feedback)
            st.markdown("**Nota pengguna**")
            for feedback in res["method_feedback"]:
                st.write(feedback)
