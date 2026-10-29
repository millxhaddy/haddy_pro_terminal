"""
HADDY PRO - TERMINAL MILLX
MODUL RASMI: PENGURUSAN HUTANG, LIABILITI & PROFIL KREDIT CCRIS/EXPERIAN (DATA SEBENAR)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_debt_management_dashboard(vault_data=None, stock_portfolio_val=54278.00):
    debts_data = [
        {"No": 1, "Kategori": "Pinjaman Perumahan", "Institusi": "Pembiayaan Bersama (BSN)", "Had Kredit": 388739.00, "Baki Semasa": 408048.18, "Tarikh Lulus": "18/07/2014", "Ansuran": 1400.00, "Cagaran": "Properties", "Kapasiti": "Joint", "Status": "DMP AKPK", "Kadar": "4.10%"},
        {"No": 2, "Kategori": "Sewa Beli Kenderaan", "Institusi": "Perodua Bezza 1.0 (Maybank)", "Had Kredit": 32900.00, "Baki Semasa": 13766.64, "Tarikh Lulus": "02/10/2021", "Ansuran": 396.00, "Cagaran": "Motor V", "Kapasiti": "Own", "Status": "Aktif", "Kadar": "6.69%"},
        {"No": 3, "Kategori": "Kad Kredit", "Institusi": "RHB Islamic (VS REWARDS CARD - i)", "Had Kredit": 19000.00, "Baki Semasa": 4682.05, "Tarikh Lulus": "17/06/2024", "Ansuran": 50.00, "Cagaran": "Clean", "Kapasiti": "Own", "Status": "DMP AKPK", "Kadar": "7.00%"},
        {"No": 4, "Kategori": "Kad Kredit", "Institusi": "RHB Islamic (VS CASH BACK CARD - i)", "Had Kredit": 19000.00, "Baki Semasa": 13638.26, "Tarikh Lulus": "07/02/2024", "Ansuran": 100.00, "Cagaran": "Clean", "Kapasiti": "Own", "Status": "DMP AKPK", "Kadar": "7.00%"},
        {"No": 5, "Kategori": "Pinjaman Peribadi", "Institusi": "Cash Plus (CIMB)", "Had Kredit": 100000.00, "Baki Semasa": 94013.13, "Tarikh Lulus": "19/02/2026", "Ansuran": 950.00, "Cagaran": "Clean", "Kapasiti": "Own", "Status": "DMP AKPK", "Kadar": "7.00%"},
        {"No": 6, "Kategori": "Sewa Beli Kenderaan", "Institusi": "Perodua Alza 1.5X (Hong Leong)", "Had Kredit": 63000.00, "Baki Semasa": 61123.74, "Tarikh Lulus": "26/06/2026", "Ansuran": 704.00, "Cagaran": "Motor V", "Kapasiti": "Own", "Status": "Aktif", "Kadar": "2.29%"}
    ]
    df_d = pd.DataFrame(debts_data)
    total_balance = df_d["Baki Semasa"].sum()
    total_monthly = df_d["Ansuran"].sum()

    st.markdown('''
    <style>
        .syariah-banner {
            background: linear-gradient(135deg, #06281E 0%, #03140F 100%);
            border: 2px solid #00E676;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 20px;
        }
        .metric-card-debt {
            background: linear-gradient(135deg, #1C2333 0%, #121722 100%);
            border: 1px solid #2B384E;
            border-radius: 10px;
            padding: 16px;
        }
    </style>
    ''', unsafe_allow_html=True)

    st.header("🏛️ Pengurusan Hutang, Liabiliti & Profil Kredit CCRIS BNM")
    st.caption("Penyegerakan Data Rasmi Google Sheets: 6 Fasiliti CCRIS, AKPK DMP & Experian i-SCORE (Setakat 26/10/2026)")

    # 1. PERINGATAN SYARIAH
    st.markdown('''
    <div class="syariah-banner">
        <h4 style="color:#00E676; margin:0 0 6px 0;">🕌 PERINGATAN SYARIAH: AMANAH PELUNASAN HUTANG & LARANGAN MUTLAK RIBA</h4>
        <p style="color:#A7F3D0; font-size:0.9rem; margin:4px 0;">
            <b>Surah Al-Baqarah (275):</b> <i>"Allah menghalalkan jual beli dan mengharamkan riba."</i> — Utamakan produk pembiayaan patuh syariah.
        </p>
        <p style="color:#E2E8F0; font-size:0.85rem; margin:4px 0;">
            <b>1. Amanah Melunaskan:</b> <i>"Jiwa seorang mukmin tergantung dengan hutangnya sehinggalah hutang itu dilunaskan."</i> (HR At-Tirmidhi)<br>
            <b>2. Niat & Bantuan Ilahi:</b> <i>"Barangsiapa meminjam harta orang dengan niat membayarnya, Allah akan menolong melunaskannya."</i> (HR Al-Bukhari)
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # 2. 4 KAD BENTO METRIK LIABILITI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card-debt" style="border-top:3px solid #FF5252;">
            <small style="color:#8E9AAF; font-weight:700;">JUMLAH BAKI LIABILITI</small>
            <h2 style="color:#FF5252; margin:4px 0;">RM {total_balance:,.2f}</h2>
            <small style="color:#A0AEC0;">DMP: RM 520,381.62 | Sewa Beli: RM 74,890.38</small>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card-debt" style="border-top:3px solid #FFBB28;">
            <small style="color:#8E9AAF; font-weight:700;">KOMITMEN BULANAN</small>
            <h2 style="color:#FFBB28; margin:4px 0;">RM {total_monthly:,.2f}</h2>
            <small style="color:#00E676;">Jimat DMP: +RM 2,163.29/bln (-46.4%)</small>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown('''
        <div class="metric-card-debt" style="border-top:3px solid #29B6F6;">
            <small style="color:#8E9AAF; font-weight:700;">TARIKH MATANG SETERUSNYA</small>
            <h2 style="color:#29B6F6; margin:4px 0;">29hb / 11hb</h2>
            <small style="color:#8E9AAF;">Alza: 29hb | Bezza: 11hb | DMP: 27hb</small>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
        <div class="metric-card-debt" style="border-top:3px solid #00E676;">
            <small style="color:#8E9AAF; font-weight:700;">STATUS SEWA BELI ALZA</small>
            <h2 style="color:#00E676; margin:4px 0;">4 / 108 Bulan</h2>
            <small style="color:#8E9AAF;">Baki Pokok: RM 61,123.74</small>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # 3. JADUAL CCRIS & CARTA PIE
    st.subheader("📋 Ringkasan 6 Fasiliti CCRIS Bank Negara Malaysia")
    c_tbl, c_pie = st.columns([7, 5])
    with c_tbl:
        st.dataframe(
            df_d.style.format({
                "Had Kredit": "RM {:,.2f}",
                "Baki Semasa": "RM {:,.2f}",
                "Ansuran": "RM {:,.2f}"
            }).map(
                lambda v: "color: #00E676; font-weight: bold;" if v == "Aktif" else "color: #29B6F6; font-weight: bold;",
                subset=["Status"]
            ),
            width="stretch",
            hide_index=True
        )
    with c_pie:
        fig_p = px.pie(
            df_d, names="Institusi", values="Ansuran", hole=0.45,
            color_discrete_sequence=["#FF5252", "#FFBB28", "#29B6F6", "#00E676", "#AB47BC", "#26A69A"]
        )
        fig_p.update_layout(template="plotly_dark", height=300, paper_bgcolor="#141824", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_p, width="stretch")

    st.markdown("---")

    # 4 & 5. EXPERIAN i-SCORE 558 & JAMBATAN UNTUNG SAHAM
    col_exp, col_brg = st.columns(2)
    with col_exp:
        st.subheader("🛡️ Profil Kredit Experian (i-SCORE 558) & DSR")
        fig_iscore = go.Figure(go.Indicator(
            mode="gauge+number", value=558,
            title={"text": "<b>Experian i-SCORE Semasa</b><br><span style='font-size:0.8rem;color:#FFBB28;'>Gred 5: SEDERHANA (FAIR) • PD 10%-20%</span>"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [300, 850], 'tickcolor': "#8E9AAF"},
                'bar': {'color': "#FFBB28", 'thickness': 0.3},
                'steps': [
                    {'range': [300, 550], 'color': "rgba(255, 82, 82, 0.35)"},
                    {'range': [550, 680], 'color': "rgba(255, 187, 40, 0.35)"},
                    {'range': [680, 850], 'color': "rgba(0, 230, 118, 0.35)"}
                ]
            }
        ))
        fig_iscore.update_layout(template="plotly_dark", height=260, paper_bgcolor="#141824", margin=dict(l=20, r=20, t=20, b=10))
        st.plotly_chart(fig_iscore, width="stretch")
        st.info("📊 **Metrik DSR Rasmi (11_Skor Kredit):** Gaji Bersih: **RM 7,500** | Komitmen: **RM 3,600** | DSR: **48.0% (SIHAT < 60%)** | Lebihan: **RM 3,900.00**")

    with col_brg:
        st.subheader("🌉 Jambatan Untung Saham ke Langsai Hutang")
        profit_flow = st.slider("Untung Saham Dialirkan ke Hutang (RM/Bulan):", 500.0, 5000.0, 1500.0, step=250.0)
        target_loan = st.selectbox("Pilih Fasiliti untuk Dilangsaikan Awal:", [
            "RHB Card-i Rewards (Baki RM 4,682.05 - Tamat Paling Pantas)",
            "Perodua Bezza (Baki RM 13,766.64 - Jimat Faedah 6.69%)",
            "RHB Card-i Cashback (Baki RM 13,638.26)",
            "Perodua Alza (Baki RM 61,123.74)",
            "CIMB Cash Plus (Baki RM 94,013.13)"
        ])
        
        bal = 4682.05 if "Rewards" in target_loan else (13766.64 if "Bezza" in target_loan else 94013.13)
        m_orig = 46 if "Rewards" in target_loan else (40 if "Bezza" in target_loan else 96)
        m_needed = int(bal / profit_flow) + 1
        m_saved = max(m_orig - m_needed, 0)
        
        st.markdown(f'''
        <div style="background:#0F291E; border:2px solid #00E676; border-radius:12px; padding:16px;">
            <h4 style="color:#00E676; margin:0 0 8px 0;">🚀 HASIL UNJURAN PELUNASAN PANTAS:</h4>
            <p><b>Tempoh Selesai:</b> <span style="font-size:1.3rem; color:#00E676; font-weight:bold;">{m_needed} Bulan Sahaja!</span> (Asal: {m_orig} Bulan)</p>
            <p><b>Masa Berjaya Dijimatkan:</b> <span style="color:#29B6F6; font-weight:bold;">{m_saved} Bulan ({m_saved/12:.1f} Tahun Lebih Awal!)</span></p>
            <p>Komitmen bulanan anda akan berkurang serta-merta selepas hutang ini tamat!</p>
        </div>
        ''', unsafe_allow_html=True)
