"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL KHAS: ENJIN PEMIKIRAN ROBOT / AI & PAPAN TANDA AMARAN BAHAYA (CYBORG SENTINEL)
Menggantikan Kelemahan Biologi Manusia dengan Logik Dingin Komputer & Algoritma
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from risk_calculator_audio import play_audio_trigger

def render_robot_mindset_hud():
    """
    Paparan Jalur Status Minda Robotik (Cognitive HUD) di bahagian atas terminal.
    """
    st.markdown("""
    <style>
        .robot-hud-wrap {
            background: linear-gradient(90deg, #1A0A0E 0%, #151A26 50%, #0A1F18 100%);
            border: 2px solid #FFBB28;
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .robot-text {
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.88rem;
            color: #FFFFFF;
            font-weight: 700;
        }
        .robot-alert-tag {
            background-color: #FF1744;
            color: #FFFFFF;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            animation: pulse-red 2s infinite;
        }
        @keyframes pulse-red {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
    <div class="robot-hud-wrap">
        <div class="robot-text">
            🤖 <b>AI DIRECTIVE PROTOCOL:</b> <span style="color:#00E676;">EMOSI: 0%</span> | <span style="color:#29B6F6;">MATEMATIK: 100%</span> | <span style="color:#FFD700;">STOP LOSS: MANDATORI</span>
        </div>
        <div>
            <span class="robot-alert-tag">ANTI-FOMO SHIELD: ACTIVE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_traffic_light_evaluator():
    """
    Sistem Lampu Isyarat Tiga Warna & Pintu Kawalan Logik Mesin.
    """
    st.markdown("""
    <style>
        .light-box-green {
            background: linear-gradient(135deg, #0A281E 0%, #05140F 100%);
            border: 3px solid #00E676;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.3);
            margin-bottom: 15px;
        }
        .light-box-yellow {
            background: linear-gradient(135deg, #2D2512 0%, #171206 100%);
            border: 3px solid #FFBB28;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(255, 187, 40, 0.3);
            margin-bottom: 15px;
        }
        .light-box-red {
            background: linear-gradient(135deg, #380C14 0%, #1C0509 100%);
            border: 3px solid #FF1744;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(255, 23, 68, 0.4);
            margin-bottom: 15px;
        }
        .signboard-caution {
            background-color: #171E2D;
            border-left: 5px solid #FF1744;
            padding: 12px 18px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
            color: #E2E8F0;
            font-size: 0.9rem;
        }
        .mantra-card {
            background: #141A26;
            border: 1px dashed #2B384E;
            border-radius: 10px;
            padding: 14px;
            text-align: center;
            font-style: italic;
            color: #CBD5E1;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🚦 Sistem Lampu Isyarat Algoritmik & Pintu Kawalan Minda Robot")
    st.caption("Uji keadaan emosi dan kelayakan teknikal anda sebelum meletakkan sebarang pesanan di broker.")

    col_t1, col_t2 = st.columns([5, 5])

    with col_t1:
        st.subheader("📋 Saringan Pra-Eksekusi (Human vs Machine Checklist)")
        st.write("Jawab soalan ini dengan jujur. Komputer tidak menerima penipuan.")

        q1 = st.checkbox("1. Adakah harga saham berada TEPAT di lantai sokongan (bukan sedang mengejar kenaikan hijau)?")
        q2 = st.checkbox("2. Adakah nisbah potensi keuntungan (R:R) telah disahkan melebihi 2.50x?")
        q3 = st.checkbox("3. Adakah Stop Loss telah ditetapkan secara rasmi di Moomoo (bukan stop loss mental dalam kepala)?")
        q4 = st.checkbox("4. Adakah saiz risiko modal terhad kepada maksimum 1.5% - 2.0% daripada jumlah portfolio?")
        q5 = st.checkbox("5. Bebas daripada dendam (Revenge Trading) atau rasa takut tertinggal bas (FOMO)?")

        st.markdown("---")
        st.markdown("#### 🛑 Semakan Amaran Gejala Emosi Manusia:")
        warn_fomo = st.checkbox("⚠️ Saya rasa terdesak nak beli sebab takut harga terbang esok.")
        warn_hope = st.checkbox("⚠️ Saya enggan potong kerugian kerana 'berharap' ia akan naik semula.")
        warn_revenge = st.checkbox("⚠️ Saya baru sahaja rugi dalam trade lepas dan nak tebus balik secepat mungkin.")

    # Logik Lampu Isyarat
    score = sum([q1, q2, q3, q4, q5])
    has_fatal_emotion = warn_fomo or warn_hope or warn_revenge

    with col_t2:
        st.subheader("🚦 Keputusan Lampu Isyarat Sistem")

        if has_fatal_emotion or score <= 2:
            play_audio_trigger("risk_warning")
            st.markdown("""
            <div class="light-box-red">
                <h1 style="color:#FF1744; margin:0 0 8px 0;">🔴 LAMPU MERAH: DANGER / HALT!</h1>
                <h3 style="color:#FFFFFF; margin:0 0 10px 0;">DILARANG MEMBELI SAMA SEKALI!</h3>
                <p style="color:#FECDD3; font-size:0.95rem; margin:0;">
                    <b>DIAGNOSTIK AI:</b> Minda anda sedang dipengaruhi oleh hormon Tamak / Takut / Dendam.
                    Ini adalah punca yang sama yang menyebabkan tragedi <b>HL (-RM 4.6k)</b> dan <b>DJT (-RM 5.8k)</b>!
                    <br><br>
                    <b>TINDAKAN MANDATORI:</b> Letakkan tetikus, tutup laptop, dan minum air. Pasaran tidak lari ke mana. Jangan derma duit anda kepada jerung!
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif score in [3, 4]:
            st.markdown("""
            <div class="light-box-yellow">
                <h1 style="color:#FFBB28; margin:0 0 8px 0;">🟡 LAMPU KUNING: CAUTION / STANDBY</h1>
                <h3 style="color:#FFFFFF; margin:0 0 10px 0;">SYARAT BELUM CUKUP LENGKAP</h3>
                <p style="color:#FEF3C7; font-size:0.95rem; margin:0;">
                    <b>DIAGNOSTIK AI:</b> Setup ini ada potensi tetapi ada 1 atau 2 parameter disiplin yang anda abaikan (cth: R:R belum 2.50x atau tiada auto-SL).
                    <br><br>
                    <b>TINDAKAN MANDATORI:</b> Jangan beli harga pasaran (Market Order). Letakkan <i>Limit Order</i> di lantai sokongan dan tunggu pasaran datang kepada anda.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            play_audio_trigger("entry_success")
            st.markdown("""
            <div class="light-box-green">
                <h1 style="color:#00E676; margin:0 0 8px 0;">🟢 LAMPU HIJAU: SAFE / EXECUTE LIKE A ROBOT</h1>
                <h3 style="color:#FFFFFF; margin:0 0 10px 0;">SEMUA 5 TIANG DISIPLIN LULUS PENUH</h3>
                <p style="color:#D1FAE5; font-size:0.95rem; margin:0;">
                    <b>DIAGNOSTIK AI:</b> Sifar unsur emosi. Matematik tepat, zon lantai disahkan, had kerugian dilindungi.
                    <br><br>
                    <b>TINDAKAN MANDATORI:</b> Eksekusi pesanan dengan tenang seperti mesin. Setelah beli, kunci Stop Loss dan biarkan pasaran bekerja.
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # PAPAN TANDA AMARAN BAHAYA & MANTRA MESIN
    # ----------------------------------------------------------------------------------
    st.subheader("⚠️ Papan Tanda Amaran Bahaya & Peringatan Kubur Modal")

    c_s1, c_s2 = st.columns(2)

    with c_s1:
        st.markdown("""
        <div class="signboard-caution">
            <h4 style="color:#FF1744; margin:0 0 4px 0;">💀 KAWASAN KEMATIAN MODAL #1: HARAPAN (HOPE)</h4>
            Harapan bukan strategi pelaburan! Bila harga saham pecah garisan sokongan, ia tidak peduli berapa banyak anda berdoa. Potong kerugian serta-merta semasa ia masih kecil (2%).
        </div>
        <div class="signboard-caution">
            <h4 style="color:#FF1744; margin:0 0 4px 0;">💀 KAWASAN KEMATIAN MODAL #2: FOMO MEDIA MASSA</h4>
            Bila berita keluar di televisyen atau media sosial mengatakan saham sedang terbang, jerung institusi sebenarnya sedang mencari pembeli naif untuk membuang pegangan mereka!
        </div>
        <div class="signboard-caution">
            <h4 style="color:#FF1744; margin:0 0 4px 0;">💀 KAWASAN KEMATIAN MODAL #3: DENDAM (REVENGE TRADING)</h4>
            Rugi satu trade adalah normal. Tetapi cuba membalas dendam untuk 'tebus balik' duit yang hilang pada hari yang sama akan menghancurkan 20% hingga 50% akaun anda.
        </div>
        """, unsafe_allow_html=True)

    with c_s2:
        st.markdown("""
        <div class="mantra-card" style="border-color:#00E676; margin-bottom:10px;">
            <h4 style="color:#00E676; margin:0 0 4px 0;">🤖 MANTRA MESIN #1</h4>
            "Komputer tidak mempunyai perasaan bangga bila menang, dan tidak rasa sedih bila kena stop loss. Berfikirlah seperti komputer."
        </div>
        <div class="mantra-card" style="border-color:#29B6F6; margin-bottom:10px;">
            <h4 style="color:#29B6F6; margin:0 0 4px 0;">🤖 MANTRA MESIN #2</h4>
            "Untung besar bukan hasil daripada tekaan hebat, tetapi hasil daripada memotong kerugian dengan pantas dan membiarkan pemenang berlari."
        </div>
        <div class="mantra-card" style="border-color:#FFBB28;">
            <h4 style="color:#FFBB28; margin:0 0 4px 0;">🤖 MANTRA MESIN #3</h4>
            "Tugas anda bukan meramal masa depan pasaran. Tugas anda hanyalah menguruskan risiko matematik pada setiap posisi."
        </div>
        """, unsafe_allow_html=True)
