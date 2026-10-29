"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FORENSIK EKSTRIM: MEJA KAJIAN KEBODOHAN & KECERDIKAN SAYA (EDISI GFM & UMC AUDIT)
Audit Khas: Mengapa GFM Rugi Teruk (-18.6%) & Mengapa UMC Menggugat Portfolio (81.8% Pendedahan)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render_postmortem_dashboard(fx_rate: float = 4.0773):
    st.markdown("""
    <style>
        .extreme-card-red {
            background: linear-gradient(135deg, #2D1118 0%, #170A0E 100%);
            border: 2px solid #FF5252;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 6px 16px rgba(255, 82, 82, 0.25);
            margin-bottom: 15px;
        }
        .extreme-card-green {
            background: linear-gradient(135deg, #0A2920 0%, #061813 100%);
            border: 2px solid #00E676;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 6px 16px rgba(0, 230, 118, 0.25);
            margin-bottom: 15px;
        }
        .stat-badge-danger {
            background-color: rgba(255, 82, 82, 0.2);
            color: #FF5252;
            border: 1px solid #FF5252;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .stat-badge-success {
            background-color: rgba(0, 230, 118, 0.2);
            color: #00E676;
            border: 1px solid #00E676;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .quote-banner {
            background: #151A26;
            border-left: 5px solid #FF1744;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin: 15px 0;
            font-style: italic;
            color: #E2E8F0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="color:#FFFFFF; margin-bottom:0;">🧠 BEDAH SIASAT FORENSIK: KEBODOHAN & KECERDIKAN SAYA</h1>', unsafe_allow_html=True)
    st.caption("Audit Psikologi, Emosi & Pasca-Dagangan Tanpa Belas Kasihan (Mind 60% • Money 30% • Method 10%)")

    st.markdown("""
    <div class="quote-banner">
        ⚠️ <b>AUDIT KESILAPAN SEMASA:</b> "Kerugian bukan berpunca daripada pasaran yang jahat, tetapi berpunca daripada <b>EGO YANG ENGGAN MENGAKU SALAH</b> dan <b>TAMAK MELETAKKAN TELUR DALAM SATU BAKUL</b>!"
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # 1. PAPAN SKOR BENTO REALITI PAHIT
    # ----------------------------------------------------------------------------------
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown("""
        <div class="extreme-card-red">
            <small style="color:#FECDD3; font-weight:700;">⚠️ RUGI ATAS KERTAS SEMASA</small>
            <h2 style="color:#FF5252; margin:6px 0;">-RM 3,294.95</h2>
            <span class="stat-badge-danger">GFM: -RM 2,256 | UMC: -RM 1,038</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="extreme-card-red">
            <small style="color:#FECDD3; font-weight:700;">💸 KOS KEBODOHAN LEPAS (REALIZED)</small>
            <h2 style="color:#FF5252; margin:6px 0;">-RM 29,677.20</h2>
            <span class="stat-badge-danger">25 Trade Rugi / Lambat Cut Loss</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown("""
        <div class="extreme-card-green">
            <small style="color:#A7F3D0; font-weight:700;">💎 GANJARAN DISIPLIN (REALIZED)</small>
            <h2 style="color:#00E676; margin:6px 0;">+RM 62,824.40</h2>
            <span class="stat-badge-success">87 Trade Menang (77.0% Win Rate)</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown("""
        <div style="background:#1A1F2C; border:1px solid #2B384E; border-radius:12px; padding:20px;">
            <small style="color:#8E9AAF; font-weight:600;">💰 BAKI UNTUNG BERSIH SEBENAR</small>
            <h2 style="color:#29B6F6; margin:6px 0;">RM 33,147.30</h2>
            <small style="color:#00E676;">Aset Portfolio: RM 54,278.00</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 2. BEDAH SIASAT KHAS: KEBODOHAN GFM & UMC (HOT FOCUS)
    # ----------------------------------------------------------------------------------
    st.subheader("🔥 Bedah Siasat Eksklusif: Kebodohan Pada Pegangan Aktif (GFM & UMC)")

    c_gfm_audit, c_umc_audit = st.columns(2)

    with c_gfm_audit:
        st.markdown("""
        <div style="background:#221015; border:2px solid #FF1744; border-radius:12px; padding:20px;">
            <h3 style="color:#FF5252; margin-top:0;">🇲🇾 KLSE:0039 - GFM SERVICES BERHAD</h3>
            <p><b>Unit:</b> 56,400 Unit | <b>Kos Asal:</b> RM 12,126.00 (RM 0.215) | <b>Nilai Semasa:</b> RM 9,870.00 (RM 0.175)</p>
            <h4 style="color:#FF1744; margin:10px 0 5px 0;">🔴 RUGI KERTAS: -RM 2,256.00 (-18.60%)</h4>
            <hr style="border-color:#3A1A22;">
            <h4 style="color:#FFBB28;">💀 KENAPA BODOH? (AUDIT KESILAPAN TEKNIKAL & MINDA):</h4>
            <ul>
                <li><b>Gagal Cut Loss Awal (Melanggar SOP 7%-8%):</b> Pelan DDNK menetapkan toleransi rugi maksima 7% hingga 8%. Anda membiarkannya melepasi -10%, -15%, sehingga terperosok ke <b>-18.60%</b>!</li>
                <li><b>Hope Trading (Berharap Pada Keajaiban):</b> Anda enggan potong kerana 'berharap' ia akan melantun semula. Harapan bukan strategi pelaburan!</li>
                <li><b>Modal Mati (Opportunity Cost):</b> RM 9,870 anda terperangkap selama berbulan-bulan dalam kaunter lesu, sedangkan saham AI/Data Center Bursa lain terbang puluhan peratus.</li>
            </ul>
            <div style="background:#161D2B; border-left:4px solid #FF1744; padding:10px; border-radius:4px; margin-top:10px;">
                🚨 <b>AMARAN LANTAI KRITIKAL: RM 0.165</b><br>
                Jika harga bocor ke bawah <b>RM 0.165</b>, anda <b>WAJIB CUT LOSS</b> tanpa sebarang alasan! Jangan biarkan ia menjadi barah -30% atau -50%!
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_umc_audit:
        st.markdown("""
        <div style="background:#221015; border:2px solid #FF1744; border-radius:12px; padding:20px;">
            <h3 style="color:#FF5252; margin-top:0;">🇺🇸 NYSE:UMC - UNITED MICROELECTRONICS</h3>
            <p><b>Unit:</b> 581 Unit | <b>Kos Asal:</b> RM 45,446.20 ($19.260) | <b>Nilai Semasa:</b> RM 44,408.00 ($18.820)</p>
            <h4 style="color:#FF1744; margin:10px 0 5px 0;">🔴 RUGI KERTAS: -RM 1,038.20 (-2.30%)</h4>
            <hr style="border-color:#3A1A22;">
            <h4 style="color:#FFBB28;">💀 KENAPA BODOH? (AUDIT PENDEDAHAN MODAL & PENGURUSAN RISIKO):</h4>
            <ul>
                <li><b>Over-Allocation Ekstrim (81.8% Modal Terkumpul Di Sini!):</b> Daripada portfolio aktif RM 54k, sebanyak RM 45.4k dilonggokkan pada UMC sahaja! Ini melanggar hukum asas Money 30% (Maksimum 20%-25% per kaunter).</li>
                <li><b>Impak Gandaan Nilai Ringgit:</b> Walaupun peratus rugi kecil (-2.30%), impak ringgitnya besar (-RM 1,038) kerana saiz lot anda terlalu gergasi untuk akaun ini!</li>
                <li><b>Gagal Kunci Untung di Puncak:</b> Pada Ogos 2026, UMC mencecah $21.07 (Untung > RM 4,000 atas kertas). Anda tamak dan tidak memasang Trailing Stop, membiarkan untung itu hilang dan bertukar menjadi rugi!</li>
            </ul>
            <div style="background:#161D2B; border-left:4px solid #FF1744; padding:10px; border-radius:4px; margin-top:10px;">
                🚨 <b>AMARAN LANTAI KRITIKAL: $18.50</b><br>
                Had lantai sokongan Wall Street ialah <b>$18.50</b>. Jika bocor, kurangkan posisi sekurang-kurangnya separuh untuk menyedut balik modal dan menghentikan pendarahan akaun!
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 3. CARTA WATERFALL KEBOCORAN MODAL
    # ----------------------------------------------------------------------------------
    st.subheader("📉 Carta Forensik: Jejak Kebocoran Modal Terkumpul")
    st.caption("Lihat bagaimana kesilapan membiarkan rugi membesar menghakis untung kasar RM 62.8k anda:")

    wf_fig = go.Figure(go.Waterfall(
        name="Aliran Untung Bersih",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
        x=[
            "Untung Kasar 87 Trade",
            "Tragedi HL (US)",
            "Tragedi MARA (US)",
            "Tragedi DJT (2 Trade)",
            "Tragedi SCIENTX",
            "Rugi Kertas GFM",
            "Rugi Kertas UMC",
            "Lain-lain Kerugian",
            "Baki Bersih Di Tangan"
        ],
        text=[
            "+RM 62,824",
            "-RM 4,607",
            "-RM 4,027",
            "-RM 5,867",
            "-RM 2,116",
            "-RM 2,256",
            "-RM 1,038",
            "-RM 9,766",
            "RM 33,147"
        ],
        y=[62824.40, -4607.19, -4026.76, -5866.99, -2115.96, -2256.00, -1038.20, -9766.00, 33147.30],
        connector={"line": {"color": "#8E9AAF"}},
        decreasing={"marker": {"color": "#FF5252"}},
        increasing={"marker": {"color": "#00E676"}},
        totals={"marker": {"color": "#29B6F6"}}
    ))

    wf_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=400,
        margin=dict(l=30, r=30, t=40, b=30),
        yaxis=dict(title="Nilai Aliran Modal (MYR)", gridcolor="#222B3D", tickprefix="RM ")
    )
    st.plotly_chart(wf_fig, width="stretch")

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 4. TAB SEJARAH KECERDIKAN & SUMPAH DISIPLIN
    # ----------------------------------------------------------------------------------
    t1, t2, t3 = st.tabs([
        "🟢 1. Sejarah Kemenangan Cerdik (+RM 22,230)",
        "📜 2. 5 Sumpah Keramat Disiplin DDNK",
        "📝 3. Borang Audit & Muhasabah Diri"
    ])

    with t1:
        st.subheader("🟢 Bukti Bahawa Anda Sebenarnya Mampu Buat Duit (Kecerdikan Disiplin)")
        top_win_df = pd.DataFrame([
            {"No": 1, "Ticker": "HIMX (US)", "Untung": "RM 9,498.22", "ROI": "+15.91%", "Kunci Kecerdikan": "Entri lantai Wyckoff $13.10, sabar biarkan untung berkembang ke $15.23."},
            {"No": 2, "Ticker": "NOK (US)", "Untung": "RM 3,487.55", "ROI": "+3.45%", "Kunci Kecerdikan": "Saiz lot matematik sempurna (1,779 unit). Kenaikan kecil +3.4% menghasilkan ribuan ringgit!"},
            {"No": 3, "Ticker": "UMC (US - Ogos)", "Untung": "RM 3,293.03", "ROI": "+4.00%", "Kunci Kecerdikan": "Disiplin TP AND CLOSE: Jual tepat pada sasaran $21.07 tanpa tamak."},
            {"No": 4, "Ticker": "HIMX (US - Jun)", "Untung": "RM 3,027.67", "ROI": "+5.45%", "Kunci Kecerdikan": "Entri Fasa D Wyckoff $20.80 bersama aliran Jerung Institusi."},
            {"No": 5, "Ticker": "FRSH (US)", "Untung": "RM 2,923.38", "ROI": "+4.60%", "Kunci Kecerdikan": "Eksekusi pantas tanpa ragu-ragu di zon asas sokongan $13.80."}
        ])
        st.dataframe(top_win_df, width="stretch", hide_index=True)

    with t2:
        st.subheader("📜 5 Sumpah Keramat Pelabur Institusi Haddy Pro")
        st.markdown("""
        1. 🛑 **AKU TIDAK AKAN SESEKALI MEMEGANG SAHAM RUGI MELEPASI -8%.**  
           *Ingat GFM: Menahan rugi kononnya nak tunggu melantun telah menyebabkan modal RM 12k terperangkap pada -18.6%!*

        2. 🛡️ **AKU TIDAK AKAN MEMASUKKAN LEBIH 25% MODAL DALAM SATU KAUNTER.**  
           *Ingat UMC: Meletakkan 81.8% modal dalam satu saham membunuh diversifikasi dan mendedahkan akaun kepada risiko besar.*

        3. 🔒 **AKU AKAN MEMASANG TRAILING STOP BILA UNTUNG SUDAH MELEPASI SASARAN PERTAMA.**  
           *Jangan sesekali membiarkan posisi untung berbalik menjadi posisi rugi seperti UMC sekarang.*

        4. 🧘 **AKU TIDAK AKAN BERDENDAM DENGAN PASARAN (NO REVENGE TRADING).**  
           *Bila rugi, tutup laptop. Pasaran akan dibuka semula esok.*

        5. 📐 **AKU PERCAYA KEPADA MATEMATIK SAIZ LOT, BUKAN PADA HARAPAN.**  
           *Harapan adalah racun. Matematik dan disiplin adalah pembina kekayaan.*
        """)

    with t3:
        st.subheader("📝 Borang Muhasabah & Tindakan Serta-Merta")
        with st.form("action_plan_form"):
            st.write("Catatkan pelan tindakan anda untuk menyelamatkan modal:")
            act_gfm = st.selectbox("Tindakan Terhadap GFM Services (RM 0.175):", [
                "Pasang Had Lantai Ketat RM 0.165 (Jika bocor terus Cut Loss)",
                "Jual Sekarang dan Alihkan Modal ke Saham Top 10 Meja Keputusan",
                "Kekal Pegang (Risiko Sendiri)"
            ])
            act_umc = st.selectbox("Tindakan Terhadap UMC ($18.82):", [
                "Pasang Had Lantai Ketat $18.50 (Jika bocor terus Cut Loss)",
                "Kurangkan Separuh Unit untuk Kurangkan Pendedahan 81.8%",
                "Kekal Pegang Menunggu Pemulihan Sektor Cip"
            ])
            submit_plan = st.form_submit_button("💾 Kunci Pelan Tindakan ke Dalam Minda Robot", width="stretch")
            if submit_plan:
                st.success("✅ Pelan tindakan dikunci! Laksanakan di Moomoo mengikut arahan yang telah anda tetapkan!")