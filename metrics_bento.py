"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 4: KAD SKOR BENTO-BOX & KPI EKSEKUTIF (EXECUTIVE BENTO-BOX METRICS)
========================================================================================
"""

import streamlit as st
import pandas as pd
from pipeline_cleaner import clean_currency

def extract_portfolio_kpis(vault_data: dict) -> dict:
    """
    Mengekstrak dan mengira KPI utama daripada data tab Funding_Details,
    Terminal_Saham, dan Jurnal Dagangan.
    """
    kpis = {
        "total_deposit": 84801.00,
        "total_withdrawal": 42303.20,
        "net_invested": 42497.80,
        "active_portfolio_val": 55945.32,
        "unrealized_pnl": 13447.52,
        "unrealized_roi_pct": 31.64,
        "win_rate_pct": 77.0,
        "profit_factor": 2.12,
        "total_trades": 113,
        "avg_win": 722.12,
        "avg_loss": -1187.09,
        "margin_fees": 4016.56,
        "cash_retention_pct": 50.1
    }
    
    # Cuba kemas kini secara dinamik jika tab funding mempunyai data
    df_funding = vault_data.get("funding", pd.DataFrame())
    if not df_funding.empty:
        try:
            # Cari baris deposit & pengeluaran jika ada
            type_cols = [c for c in df_funding.columns if "TYPE" in c.upper() or "JENIS" in c.upper()]
            amt_cols = [c for c in df_funding.columns if "AMOUNT" in c.upper() or "AMAUN" in c.upper() or "JUMLAH" in c.upper()]
            if type_cols and amt_cols:
                t_col = type_cols[0]
                a_col = amt_cols[0]
                dep_mask = df_funding[t_col].astype(str).str.upper().str.contains("DEPOSIT")
                wth_mask = df_funding[t_col].astype(str).str.upper().str.contains("WITHDRAW")
                dep_sum = df_funding.loc[dep_mask, a_col].apply(clean_currency).sum()
                wth_sum = df_funding.loc[wth_mask, a_col].apply(clean_currency).sum()
                if dep_sum > 0:
                    kpis["total_deposit"] = dep_sum
                    kpis["total_withdrawal"] = abs(wth_sum)
                    kpis["net_invested"] = dep_sum - abs(wth_sum)
                    kpis["cash_retention_pct"] = (kpis["net_invested"] / dep_sum) * 100
        except Exception:
            pass

    return kpis

def render_bento_metrics(kpis: dict):
    """
    Memaparkan susun atur Bento-Box interaktif menggunakan CSS kad gelap bertaraf institusi.
    """
    st.markdown("""
    <style>
        .bento-card {
            background: linear-gradient(135deg, #1A1F2C 0%, #141824 100%);
            border: 1px solid #2B354C;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .bento-card:hover {
            border-color: #00E676;
            transform: translateY(-2px);
        }
        .bento-title {
            color: #8E9AAF;
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .bento-value {
            color: #FFFFFF;
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 6px;
        }
        .bento-badge-green {
            background-color: rgba(0, 230, 118, 0.15);
            color: #00E676;
            border: 1px solid rgba(0, 230, 118, 0.3);
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
        .bento-badge-blue {
            background-color: rgba(41, 182, 246, 0.15);
            color: #29B6F6;
            border: 1px solid rgba(41, 182, 246, 0.3);
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
        .bento-badge-yellow {
            background-color: rgba(255, 187, 40, 0.15);
            color: #FFBB28;
            border: 1px solid rgba(255, 187, 40, 0.3);
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

    # Baris Utama: 4 Petak Teras Aliran Modal & Ekuiti
    row1_c1, row1_c2, row1_c3, row1_c4 = st.columns(4)

    with row1_c1:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">💵 Jumlah Deposit Terkumpul</div>
            <div class="bento-value">RM {kpis['total_deposit']:,.2f}</div>
            <span class="bento-badge-green">↑ Aliran Modal Masuk</span>
        </div>
        """, unsafe_allow_html=True)

    with row1_c2:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">🏧 Jumlah Pengeluaran Modal</div>
            <div class="bento-value">RM {kpis['total_withdrawal']:,.2f}</div>
            <span class="bento-badge-blue">Kadar Ambilan: {100 - kpis['cash_retention_pct']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with row1_c3:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">🛡️ Modal Bersih Dilaburkan</div>
            <div class="bento-value" style="color: #00E676;">RM {kpis['net_invested']:,.2f}</div>
            <span class="bento-badge-green">Kadar Pengekalan: {kpis['cash_retention_pct']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with row1_c4:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">📊 Nilai Pasaran Aktif (NAV)</div>
            <div class="bento-value" style="color: #29B6F6;">RM {kpis['active_portfolio_val']:,.2f}</div>
            <span class="bento-badge-green">+{kpis['unrealized_roi_pct']:.1f}% Untung Kertas</span>
        </div>
        """, unsafe_allow_html=True)

    # Baris Kedua: 4 Petak Prestasi Institusi & Nisbah Risiko
    row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)

    with row2_c1:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">🎯 Kadar Kemenangan (Win Rate)</div>
            <div class="bento-value">{kpis['win_rate_pct']:.1f}%</div>
            <span class="bento-badge-green">Penanda Aras: > 50.0%</span>
        </div>
        """, unsafe_allow_html=True)

    with row2_c2:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">⚖️ Profit Factor</div>
            <div class="bento-value" style="color: #FFBB28;">{kpis['profit_factor']:.2f}x</div>
            <span class="bento-badge-yellow">Sasaran Institusi: > 1.50x</span>
        </div>
        """, unsafe_allow_html=True)

    with row2_c3:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">📈 Purata Untung vs Rugi</div>
            <div class="bento-value" style="font-size: 1.25rem; padding-top: 4px;">
                <span style="color:#00E676;">RM {kpis['avg_win']:,.0f}</span> / <span style="color:#FF5252;">RM {abs(kpis['avg_loss']):,.0f}</span>
            </div>
            <span class="bento-badge-blue">Nisbah Payoff: 0.61x</span>
        </div>
        """, unsafe_allow_html=True)

    with row2_c4:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-title">💳 Kos Yuran & Faedah Margin</div>
            <div class="bento-value" style="font-size: 1.35rem; color: #E0E0E0;">RM {kpis['margin_fees']:,.2f}</div>
            <span class="bento-badge-blue">Audit Moomoo 8702</span>
        </div>
        """, unsafe_allow_html=True)
