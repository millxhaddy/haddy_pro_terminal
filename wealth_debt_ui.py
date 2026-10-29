"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL PAPAN KAWALAN KEWANGAN HOLISTIK & LIABILITI (WEALTH & DEBT UI)
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wealth_debt_engine import get_holistic_balance_sheet, get_syariah_reminders

def render_wealth_debt_dashboard(stock_portfolio_val=55945.32, cash_reserve=18500.00):
    data = get_holistic_balance_sheet(stock_portfolio_val, cash_reserve)
    
    st.markdown("""
    <style>
        .syariah-card {
            background: linear-gradient(135deg, #09261E 0%, #05140F 100%);
            border: 2px solid #00E676;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 230, 118, 0.2);
        }
        .debt-card-red {
            background: linear-gradient(135deg, #331018 0%, #1A080C 100%);
            border: 1px solid #FF5252;
            border-radius: 12px;
            padding: 16px;
        }
        .asset-card-green {
            background: linear-gradient(135deg, #0D2B20 0%, #061811 100%);
            border: 1px solid #00E676;
            border-radius: 12px;
            padding: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🏛️ Pengurusan Kewangan Holistik & Liabiliti (Penyata Imbangan Sebenar)")
    st.caption("Pusat Penyatuan Nilai Bersih, Profil Kredit CCRIS/Experian, AKPK DMP, Pinjaman Kenderaan, Simpanan & Pasaran Saham")

    # ----------------------------------------------------------------------------------
    # 1. PERINGATAN SYARIAH MUTLAK (PERISAI ROHANI)
    # ----------------------------------------------------------------------------------
    reminders = get_syariah_reminders()
    with st.expander("🕌 PERINGATAN SYARIAH: AMANAH PELUNASAN HUTANG & LARANGAN RIBA (KLIK UNTUK BACA)", expanded=True):
        st.markdown(f"""
        <div class="syariah-card">
            <h4 style="color:#00E676; margin:0 0 6px 0;">📖 {reminders[0]['Surah_Hadis']}</h4>
            <h3 style="color:#FFFFFF; margin:0 0 8px 0;">"{reminders[0]['Maksud']}"</h3>
            <p style="color:#A7F3D0; font-size:0.92rem; margin:0;"><b>Panduan:</b> {reminders[0]['Tafsiran']}</p>
            <hr style="border-color:#1F4D3E; margin:10px 0;">
            <p style="color:#E2E8F0; font-size:0.88rem; margin:0;">
                💡 <i>"Jiwa seorang mukmin tergantung dengan hutangnya sehinggalah hutang itu dilunaskan."</i> (HR At-Tirmidhi)
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # 2. PAPAN SKOR BENTO NILAI BERSIH (NET WORTH BENTO-BOX)
    # ----------------------------------------------------------------------------------
    col_w1, col_w2, col_w3, col_w4 = st.columns(4)

    with col_w1:
        st.markdown(f"""
        <div class="asset-card-green">
            <small style="color:#A7F3D0; font-weight:700;">💎 JUMLAH KESELURUHAN ASET</small>
            <h2 style="color:#00E676; margin:4px 0;">RM {data['total_assets']:,.2f}</h2>
            <small style="color:#8E9AAF;">Hartanah, Saham, Tunai & KWSP</small>
        </div>
        """, unsafe_allow_html=True)

    with col_w2:
        st.markdown(f"""
        <div class="debt-card-red">
            <small style="color:#FECDD3; font-weight:700;">📉 JUMLAH BAKI LIABILITI</small>
            <h2 style="color:#FF5252; margin:4px 0;">RM {data['total_liabilities']:,.2f}</h2>
            <small style="color:#FFA4B2;">7 Fasiliti (4 DMP + 3 Aktif)</small>
        </div>
        """, unsafe_allow_html=True)

    with col_w3:
        nw_color = "#29B6F6" if data["net_worth"] >= 0 else "#FF5252"
        st.markdown(f"""
        <div style="background:#171E2D; border:1px solid #2B384E; border-radius:12px; padding:16px;">
            <small style="color:#8E9AAF; font-weight:700;">⚖️ NILAI BERSIH SEBENAR (NET WORTH)</small>
            <h2 style="color:{nw_color}; margin:4px 0;">RM {data['net_worth']:,.2f}</h2>
            <small style="color:#00E676;">Nisbah Solvensi: {data['solvency_ratio']:.2f}x Aset</small>
        </div>
        """, unsafe_allow_html=True)

    with col_w4:
        st.markdown(f"""
        <div style="background:#171E2D; border:1px solid #2B384E; border-radius:12px; padding:16px;">
            <small style="color:#8E9AAF; font-weight:700;">💳 KOMITMEN BULANAN</small>
            <h2 style="color:#FFBB28; margin:4px 0;">RM {data['total_monthly_commitment']:,.2f}</h2>
            <small style="color:#00E676;">Jimat DMP: +RM {data['dmp_monthly_savings']:,.2f}/bln</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 3. TAB STRUKTUR TERPERINCI
    # ----------------------------------------------------------------------------------
    tab_debts, tab_experian, tab_akpk, tab_bridge = st.tabs([
        "📋 1. Lejar 7 Fasiliti Hutang (CCRIS)",
        "🛡️ 2. Profil Kredit Experian & i-SCORE",
        "🤝 3. Program AKPK DMP & Sewa Beli",
        "🌉 4. Jambatan Untung Saham ke Hutang"
    ])

    with tab_debts:
        st.subheader("📋 Ringkasan Liabiliti Portfolio (Rekod CCRIS Bank Negara Malaysia)")
        df_l = data["df_liabilities"]

        c_t1, c_t2 = st.columns([7, 5])
        with c_t1:
            st.dataframe(
                df_l.style.format({
                    "Baki_Semasa": "RM {:,.2f}",
                    "Had_Asal": "RM {:,.2f}",
                    "Ansuran_Bulanan": "RM {:,.2f}"
                }).map(lambda v: "color: #00E676; font-weight: bold;" if v == "Aktif" else "color: #29B6F6; font-weight: bold;", subset=["Status"]),
                width="stretch",
                hide_index=True
            )

        with c_t2:
            st.markdown("#### 🥧 Pecahan Komitmen Ansuran Bulanan")
            fig_pie_debt = px.pie(
                df_l,
                names="Fasiliti",
                values="Ansuran_Bulanan",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            fig_pie_debt.update_layout(
                template="plotly_dark", height=320,
                paper_bgcolor="#141824", plot_bgcolor="#141824",
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_pie_debt, width="stretch")

    with tab_experian:
        st.subheader("🛡️ Profil Kredit Experian (i-SCORE) & Penarafan Kesihatan")

        exp_c1, exp_c2 = st.columns(2)
        with exp_c1:
            # Tolok Skor Kredit Experian
            fig_score = go.Figure(go.Indicator(
                mode="gauge+number",
                value=688,
                title={"text": "<b>Experian i-SCORE Semasa</b><br><span style='font-size:0.8rem;color:#00E676;'>Gred Kredibiliti Kewangan: BAIK</span>"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [300, 850], 'tickcolor': "#8E9AAF"},
                    'bar': {'color': "#00E676"},
                    'steps': [
                        {'range': [300, 550], 'color': "rgba(255, 82, 82, 0.3)"},
                        {'range': [550, 680], 'color': "rgba(255, 187, 40, 0.3)"},
                        {'range': [680, 850], 'color': "rgba(0, 230, 118, 0.3)"}
                    ],
                    'threshold': {'line': {'color': "#29B6F6", 'width': 4}, 'thickness': 0.8, 'value': 700}
                }
            ))
            fig_score.update_layout(template="plotly_dark", height=280, paper_bgcolor="#141824", plot_bgcolor="#141824", margin=dict(l=20, r=20, t=30, b=10))
            st.plotly_chart(fig_score, width="stretch")

        with exp_c2:
            st.markdown("""
            <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
                <h4 style="color:#29B6F6; margin-top:0;">📊 Analisis Laporan CCRIS & Kebarangkalian Ingkar:</h4>
                <ul>
                    <li><b>Rekod Tunggakan Semasa:</b> <span style="color:#00E676; font-weight:bold;">0 Bulan (Bersih / On-Track)</span></li>
                    <li><b>Status Program AKPK (DMP):</b> 4 Akaun Berjadual (Dibayar tepat 27hb setiap bulan).</li>
                    <li><b>Kebarangkalian Ingkar (Default Risk):</b> <b>Rendah (1.2%)</b> dengan pematuhan ansuran DMP.</li>
                    <li><b>Kapasiti Pinjaman Bersama:</b> Pinjaman Perumahan BSN (RM 408k) berkongsi liabiliti bersama pasangan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_akpk:
        st.subheader("🤝 Program Pengurusan Kredit (AKPK DMP) & Perjanjian Sewa Beli")
        
        akpk_col1, akpk_col2 = st.columns(2)
        with akpk_col1:
            st.markdown("""
            <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
                <h4 style="color:#00E676; margin-top:0;">🏛️ Butiran Berjadual AKPK DMP:</h4>
                <p><b>Jumlah Bayaran Bulanan:</b> RM 2,500.00 (Selesai Ref: 9907505053)</p>
                <p><b>Kadar Faedah Konsesi:</b> 7.00% (RHB & CIMB) & 4.10% (BSN)</p>
                <p><b>Penjimatan Tunai Bulanan:</b> <span style="color:#00E676; font-weight:bold;">+RM 981.00 sebulan</span></p>
                <p><b>Status Pematuhan:</b> 100% Berdisiplin (Tiada rekod lewat bayar)</p>
            </div>
            """, unsafe_allow_html=True)

        with akpk_col2:
            st.markdown("""
            <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
                <h4 style="color:#29B6F6; margin-top:0;">🚗 Status Sewa Beli Kenderaan:</h4>
                <p><b>Perodua Alza 1.5X:</b> RM 704.00/bulan (Bulan 4 / 108 Bulan | Baki RM 61,123.74)</p>
                <p><b>Perodua Bezza 1.0:</b> RM 396.00/bulan (Baki 40 Bulan | Baki RM 13,766.64)</p>
                <p><b>Status Syariah:</b> 100% Patuh Syariah (AITAB)</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_bridge:
        st.subheader("🌉 Jambatan Keuntungan Saham ke Pelunasan Liabiliti")
        st.caption("Gunakan dividen dan keuntungan modal pasaran saham untuk mempercepatkan pelunasan hutang pokok.")

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.markdown("#### ⚡ Simulasi Pelunasan Pantas Menggunakan Keuntungan Saham:")
            stock_profit_monthly = st.slider("Untung Purata Dagangan Saham Bersih (MYR/Bulan):", 500.0, 5000.0, 1500.0, step=250.0)
            target_debt = st.selectbox("Pilih Liabiliti Sasaran untuk Dilangsaikan Awal:", [
                "Perodua Bezza (Baki RM 13,766.64 - Tamat Cepat)",
                "PTPTN (Baki RM 18,450.00 - Bebaskan Nama)",
                "RHB Card-i 1 (Baki RM 4,682.05 - Hapuskan Segera)",
                "CIMB Cash Plus (Baki RM 94,013.13)"
            ])

        with b_c2:
            if "Bezza" in target_debt:
                target_bal = 13766.64
                orig_months = 40
            elif "RHB" in target_debt:
                target_bal = 4682.05
                orig_months = 46
            elif "PTPTN" in target_debt:
                target_bal = 18450.00
                orig_months = 120
            else:
                target_bal = 94013.13
                orig_months = 96

            months_to_clear = int(target_bal / stock_profit_monthly) + 1
            months_saved = max(orig_months - months_to_clear, 0)

            st.markdown(f"""
            <div style="background:#0F291E; border:2px solid #00E676; border-radius:12px; padding:18px;">
                <h4 style="color:#00E676; margin-top:0;">🚀 KEPUTUSAN PELUNASAN PANTAS:</h4>
                <p><b>Tempoh Masa Selesai:</b> <span style="font-size:1.3rem; color:#00E676; font-weight:bold;">{months_to_clear} Bulan Sahaja!</span> (Asal: {orig_months} Bulan)</p>
                <p><b>Masa Berjaya Dijimatkan:</b> <span style="color:#29B6F6; font-weight:bold;">{months_saved} Bulan ({months_saved/12:.1f} Tahun) Lebih Awal!</span></p>
                <p><b>Beban Ansuran Terhapus:</b> Tunai anda bertambah bebas setiap bulan selepas hutang ini tamat!</p>
            </div>
            """, unsafe_allow_html=True)
