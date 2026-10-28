"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FORENSIK EKSTRIM: MEJA KAJIAN KEBODOHAN & KECERDIKAN SAYA (FULL REPORT EDITION)
Audit Psikologi, Emosi & Pasca-Dagangan Tanpa Belas Kasihan (Mind 60% • Money 30%)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render_postmortem_dashboard(fx_rate: float = 4.0773):
    # CSS Custom untuk Paparan Gred Forensik Dark Bloomberg
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
            border-left: 5px solid #FFBB28;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin: 15px 0;
            font-style: italic;
            color: #E2E8F0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="color:#FFFFFF; margin-bottom:0;">🧠 BEDAH SIASAT FORENSIK: KEBODOHAN & KECERDIKAN SAYA</h1>', unsafe_allow_html=True)
    st.caption("Laporan Bedah Siasat Paling Mentah, Telus & Terperinci ke atas 113 Keputusan Hidup-Mati Dagangan Anda (Ogos 2024 - Oktober 2026)")

    st.markdown("""
    <div class="quote-banner">
        "Pasaran saham adalah mekanisme pemindahan kekayaan daripada mereka yang tidak sabar dan beremosi, kepada mereka yang berdisiplin dan tenang." — <b>Warren Buffett</b>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # 1. PARADOKS REALITI ANGKA (BENTO METRIKS)
    # ----------------------------------------------------------------------------------
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown("""
        <div class="extreme-card-green">
            <small style="color:#A7F3D0; font-weight:700;">💎 GANJARAN KECERDIKAN KASAR</small>
            <h2 style="color:#00E676; margin:6px 0;">+RM 62,824.40</h2>
            <span class="stat-badge-success">87 Dagangan Untung (77.0%)</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="extreme-card-red">
            <small style="color:#FECDD3; font-weight:700;">💸 KOS KEBODOHAN & EMOSI</small>
            <h2 style="color:#FF5252; margin:6px 0;">-RM 29,677.20</h2>
            <span class="stat-badge-danger">25 Dagangan Rugi (23.0%)</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown("""
        <div style="background:#1A1F2C; border:1px solid #2B384E; border-radius:12px; padding:20px;">
            <small style="color:#8E9AAF; font-weight:600;">⚠️ NISBAH PAYOFF (UNTUNG / RUGI)</small>
            <h2 style="color:#FFBB28; margin:6px 0;">0.61x</h2>
            <small style="color:#FF5252;">Purata Rugi (-RM 1,187) > Purata Untung (+RM 722)</small>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown("""
        <div style="background:#1A1F2C; border:1px solid #2B384E; border-radius:12px; padding:20px;">
            <small style="color:#8E9AAF; font-weight:600;">💰 BAKI UNTUNG BERSIH SEBENAR</small>
            <h2 style="color:#29B6F6; margin:6px 0;">RM 33,147.30</h2>
            <small style="color:#00E676;">+RM 282.83 Purata Expectancy Per Trade</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 2. CARTA AIR TERJUN KEBOCORAN MODAL (WATERFALL CHART)
    # ----------------------------------------------------------------------------------
    st.subheader("📉 Carta Forensik: Bagaimana RM 29,677.20 Hangus Terbakar?")
    st.caption("Visualisasi bagaimana untung kasar RM 62.8k dihakis oleh 5 kesilapan terbodoh sebelum meninggalkan baki RM 33.1k di tangan anda.")

    wf_fig = go.Figure(go.Waterfall(
        name="Aliran Untung Bersih",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "relative", "total"],
        x=[
            "Untung Kasar 87 Trade",
            "Tragedi HL (US)",
            "Tragedi MARA (US)",
            "Tragedi DJT #1",
            "Tragedi DJT #2 (Dendam)",
            "Tragedi SCIENTX (Bursa)",
            "Baki Bersih Di Tangan"
        ],
        text=[
            "+RM 62,824",
            "-RM 4,607",
            "-RM 4,027",
            "-RM 3,129",
            "-RM 2,738",
            "-RM 2,116",
            "RM 33,147"
        ],
        y=[62824.40, -4607.19, -4026.76, -3129.22, -2737.77, -2115.96, 33147.30],
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

    st.error("""
    💥 **HAKIKAT PAHIT YANG MENYAKITKAN:**  
    Jika anda mematuhi peraturan asas Stop Loss pada had maksimum **-RM 500** per dagangan, **RM 19,650.00** daripada wang yang hilang di atas akan kekal berada di dalam poket anda! Untung bersih anda hari ini sepatutnya **MELEPASI RM 52,800.00**!
    """)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 3. EMPAT TAB BEDAH SIASAT MENDALAM
    # ----------------------------------------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔴 1. Bedah Siasat 5 Tragedi Kebodohan Termahal",
        "🟢 2. Bedah Siasat 5 Kemenangan Kecerdikan Mutlak",
        "📦 3. Bedah Siasat Pegangan Aktif (UMC & GFM)",
        "📜 4. 5 Sumpah Keramat Disiplin DDNK"
    ])

    # ----------------------------------------------------------------------------------
    # TAB 1: 5 DOSA BESAR KEHILANGAN MODAL
    # ----------------------------------------------------------------------------------
    with tab1:
        st.subheader("🔴 5 Dosa Terbesar Yang Memusnahkan RM 15,616.90 Modal Anda")

        with st.expander("💀 TRAGEDI 1: Hecla Mining (NYSE:HL) — Rugi Terbesar Dalam Hidup (-RM 4,607.19 / -14.54%)", expanded=True):
            st.markdown("""
            - **Tarikh Transaksi:** 18-03-2026 | **Kuantiti:** 326 Unit
            - **Harga Beli:** $22.50 | **Stop Loss Dirancang:** $20.00 | **Harga Jual Sebenar:** **$19.2504**
            - **Punca Kebodohan Ekstrim:**  
              Pelan asal anda meletakkan Stop Loss pada **$20.00**. Tetapi apabila harga jatuh menyentuh $20.00, anda **TERKUNCI (FROZEN) & BERHARAP**. Anda membiarkan kerugian menjunam sehingga $19.25 baru panik menjual di lantai terendah!
            - **Dosa Psikologi:** **HOPE (Harapan Palsu).** Anda mengharapkan pasaran berpatah balik demi ego peribadi.
            - **Pengajaran Berdarah:** *Stop Loss bukan hiasan! Menolak kerugian kecil RM 1,500 mengundang bencana kerugian RM 4,600.*
            """)

        with st.expander("💀 TRAGEDI 2: Marathon Digital (NASDAQ:MARA) — Menang 6 Kali, Hancur Dalam 1 Hari (-RM 4,026.76 / -18.99%)", expanded=True):
            st.markdown("""
            - **Tarikh Bencana:** 01-11-2024 | **Kuantiti:** 251 Unit | **Harga Beli:** $19.88 | **Harga Jual:** $16.1331
            - **Kronologi Menyesakkan Dada:**
              - 18-10-2024: Untung +RM 161.52
              - 21-10-2024 (3 trade): Untung +RM 181.71
              - 22-10-2024: Untung +RM 80.52
              - 29-10-2024: Untung +RM 752.76
              - **Jumlah 6 kemenangan berturut-turut = +RM 1,176.51.**
            - **Punca Kebodohan Ekstrim:**  
              Ego anda melambung tinggi. Pada 1 November, anda masuk dengan saiz lot gergasi di puncak $19.88. Apabila harga jatuh, anda degil dan membiarkan posisi rugi hampir **-19.0%**!
            - **Dosa Psikologi:** **OVERCONFIDENCE & HUBRIS.** Satu dagangan cuai memadamkan seluruh hasil kerja keras berminggu-minggu dan merampas tambahan modal RM 2,850!
            """)

        with st.expander("💀 TRAGEDI 3 & 4: Trump Media (NASDAQ:DJT) — Mabuk FOMO & Revenge Trading (-RM 5,866.99)", expanded=True):
            st.markdown("""
            - **05-11-2024 (Trade 1):** Beli di pucuk $38.58 ➔ Panik jual $32.00 ➔ **Rugi -RM 3,129.22 (-17.20%)**
            - **07-11-2024 (Trade 2):** Masuk semula $36.50 ➔ Lebur ke $28.00 ➔ **Rugi -RM 2,737.77 (-23.74%)**
            - **Punca Kebodohan Ekstrim:**  
              1. **FOMO Melampau:** Beli pada hari mengundi Presiden AS kerana termakan berita hangat media massa.
              2. **Revenge Trading (Balas Dendam):** Bukannya bertenang selepas rugi RM 3.1k, anda masuk semula 2 hari kemudian dengan hati yang panas semata-mata mahu "balas dendam pada kaunter DJT".
            - **Dosa Psikologi:** **EGO & DENDAM.** Berdendam dengan pasaran adalah jalan pintas membakar akaun bank anda.
            """)

        with st.expander("💀 TRAGEDI 5: Scientex Berhad (KLSE:SCIENTX) — Anggapan Kebal Graviti (-RM 2,115.96 / -17.00%)", expanded=True):
            st.markdown("""
            - **Tarikh:** 24-03-2026 | **Kuantiti:** 3,000 Unit | **Beli:** RM 4.15 | **Jual:** RM 3.45
            - **Punca Kebodohan Ekstrim:**  
              Menyangka saham modal besar Bursa Malaysia tidak boleh jatuh teruk. Anda membiarkan sokongan demi sokongan bocor tanpa memasang Perintah Henti Otomatik (*Auto Stop Order*).
            - **Dosa Psikologi:** **COMPLACENCY (Sikap Mengabaikan Risiko).**
            """)

    # ----------------------------------------------------------------------------------
    # TAB 2: 5 KEMENANGAN KECERDIKAN BERDISIPLIN
    # ----------------------------------------------------------------------------------
    with tab2:
        st.subheader("🟢 5 Bukti Kecerdikan Ekstrim: Menjana +RM 22,230.15!")

        top_win_df = pd.DataFrame([
            {"No": 1, "Ticker": "HIMX (US)", "Tarikh": "10-08-2026", "Untung_MYR": "RM 9,498.22", "ROI": "+15.91%", "Kunci Kecerdikan": "Entri lantai Wyckoff $13.10, sabar biarkan untung berkembang ke $15.23."},
            {"No": 2, "Ticker": "NOK (US)", "Tarikh": "13-05-2026", "Untung_MYR": "RM 3,487.55", "ROI": "+3.45%", "Kunci Kecerdikan": "Saiz lot matematik sempurna (1,779 unit). Pergerakan kecil +3.4% menghasilkan ribuan ringgit!"},
            {"No": 3, "Ticker": "UMC (US)", "Tarikh": "31-08-2026", "Untung_MYR": "RM 3,293.03", "ROI": "+4.00%", "Kunci Kecerdikan": "Disiplin TP AND CLOSE: Jual tepat pada sasaran $21.07 tanpa tamak."},
            {"No": 4, "Ticker": "HIMX (US)", "Tarikh": "01-06-2026", "Untung_MYR": "RM 3,027.67", "ROI": "+5.45%", "Kunci Kecerdikan": "Entri Fasa D Wyckoff $20.80 bersama aliran Jerung Institusi (Smart Money)."},
            {"No": 5, "Ticker": "FRSH (US)", "Tarikh": "16-10-2026", "Untung_MYR": "RM 2,923.38", "ROI": "+4.60%", "Kunci Kecerdikan": "Eksekusi pantas tanpa ragu-ragu di zon asas sokongan $13.80."}
        ])
        st.dataframe(top_win_df, width="stretch", hide_index=True)

        st.success("""
        💎 **PELAJARAN EMAS:**  
        Anda tidak perlukan kenaikan 100% untuk menjadi kaya! Kaunter **NOK** hanya naik **+3.45%**, tetapi dengan saiz posisi matematik yang tepat, anda mengaut **RM 3,487.55 bersih** dalam beberapa hari!
        """)

    # ----------------------------------------------------------------------------------
    # TAB 3: BEDAH SIASAT TERBUKA PEGANGAN AKTIF
    # ----------------------------------------------------------------------------------
    with tab3:
        st.subheader("📦 Bedah Siasat Terbuka: Portfolio Yang Anda Pegang Hari Ini")

        c_u1, c_u2 = st.columns(2)

        with c_u1:
            st.markdown("""
            <div style="background:#161D2A; border:1px solid #2B384E; border-radius:12px; padding:20px;">
                <h3 style="color:#29B6F6; margin-top:0;">🇺🇸 NYSE:UMC (United Microelectronics)</h3>
                <p><b>Unit:</b> 581 | <b>Kos:</b> $19.260 | <b>Harga Live:</b> $18.650 | <b>P&L:</b> <span style="color:#FF5252;">-RM 1,444.79 (-3.2%)</span></p>
                <hr style="border-color:#2B384E;">
                <h4 style="color:#00E676;">🟢 Kenapa Cerdik?</h4>
                <p>Syarikat gergasi foundry cip semikonduktor nod matang dengan dividen sihat dan penilaian P/E rendah.</p>
                <h4 style="color:#FF5252;">🔴 Kenapa Bodoh & Menyedihkan?</h4>
                <p>Pada akhir Ogos 2026, UMC melonjak melepasi <b>$21.07</b>! Posisi anda ketika itu <b>SEDANG UNTUNG LEBIH RM 4,000 ATAS KERTAS!</b> Mengapa anda tidak memasang Trailing Stop untuk mengunci untung tersebut? Mengapa dibiarkan keuntungan ribuan ringgit terhakis sehingga bertukar menjadi <b>kerugian kertas -RM 1,444.79 hari ini</b>?</p>
                <div style="background:#2D151B; border-left:4px solid #FF5252; padding:10px; border-radius:4px;">
                    🛡️ <b>AMARAN KERAS:</b> Jangan biarkan UMC jadi mangsa HL kedua! Had lantai mutlak ialah <b>$18.00</b>. Jika pecah $18.00, potong tanpa ragu-ragu!
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_u2:
            st.markdown("""
            <div style="background:#161D2A; border:1px solid #2B384E; border-radius:12px; padding:20px;">
                <h3 style="color:#29B6F6; margin-top:0;">🇲🇾 KLSE:0039 (GFM Services Berhad)</h3>
                <p><b>Unit:</b> 56,400 | <b>Kos:</b> RM 0.175 | <b>Nilai Pasaran:</b> RM 9,870.00 | <b>P&L:</b> RM 0.00 (Pulang Modal)</p>
                <hr style="border-color:#2B384E;">
                <h4 style="color:#00E676;">🟢 Kenapa Cerdik?</h4>
                <p>Berjaya menurunkan kos purata daripada 0.215 kepada 0.175 melalui pembelian terancang. Syarikat ada konsesi fasiliti stabil.</p>
                <h4 style="color:#FF5252;">🔴 Kenapa Bodoh?</h4>
                <p><b>MODAL MATI (OPPORTUNITY COST)!</b> Wang anda sebanyak RM 9,870.00 terbeku berbulan-bulan tanpa bergerak, sedangkan dana tersebut boleh digunakan untuk menggandakan keuntungan dalam kaunter pemacu AI seperti TENAGA atau YTLPOWR.</p>
                <div style="background:#2D2515; border-left:4px solid #FFBB28; padding:10px; border-radius:4px;">
                    💡 <b>KEPUTUSAN STRATEGIK:</b> Letak had masa. Jika GFM gagal membuat lonjakan volum melepasi RM 0.190, cairkan modal dan pindahkan ke Meja Keputusan Harian!
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # TAB 4: 5 SUMPAH KERAMAT DISIPLIN DDNK
    # ----------------------------------------------------------------------------------
    with tab4:
        st.subheader("📜 5 Sumpah Keramat Pelabur Institusi Haddy Pro")
        st.caption("Lafazkan dan patuhi ikrar ini setiap kali sebelum menekan butang belian di broker Moomoo:")

        st.markdown("""
        1. 🛑 **AKU TIDAK AKAN SESEKALI MEMBELI KERANA BERITA ATAU FOMO.**  
           *Ingat tragedi DJT: Menunggang berita hangat adalah cara terpantas menaja kekayaan orang lain.*
        
        2. 🛡️ **AKU AKAN MENGHORMATI STOP LOSS SEPERTI MANA AKU MENGHORMATI MODALKU.**  
           *Rugi kecil 2% adalah kos perlindungan. Menolak rugi kecil adalah jemputan kepada kerugian ngeri 20% seperti HL dan MARA.*
        
        3. 🧘 **AKU TIDAK AKAN BERDENDAM DENGAN PASARAN (NO REVENGE TRADING).**  
           *Bila rugi, tutup skrin dan bertenang. Pasaran akan dibuka semula esok. Dendam hanya membawa kebankrapan.*
        
        4. 🔒 **AKU TIDAK AKAN MEMBIARKAN POSISI UNTUNG BESAR BERTUKAR MENJADI POSISI RUGI.**  
           *Ambil iktibar daripada UMC: Bila harga melepasi sasaran pertama, aktifkan Trailing Stop untuk mengunci modal.*
        
        5. 📐 **AKU PERCAYA KEPADA MATEMATIK SAIZ LOT, BUKAN PADA HARAPAN.**  
           *Kejayaan NOK dan HIMX membuktikan bahawa disiplin saiz posisi dan sabar di lantai Wyckoff adalah kunci sebenar membina kekayaan konsisten.*
        """)
