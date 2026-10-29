"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL 1: ZAKAT SAHAM & AUDIT KEKAYAAN PATUH SYARIAH (ISLAMIC WEALTH COMPLIANCE)
Kaedah Taksiran Urus Niaga Saham (2.5% atas Nilai Ekuiti Bersih)
========================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def calculate_stock_zakat(
    active_portfolio_val: float = 55945.32,
    cash_buffer: float = 18500.00,
    short_term_liabilities: float = 0.00,
    gold_price_per_gram: float = 385.50
) -> dict:
    """
    Kiraan Zakat Saham mengikut piawaian Pusat Pungutan Zakat (PPZ) & Mazhab Syafi'i.
    Kaedah Pelaburan/Perdagangan Aktif (Trade for Capital Gain):
    Zakat = 2.5% x (Nilai Pasaran Saham Aktif + Tunai Bersih - Liabiliti Jangka Pendek)
    """
    total_assets = active_portfolio_val + cash_buffer
    net_zakatable_wealth = max(total_assets - short_term_liabilities, 0.0)
    
    # Nilai Nisab (85 gram Emas)
    nisab_value = 85.0 * gold_price_per_gram
    is_nisab_reached = net_zakatable_wealth >= nisab_value
    
    zakat_rate = 0.025
    zakat_payable = (net_zakatable_wealth * zakat_rate) if is_nisab_reached else 0.0

    return {
        "active_portfolio_val": active_portfolio_val,
        "cash_buffer": cash_buffer,
        "total_assets": total_assets,
        "short_term_liabilities": short_term_liabilities,
        "net_zakatable_wealth": net_zakatable_wealth,
        "gold_price_per_gram": gold_price_per_gram,
        "nisab_value": nisab_value,
        "is_nisab_reached": is_nisab_reached,
        "zakat_rate_pct": 2.5,
        "zakat_payable": zakat_payable
    }

def render_zakat_compliance_ui(net_equity: float = 55945.32):
    st.markdown("""
    <style>
        .zakat-card {
            background: linear-gradient(135deg, #0D281E 0%, #061811 100%);
            border: 2px solid #00E676;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 18px rgba(0, 230, 118, 0.2);
            margin-bottom: 20px;
        }
        .nisab-box {
            background-color: #171E2D;
            border-left: 4px solid #FFD700;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🌙 Modul Zakat Saham & Penyata Kekayaan Patuh Syariah")
    st.caption("Penyucian Keuntungan & Pemerkasaan Harta Berdasarkan Kaedah Urus Niaga Saham (PPZ & Majlis Agama Islam).")

    col_z1, col_z2 = st.columns([5, 5])

    with col_z1:
        st.subheader("⚙️ Parameter Taksiran Harta Saham")
        with st.form("zakat_calculator_form"):
            z_port = st.number_input("Nilai Pasaran Saham Aktif (MYR):", value=float(net_equity), step=1000.0, format="%.2f")
            z_cash = st.number_input("Baki Tunai Tersedia / Dividen Simpanan (MYR):", value=18500.00, step=1000.0, format="%.2f")
            z_debt = st.number_input("Tolak: Liabiliti / Hutang Margin Jangka Pendek (MYR):", value=0.00, step=500.0, format="%.2f")
            z_gold = st.number_input("Harga Pasaran 1 Gram Emas Semasa (MYR):", value=385.50, step=5.0, format="%.2f", help="Kadar Semasa Pusat Pungutan Zakat (Nilai 85g Emas).")
            
            calc_submit = st.form_submit_button("🌙 Kira Zakat Semula", width="stretch")

    res = calculate_stock_zakat(
        active_portfolio_val=z_port,
        cash_buffer=z_cash,
        short_term_liabilities=z_debt,
        gold_price_per_gram=z_gold
    )

    with col_z2:
        st.subheader("📋 Keputusan Taksiran Kewajipan Zakat")
        
        if res["is_nisab_reached"]:
            st.markdown(f"""
            <div class="zakat-card">
                <small style="color:#A7F3D0; font-weight:700;">🟢 STATUS: WAJIB ZAKAT (MELEPASI NISAB)</small>
                <h1 style="color:#00E676; margin:8px 0;">RM {res['zakat_payable']:,.2f}</h1>
                <p style="color:#E2E8F0; margin:0; font-size:0.92rem;">
                    Kadar Wajib: <b>2.5%</b> ke atas Harta Boleh Zakat (RM {res['net_zakatable_wealth']:,.2f}).
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#222B3D; border:2px solid #8E9AAF; border-radius:14px; padding:22px;">
                <small style="color:#CBD5E1; font-weight:700;">🟡 STATUS: BELUM CUKUP NISAB</small>
                <h1 style="color:#FFFFFF; margin:8px 0;">RM 0.00</h1>
                <p style="color:#94A3B8; margin:0;">Jumlah harta belum mencecah paras nisab minima.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nisab-box">
            🥇 <b>Paras Nisab Semasa (85g Emas):</b> RM {res['nisab_value']:,.2f} (85g x RM {res['gold_price_per_gram']:.2f}/g)<br>
            💼 <b>Jumlah Harta Boleh Zakat:</b> RM {res['net_zakatable_wealth']:,.2f} ({(res['net_zakatable_wealth']/res['nisab_value']*100):.1f}% Nisab)<br>
            ⏳ <b>Tempoh Haul:</b> 1 Tahun Qamariah (354 Hari) bermula dari tarikh genap nisab.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📜 Penyata Ringkas Zakat Saham Sedia Rujukan")
    z_table_data = [
        {"Keterangan": "Nilai Pasaran Saham Tempatan & Global (GFM, UMC)", "Nilai (MYR)": f"RM {res['active_portfolio_val']:,.2f}"},
        {"Keterangan": "Baki Tunai & Rizab Akaun Broker", "Nilai (MYR)": f"RM {res['cash_buffer']:,.2f}"},
        {"Keterangan": "Tolak: Liabiliti / Kos Margin Jangka Pendek", "Nilai (MYR)": f"-RM {res['short_term_liabilities']:,.2f}"},
        {"Keterangan": "Jumlah Harta Yang Dikenakan Zakat", "Nilai (MYR)": f"RM {res['net_zakatable_wealth']:,.2f}"},
        {"Keterangan": "Kadar Zakat (Kaedah Urus Niaga)", "Nilai (MYR)": "2.5%"},
        {"Keterangan": "JUMLAH ZAKAT PERLU DIBAYAR", "Nilai (MYR)": f"RM {res['zakat_payable']:,.2f}"}
    ]
    st.dataframe(pd.DataFrame(z_table_data), width="stretch", hide_index=True)
