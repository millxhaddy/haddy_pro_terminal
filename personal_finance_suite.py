"""
HADDY PRO - TERMINAL MILLX
MODUL KEWANGAN PERIBADI, PERBANKAN, MIKRO-LIABILITI, KWSP & FIQH SYARIAH (DATA SEBENAR)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_banking_and_kwsp():
    st.subheader("🏦 Hab Perbankan, Simpanan Syariah & Dana Persaraan KWSP")
    st.caption("Penyatuan akaun simpanan Maybank Islamic, Tabung Haji, ASNB dan caruman persaraan KWSP Simpanan Shariah (Data Rasmi 26/10/2026).")

    # 4 KAD SKOR SEBENAR DARI GOOGLE SHEETS
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Maybank Islamic (Savers-i)", "RM 4.24", "Baki Penyata Terkini")
    with c2:
        st.metric("Lembaga Tabung Haji", "RM 44.84", "Tabung Am (T1)")
    with c3:
        st.metric("Pelaburan ASNB", "RM 549.07", "523.21 Unit (7 Tabung Aktif)")
    with c4:
        st.metric("Jumlah Simpanan KWSP", "RM 251,831.78", "100% Simpanan Shariah")

    st.markdown("---")
    col_k1, col_k2 = st.columns([5, 5])

    with col_k1:
        st.markdown("#### 🥧 Struktur Sebenar Akaun KWSP (Setakat 26/10/2026):")
        kwsp_df = pd.DataFrame([
            {"Akaun": "Akaun Persaraan (Akaun 1 - 92.1%)", "Nilai (RM)": 231894.61, "Peratus": "92.08%", "Status": "Terkunci Umur 55"},
            {"Akaun": "Akaun Sejahtera (Akaun 2 - 6.8%)", "Nilai (RM)": 17070.27, "Peratus": "6.78%", "Status": "Pra-Persaraan Khas"},
            {"Akaun": "Akaun Fleksibel (Akaun 3 - 1.1%)", "Nilai (RM)": 2866.90, "Peratus": "1.14%", "Status": "Pengeluaran Bila-bila Masa"}
        ])
        fig_kwsp = px.pie(
            kwsp_df, names="Akaun", values="Nilai (RM)", hole=0.45,
            color_discrete_sequence=["#00E676", "#29B6F6", "#FFBB28"]
        )
        fig_kwsp.update_layout(template="plotly_dark", height=280, paper_bgcolor="#141824", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_kwsp, width="stretch")

    with col_k2:
        st.markdown("#### 🛡️ Audit Aliran Dana KWSP & Simpanan Tunai:")
        st.markdown("""
        <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
            <p><b>Jumlah Simpanan KWSP Semasa:</b> <span style="color:#00E676; font-weight:bold; font-size:1.1rem;">RM 251,831.78</span></p>
            <ul>
                <li><b>Caruman Tahunan 2026 (YTD):</b> +RM 22,412.00</li>
                <li><b>Pemulihan Modal SPA Kenanga (01/08/2026):</b> +RM 32,969.10</li>
                <li><b>Pengeluaran Terdahulu (2025):</b> -RM 34,798.00</li>
            </ul>
            <hr style="border-color:#2B384E;">
            <p style="font-size:0.85rem; color:#8E9AAF;">
                💡 <b>Kecairan Boleh Keluar Segera:</b> Akaun 3 Fleksibel mempunyai baki <b>RM 2,866.90</b>. Baki selebihnya dilindungi di bawah mandat persaraan.
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_micro_liabilities():
    st.subheader("💳 Lejar Mikro-Liabiliti, PTPTN & Penyelenggaraan Kediaman")
    st.caption("Penjejakan transaksi kad kredit RHB, lejar pembiayaan peribadi CIMB, ansuran PTPTN dan yuran Castana.")

    t_rhb, t_cimb, t_ptptn, t_castana = st.tabs([
        "💳 Kad Kredit RHB (Shared Limit)",
        "💰 Pinjaman Peribadi CIMB",
        "🎓 Pinjaman Pendidikan PTPTN",
        "🏡 Penyelenggaraan Castana"
    ])

    with t_rhb:
        st.markdown("#### 💳 Audit Kad Kredit RHB Islamic (VS Rewards & Cashback):")
        st.markdown("""
        - **Had Kredit Berkongsi (Shared Limit):** RM 19,000.00
        - **Baki Kad 1 (Rewards - i):** RM 4,682.05 (Ansuran DMP: RM 50.00/bulan)
        - **Baki Kad 2 (Cash Back - i):** RM 13,638.26 (Ansuran DMP: RM 100.00/bulan)
        - **Jumlah Penggunaan Had:** **RM 18,320.31 (96.4% daripada had)**
        - **Kadar Konsesi DMP:** 7.00% setahun (Pencegahan kompaun faedah riba 18% kad kredit biasa).
        """)

    with t_cimb:
        st.markdown("#### 💰 Pinjaman Peribadi CIMB Cash Plus (Ref: DMP AKPK):")
        st.markdown("""
        - **Jumlah Pembiayaan Asal:** RM 100,000.00
        - **Baki Diisytiharkan Terkini:** **RM 94,013.13**
        - **Ansuran Bulanan Berjadual:** RM 950.00 sebulan
        - **Kadar Keuntungan Konsesi:** 7.00% p.a.
        - **Status Bayaran:** Diselesaikan berpusat melalui bayaran konsortium AKPK RM 2,500 pada 27hb setiap bulan.
        """)

    with t_ptptn:
        st.markdown("#### 🎓 Pinjaman Pendidikan PTPTN (Ujrah 1%):")
        st.markdown("""
        - **Jumlah Pinjaman Asal:** RM 25,000.00
        - **Baki Semasa:** **RM 18,450.00**
        - **Ansuran Bulanan:** RM 150.00 / bulan (Auto-debit / Potongan Gaji)
        - **Upah Pengurusan (Ujrah):** 1.00% setahun (Patuh Syariah)
        - **Perlindungan Takaful:** Aktif (Penyelesaian penuh jika berlaku kematian/keilatan kekal).
        - **Sekatan Perjalanan Imigresen:** Bersih / Tiada Senarai Hitam.
        """)

    with t_castana:
        st.markdown("#### 🏡 Penyelenggaraan Kediaman Castana & Sinking Fund:")
        st.markdown("""
        - **Yuran Pengurusan Bulanan:** RM 120.00 / bulan
        - **Kumpulan Wang Penjelas (Sinking Fund):** RM 12.00 / bulan
        - **Status Invois:** Terkini / Tiada Tunggakan
        - **Liputan Perkhidmatan:** Keselamatan komuniti 24-jam, pembersihan kawasan bersama dan penyelenggaraan landskap.
        """)

