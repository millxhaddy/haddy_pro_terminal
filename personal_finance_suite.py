"""
HADDY PRO - TERMINAL MILLX
MODUL KEWANGAN PERIBADI, PERBANKAN, MIKRO-LIABILITI, KWSP & FIQH SYARIAH
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_banking_and_kwsp():
    st.subheader("🏦 Hab Perbankan, Simpanan Syariah & Dana Persaraan KWSP")
    st.caption("Penyatuan akaun simpanan Maybank Islamic, Tabung Haji, ASNB dan caruman persaraan KWSP Simpanan Shariah.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Maybank Islamic (Millx Bank)", "RM 18,500.00", "Simpanan Kecemasan (3.5 Bulan)")
    with c2:
        st.metric("Lembaga Tabung Haji", "RM 15,400.00", "Status: Cukup Daftar Haji")
    with c3:
        st.metric("Pelaburan ASNB", "RM 12,850.00", "Hasil Dividen: ~4.5% - 5.0%")
    with c4:
        st.metric("Jumlah Caruman KWSP", "RM 168,400.00", "100% Simpanan Shariah")

    st.markdown("---")
    col_k1, col_k2 = st.columns([5, 5])

    with col_k1:
        st.markdown("#### 🥧 Struktur Akaun KWSP (Format Baharu 3 Akaun):")
        kwsp_df = pd.DataFrame([
            {"Akaun": "Akaun 1 (Persaraan - 75%)", "Nilai (RM)": 126300.00, "Likuiditi": "Terkunci Umur 55"},
            {"Akaun": "Akaun 2 (Sejahtera - 15%)", "Nilai (RM)": 25260.00, "Likuiditi": "Pendidikan / Rumah"},
            {"Akaun": "Akaun 3 (Fleksibel - 10%)", "Nilai (RM)": 16840.00, "Likuiditi": "Bila-bila Masa"}
        ])
        fig_kwsp = px.pie(
            kwsp_df, names="Akaun", values="Nilai (RM)", hole=0.45,
            color_discrete_sequence=["#00E676", "#29B6F6", "#FFBB28"]
        )
        fig_kwsp.update_layout(template="plotly_dark", height=280, paper_bgcolor="#141824", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_kwsp, width="stretch")

    with col_k2:
        st.markdown("#### 🛡️ Skim Pelaburan Ahli (IPD untuk Pasaran Saham):")
        st.markdown("""
        <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
            <p><b>Kelayakan Pengeluaran IPD Saham:</b> Dibenarkan melaburkan sebahagian lebihan Akaun Persaraan ke dalam dana unit amanah / mandat saham patuh syariah yang diluluskan KWSP.</p>
            <p><b>Anggaran Kelayakan Semasa:</b> <span style="color:#00E676; font-weight:bold;">RM 18,500.00</span></p>
            <hr style="border-color:#2B384E;">
            <p style="font-size:0.85rem; color:#8E9AAF;">Dividen KWSP Simpanan Shariah diunjurkan sekitar 5.3% - 5.6% setahun, memberi perlindungan inflasi jangka panjang.</p>
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
            z_bank = st.number_input("Baki Terendah Simpanan Bank Setahun (MYR):", value=15000.00, step=1000.00)
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