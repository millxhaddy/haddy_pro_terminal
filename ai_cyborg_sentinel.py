"""User-operated trading checklist; it does not monitor markets or authorize orders."""

import streamlit as st


def render_robot_mindset_hud():
    st.caption(
        "Peringatan: checklist ini manual. Ia tidak mengesahkan harga, stop loss, "
        "risiko posisi atau keadaan pasaran."
    )


def render_traffic_light_evaluator():
    st.subheader("Checklist kendiri sebelum dagangan")
    st.caption(
        "Semua jawapan diisi sendiri dan tidak disahkan oleh aplikasi. Hasilnya "
        "bukan isyarat pasaran atau arahan untuk bertransaksi."
    )
    with st.form("trading_self_check_form"):
        price_checked = st.checkbox("Saya telah mengesahkan harga daripada sumber broker.")
        reward_risk_checked = st.checkbox("Saya telah mengira nisbah ganjaran/risiko daripada input sendiri.")
        stop_checked = st.checkbox("Saya telah menyemak pesanan stop loss pada platform broker.")
        sizing_checked = st.checkbox("Saya telah menyemak saiz risiko berbanding had peribadi.")
        calm_checked = st.checkbox("Saya tidak bertindak kerana FOMO atau mahu membalas kerugian.")
        emotional_flags = [
            st.checkbox("Saya berasa terdesak mengejar harga."),
            st.checkbox("Saya bercadang menambah posisi kerana berharap kerugian akan pulih."),
            st.checkbox("Saya mahu membalas kerugian dagangan dengan segera."),
        ]
        submitted = st.form_submit_button("Semak checklist", width="stretch")

    if not submitted:
        st.info("Jawab checklist dan hantar untuk melihat ringkasan kendiri.")
        return
    score = sum(
        (
            price_checked,
            reward_risk_checked,
            stop_checked,
            sizing_checked,
            calm_checked,
        )
    )
    if any(emotional_flags):
        st.warning(
            f"{score}/5 item checklist ditandakan. Anda juga menandakan tekanan "
            "emosi; pertimbangkan untuk berhenti dan menilai semula."
        )
    elif score == 5:
        st.success(
            "Semua item ditandakan oleh pengguna. Aplikasi tidak mengesahkan "
            "kebenaran jawapan atau memberi kelulusan transaksi."
        )
    else:
        st.info(f"{score}/5 item checklist ditandakan; item lain belum disahkan.")
