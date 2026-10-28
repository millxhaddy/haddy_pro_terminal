"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 20: PROTOKOL KRISIS 'BLACK SWAN', PEMUTUS LITAR & MANUAL OPERASI HARIAN 15 MINIT
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from risk_calculator_audio import play_audio_trigger

def initialize_crisis_state():
    if "circuit_breaker_active" not in st.session_state:
        st.session_state["circuit_breaker_active"] = False

def render_crisis_playbook_ui(net_equity: float = 55945.32):
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
                <h3 style="color:#00E676; margin:0 0 6px 0;">🟢 STATUS PASARAN: OPERASI NORMAL & TERKAWAL</h3>
                <p style="color:#D1FAE5; font-size:0.9rem; margin:0;">
                    Pemutus litar berada dalam mod sedia (*standby*). Eksekusi belian mengikut Meja Keputusan Harian dibenarkan sekiranya melepasi saringan AI Mentor.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col_cb2:
        st.markdown("<br>", unsafe_allow_html=True)
        if not st.session_state["circuit_breaker_active"]:
            if st.button("🚨 CETUSKAN PEMUTUS LITAR", width="stretch"):
                st.session_state["circuit_breaker_active"] = True
                play_audio_trigger("risk_warning")
                st.rerun()
        else:
            if st.button("🟢 NYAHAKTIFKAN / RESET NORMAL", width="stretch"):
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
            port_val = st.number_input("Nilai Ekuiti Portfolio Dilindungi (MYR):", value=float(net_equity), step=1000.0)
            crash_scenario = st.select_slider("Senario Kejatuhan Indeks Pasaran (%):", options=[-5, -10, -15, -20, -30], value=-10)
            hedge_pct = st.slider("Sasaran Perlindungan Lindung Nilai (%):", 20, 100, 50, step=10)

        with c_h2:
            potential_loss = port_val * abs(crash_scenario / 100.0)
            hedged_coverage = potential_loss * (hedge_pct / 100.0)
            gold_needed = hedged_coverage * 0.60
            cash_needed = hedged_coverage * 0.40

            st.markdown(f"""
            <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
                <h4 style="color:#FFBB28; margin-top:0;">📊 Analisis Impak & Penampan Krisis:</h4>
                <p><b>Potensi Penarikan Modal ({crash_scenario}%):</b> <span style="color:#FF5252; font-weight:700;">-RM {potential_loss:,.2f}</span></p>
                <p><b>Nilai Perlindungan Sasaran ({hedge_pct}%):</b> <span style="color:#00E676; font-weight:700;">RM {hedged_coverage:,.2f}</span></p>
                <hr style="border-color:#2B384E;">
                <h5 style="color:#29B6F6; margin-bottom:6px;">Cadangan Struktur Lindung Nilai Institusi:</h5>
                <ul>
                    <li><b>Emas Fizikal / ETF GLD (60%):</b> Peruntukkan <b>RM {gold_needed:,.2f}</b></li>
                    <li><b>Tunai Bersih / Pasaran Wang (40%):</b> Kunci rizab tunai <b>RM {cash_needed:,.2f}</b></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

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
                <li>Semak kedudukan pegangan aktif tempatan (kaunter <b>GFM Services</b>).</li>
                <li>Semak Tab <b>🛡️ Trailing Stop Sentinel</b>: Pastikan tiada saham yang menyentuh garisan amaran pemotongan modal.</li>
                <li>Sifar aktiviti dagangan baharu waktu rehat tengah hari (elakkan terperangkap volatiliti rendah).</li>
            </ul>
        </div>

        <div class="sop-step">
            <h4 style="color:#FFBB28; margin:0 0 4px 0;">🌆 3. Sesi Malam (08:30 PM - 08:45 PM MYT) • Pra-Wall Street US</h4>
            <ul>
                <li>Buka Tab <b>📡 Radar Makro & Multimedia</b>: Semak sebut harga Minyak Brent ($115/bbl) dan sentimen mesyuarat FOMC Fed.</li>
                <li>Semak Tab <b>🎯 Meja Keputusan US</b>: Teliti calon entri AI (NVDA, MSFT, META).</li>
                <li>Gunakan Tab <b>🧮 Kalkulator 3M</b> untuk mengunci saiz unit pesanan Moomoo sebelum loceng New York berbunyi jam 9:30 PM.</li>
            </ul>
        </div>

        <div class="sop-step">
            <h4 style="color:#E040FB; margin:0 0 4px 0;">🌙 4. Sesi Malam Lewat (11:30 PM - 11:40 PM MYT) • Pasca-Dagangan & Audit Diri</h4>
            <ul>
                <li>Semak kedudukan posisi aktif global (kaunter <b>UMC</b>): Kunci <i>Trailing Stop</i> jika untung melepasi sasaran pertama.</li>
                <li>Buka Tab <b>⚡ Meja Beli/Jual</b>: Rekodkan sebarang transaksi jual/beli yang telah dipadankan broker.</li>
                <li>Baca sekilas <b>5 Sumpah Keramat DDNK</b> di Tab 18 bagi mengekalkan ketenangan minda sebelum tidur.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