def render_fiqh_and_zakat(net_equity=55945.32):
    st.subheader("🕌 Fiqh Kewangan Islam, Hadis Tematik & Taksiran Zakat Menyeluruh")
    st.caption("Penyucian harta dan panduan pengurusan rezeki mengikut Al-Quran dan Sunnah.")

    f_zakat, f_hadis = st.tabs([
        "🌙 Taksiran Zakat Bersepadu 3-dalam-1",
        "📖 Himpunan Hadis Sahih Kewangan & Hutang"
    ])

    with f_zakat:
        st.markdown("#### 🌙 Kiraan Zakat Pendapatan, Simpanan Bank & Saham:")
        c_z1, c_z2 = st.columns(2)
        with c_z1:
            z_inc = st.number_input("Pendapatan Tahunan Bersih (MYR):", value=60000.00, step=5000.00)
            z_bank = st.number_input("Baki Terendah Simpanan Bank Setahun (MYR):", value=598.15, step=50.0, help="Maybank (RM4.24) + TH (RM44.84) + ASNB (RM549.07)")
            z_stocks = st.number_input("Nilai Pasaran Saham Aktif Urus Niaga (MYR):", value=float(net_equity), step=1000.00)
            gold_rate = 385.50
            nisab_val = 85.0 * gold_rate

        with c_z2:
            total_zakatable = z_inc + z_bank + z_stocks
            zakat_total_pay = total_zakatable * 0.025 if total_zakatable >= nisab_val else 0.0

            st.markdown(f"""
            <div style="background:#0F291E; border:2px solid #00E676; border-radius:12px; padding:18px;">
                <h4 style="color:#00E676; margin-top:0;">📋 KEPUTUSAN TAKSIRAN ZAKAT KESELURUHAN:</h4>
                <p><b>Nilai Nisab Semasa (85g Emas):</b> RM {nisab_val:,.2f}</p>
                <p><b>Jumlah Harta Layak Zakat:</b> RM {total_zakatable:,.2f}</p>
                <hr style="border-color:#1E4E3E;">
                <h2 style="color:#00E676; margin:4px 0;">RM {zakat_total_pay:,.2f}</h2>
                <small style="color:#A7F3D0;">Kadar Wajib: 2.5% ke atas jumlah harta genap haul & nisab.</small>
            </div>
            """, unsafe_allow_html=True)

    with f_hadis:
        st.markdown("#### 📖 Peringatan Hadis Sahih Pengurusan Wang & Tanggungjawab:")
        st.markdown("""
        1. **Keberkatan Jual Beli Yang Jujur:**  
           *"Peniaga yang jujur dan amanah akan bersama-sama para nabi, orang-orang yang benar (shiddiqin) dan para syuhada."* (HR At-Tirmidhi)
        
        2. **Bahaya Menangguhkan Bayaran Hutang Ketika Mampu:**  
           *"Menangguh-nangguhkan pembayaran hutang oleh orang yang mampu adalah satu kezaliman."* (HR Al-Bukhari & Muslim)
        
        3. **Rezeki Yang Berkat Adalah Yang Mengalir Manfaat:**  
           *"Harta tidak akan berkurang kerana sedekah, dan Allah tidak menambah kepada seseorang hamba yang memberi kemaafan melainkan kemuliaan."* (HR Muslim)
        
        4. **Doa Bebas Belenggu Hutang:**  
           *Allahumma inni a'udzu bika minal ma'tsami wal maghram (Ya Allah, aku berlindung kepada-Mu daripada perbuatan dosa dan belenggu hutang).* (HR Al-Bukhari)
        """)

def render_personal_finance_suite(vault_data=None, net_equity=55945.32):
    t1, t2, t3 = st.tabs([
        "🏦 1. Perbankan & KWSP",
        "💳 2. Mikro-Liabiliti & PTPTN",
        "🕌 3. Fiqh Syariah & Zakat Menyeluruh"
    ])
    with t1:
        render_banking_and_kwsp()
    with t2:
        render_micro_liabilities()
    with t3:
        render_fiqh_and_zakat(net_equity=net_equity)