"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 20: PROTOKOL KRISIS 'BLACK SWAN', PEMUTUS LITAR & MANUAL OPERASI HARIAN 15 MINIT
========================================================================================
"""

import streamlit as st
from risk_calculator_audio import play_audio_trigger

def initialize_crisis_state():
    if "circuit_breaker_active" not in st.session_state:
        st.session_state["circuit_breaker_active"] = False

def render_crisis_playbook_ui(net_equity: float | None = None):
    initialize_crisis_state()

    st.markdown("""
    <style>
        .crisis-card-red {
            background: linear-gradient(135deg, #3A0D16 0%, #1A060A 100%);
            border: 2px solid #FF1744;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 20px rgba(255, 23, 68, 0.35);
            margin-bottom: 20px;
        }
        .crisis-card-green {
            background: linear-gradient(135deg, #0A281E 0%, #05140F 100%);
            border: 2px solid #00E676;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 20px rgba(0, 230, 118, 0.25);
            margin-bottom: 20px;
        }
        .sop-step {
            background-color: #171E2D;
            border-left: 4px solid #29B6F6;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
            color: #E2E8F0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🚨 Protokol Krisis 'Black Swan' & Manual Operasi Harian (SOP)")
    st.caption("Pusat Kawalan Kecemasan Pertahanan Modal & Panduan Disiplin Harian 15 Minit Pelabur Institusi.")

    # ----------------------------------------------------------------------------------
    # 1. BUTANG PEMUTUS LITAR KECEMASAN (CIRCUIT BREAKER)
    # ----------------------------------------------------------------------------------
    col_cb1, col_cb2 = st.columns([7, 3])

    with col_cb1:
        if st.session_state["circuit_breaker_active"]:
            st.markdown("""
            <div class="crisis-card-red">
                <h2 style="color:#FF1744; margin:0 0 8px 0;">🛑 PEMUTUS LITAR KECEMASAN DIAKTIFKAN!</h2>
                <h4 style="color:#FFFFFF; margin:0 0 8px 0;">MOD DEFANSIF: SEMUA AKTIVITI PEMBELIAN DIBEKUKAN</h4>
                <p style="color:#FECDD3; font-size:0.92rem; margin:0;">
                    Pasaran sedang mengalami anomali kejatuhan tajam atau kejutan geopolitik ekstrem. 
                    <b>DILARANG membuka posisi baharu!</b> Fokus kepada perlindungan modal, semak trailing stop, dan pertahankan baki tunai.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="crisis-card-green">
                <h3 style="color:#00E676; margin:0 0 6px 0;">Kawalan manual tidak diaktifkan</h3>
                <p style="color:#D1FAE5; font-size:0.9rem; margin:0;">
                    Kawalan ini tidak memantau pasaran dan status tidak bermaksud keadaan pasaran normal.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col_cb2:
        st.markdown("<br>", unsafe_allow_html=True)
        if not st.session_state["circuit_breaker_active"]:
            if st.button("Aktifkan jeda manual", width="stretch"):
                st.session_state["circuit_breaker_active"] = True
                play_audio_trigger("risk_warning")
                st.rerun()
        else:
            if st.button("Matikan jeda manual", width="stretch"):
                st.session_state["circuit_breaker_active"] = False
                play_audio_trigger("entry_success")
                st.rerun()

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 2. DUA SUB-TAB: KALKULATOR LINDUNG NILAI & MANUAL RUTIN 15 MINIT
    # ----------------------------------------------------------------------------------
    sub_hedge, sub_sop = st.tabs([
        "🛡️ 1. Kalkulator Lindung Nilai Pantas (Hedging Shield)",
        "📖 2. Manual Rutin Harian 15 Minit (Daily SOP)"
    ])

    with sub_hedge:
        st.subheader("🛡️ Kalkulator Lindung Nilai Semasa Krisis (Crash-Shield)")
        st.caption("Kira peruntukan penampan tunai dan pendedahan emas safe-haven untuk menyerap impak kejatuhan pasaran.")

        c_h1, c_h2 = st.columns(2)
        with c_h1:
            port_val = st.number_input(
                "Nilai portfolio untuk senario ini (input/sumber, RM):",
                min_value=0.0,
                value=float(net_equity or 0.0),
                step=1000.0,
            )
            crash_scenario = st.select_slider("Senario Kejatuhan Indeks Pasaran (%):", options=[-5, -10, -15, -20, -30], value=-10)
            hedge_pct = st.slider("Sasaran perlindungan untuk ilustrasi (%):", 20, 100, 50, step=10)

        with c_h2:
            potential_loss = port_val * abs(crash_scenario / 100.0)
            hedged_coverage = potential_loss * (hedge_pct / 100.0)
            if port_val <= 0:
                st.info("Masukkan nilai portfolio yang disahkan; tiada nilai lalai digunakan.")
            else:
                st.metric(
                    f"Anggaran perubahan pada senario {crash_scenario}%",
                    f"-RM {potential_loss:,.2f}",
                )
                st.metric(
                    f"Sasaran perlindungan ilustrasi ({hedge_pct}%)",
                    f"RM {hedged_coverage:,.2f}",
                )
                st.caption(
                    "Pengiraan aritmetik berdasarkan andaian input; ia bukan ramalan "
                    "pasaran atau cadangan lindung nilai."
                )

    with sub_sop:
        st.subheader("📖 Manual Operasi Harian 15 Minit Pelabur Haddy Pro")
        st.caption("Rutin berdisiplin 4 fasa sehari yang membezakan pelabur berprestasi tinggi daripada pedagang emosi:")

        st.markdown("""
        <div class="sop-step">
            <h4 style="color:#00E676; margin:0 0 4px 0;">🌅 1. Sesi Pagi (07:30 AM - 07:45 AM MYT) • Pra-Bursa Malaysia</h4>
            <ul>
                <li>Buka emel Gmail anda untuk membaca <b>Taklimat Pasaran Pagi (Pre-Market Briefing)</b> automatik.</li>
                <li>Buka Tab <b>🎯 Meja Keputusan Harian</b>: Semak 3 saham Bursa Malaysia teratas.</li>
                <li>Jika ada calon entri sedia ada, masukkan pesanan <i>Limit Order</i> di platform Moomoo sebelum pasaran dibuka jam 9:00 AM.</li>
            </ul>
        </div>

        <div class="sop-step">
            <h4 style="color:#29B6F6; margin:0 0 4px 0;">☀️ 2. Sesi Tengah Hari (12:35 PM - 12:45 PM MYT) • Rehat Bursa</h4>
            <ul>
                <li>Semak pegangan aktif dan masa kemas kini sumber; jangan anggap harga tanpa cap masa sebagai sebut harga semasa.</li>
                <li>Semak Tab <b>🛡️ Trailing Stop Sentinel</b>: Pastikan tiada saham yang menyentuh garisan amaran pemotongan modal.</li>
                <li>Sifar aktiviti dagangan baharu waktu rehat tengah hari (elakkan terperangkap volatiliti rendah).</li>
            </ul>
        </div>

        <div class="sop-step">
            <h4 style="color:#FFBB28; margin:0 0 4px 0;">🌆 3. Sesi Malam (08:30 PM - 08:45 PM MYT) • Pra-Wall Street US</h4>
            <ul>
                <li>Buka tab radar makro dan semak sumber serta cap masa; jika tiada data, jangan anggap ia sebut harga semasa.</li>
                <li>Semak kaunter dalam senarai keputusan dan sahkan maklumat dengan sumber pasaran sebelum membuat keputusan.</li>
                <li>Gunakan Tab <b>🧮 Kalkulator 3M</b> untuk mengunci saiz unit pesanan Moomoo sebelum loceng New York berbunyi jam 9:30 PM.</li>
            </ul>
        </div>

        <div class="sop-step">
            <h4 style="color:#E040FB; margin:0 0 4px 0;">🌙 4. Sesi Malam Lewat (11:30 PM - 11:40 PM MYT) • Pasca-Dagangan & Audit Diri</h4>
            <ul>
                <li>Semak pegangan global yang benar-benar wujud dalam snapshot dan sahkan paras harga sebelum mengubah pesanan.</li>
                <li>Buka Tab <b>⚡ Meja Beli/Jual</b>: Rekodkan sebarang transaksi jual/beli yang telah dipadankan broker.</li>
                <li>Baca sekilas <b>5 Sumpah Keramat DDNK</b> di Tab 18 bagi mengekalkan ketenangan minda sebelum tidur.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
