import os
from personal_finance_suite import render_personal_finance_suite

import streamlit as st
st.set_page_config(
    page_title="Haddy Pro — Terminal Dagangan",
    page_icon="haddy_logo.png" if os.path.exists("haddy_logo.png") else "⚡",
    layout="wide"
)
import pandas as pd
import numpy as np
from datetime import datetime

# --------------------------------------------------------------------------------------
# PROTOKOL KESELAMATAN SULIT (AES-256-GCM + 600,000 PBKDF2 ITERATIONS)
# --------------------------------------------------------------------------------------
from security_vault import verify_vault_authentication

st.set_page_config(
    page_title="Haddy Pro - Terminal Millx",
    page_icon="haddy_logo.png" if os.path.exists("haddy_logo.png") else "⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KUNCI PINTU: Aplikasi akan terhenti di sini sekiranya belum didekripsi!
verify_vault_authentication()

# --------------------------------------------------------------------------------------
# SELEPAS KUNCI DIBUKA: MUAT TURUN MODUL & DATA VAULT
# --------------------------------------------------------------------------------------
from engine_gsheets import load_all_terminal_data
from pipeline_cleaner import process_master_database
from metrics_bento import extract_portfolio_kpis, render_bento_metrics
from visuals_cashflow import get_cashflow_dataframe, render_cumulative_equity_curve, render_annual_flow_breakdown
from portfolio_holdings import get_active_holdings, render_allocation_donut, render_holdings_cards
from debt_management_ui import render_debt_management_dashboard
from wealth_debt_ui import render_wealth_debt_dashboard
from decision_tables import get_top10_bursa, get_top10_us, render_rr_comparison_chart
from master_screener import build_institutional_screener_data, render_canslim_bubble_matrix
from risk_calculator_audio import render_3m_calculator_ui, AUDIO_SOUNDS
from macro_multimedia import LIVE_STREAMS, get_macro_intelligence_data, render_geopolitical_gauges
from moomoo_journal_analytics import render_moomoo_order_generator, render_journal_analytics_dashboard
from system_diagnostics import render_system_diagnostics
from market_heatmap import render_ticker_tape_marquee, render_market_heatmap_tab
from advanced_quant_suite import render_monte_carlo_ui, render_correlation_matrix_ui, render_wyckoff_rvol_screener, render_earnings_dividend_hub
from ai_copilot_mentor import render_ai_copilot_ui
from million_milestone import render_milestone_tracker_ui
from zakat_compliance import render_zakat_compliance_ui
from report_exporter import render_report_exporter_ui
from backtest_engine import render_backtest_ui
from trailing_sentinel import render_trailing_sentinel_ui
from voice_assistant import render_voice_assistant_ui
from paper_autopilot import render_paper_autopilot_ui
from tax_ledger import render_tax_ledger_ui
from crisis_playbook import render_crisis_playbook_ui
from ai_cyborg_sentinel import render_robot_mindset_hud, render_traffic_light_evaluator
from elite_expansion_suite import render_elite_expansion_suite
from ai_soul_core import render_ai_soul_hud
from postmortem_desk import render_postmortem_dashboard
from trade_desk import render_trade_desk_ui

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #8E9AAF;
        margin-bottom: 20px;
    }
    .metric-pill {
        background-color: #1A1F2C;
        border: 1px solid #2E384D;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #00E676;
    }
    .security-badge {
        background: linear-gradient(90deg, #00C853 0%, #009624 100%);
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* PENGEMASAN RESPANSIF MUDAH ALIH (MOBILE UI & PWA POLISH) */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.5rem !important;
        }
        .sub-title {
            font-size: 0.8rem !important;
            margin-bottom: 10px !important;
        }
        .bento-card {
            padding: 12px 14px !important;
            margin-bottom: 10px !important;
        }
        .bento-value {
            font-size: 1.25rem !important;
        }
        .bento-title {
            font-size: 0.72rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px !important;
            font-size: 0.78rem !important;
        }
    }

</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60, show_spinner=False)
def fetch_cached_vault():
    return load_all_terminal_data()

with st.spinner("⚡ Menyegerakkan ekosistem Haddy Pro Vault secara langsung..."):
    vault = fetch_cached_vault()
    kpis = extract_portfolio_kpis(vault)
    fx_rate = 4.0773
    df_holdings = get_active_holdings(vault, fx_rate=fx_rate)
    df_cf = get_cashflow_dataframe(vault)
    df_bursa = get_top10_bursa(vault)
    df_us = get_top10_us(vault)
    df_1000 = build_institutional_screener_data(vault)
    macro_data = get_macro_intelligence_data(vault)

# --------------------------------------------------------------------------------------
# SIDEBAR DENGAN BUTANG KUNCI VAULT (LOGOUT)
# --------------------------------------------------------------------------------------
with st.sidebar:
    st.image("haddy_logo.png", width=75) if os.path.exists("haddy_logo.png") else st.write("⚡")
    st.markdown('<div class="main-title" style="font-size:1.5rem;">HADDY PRO</div>', unsafe_allow_html=True)
    st.markdown('<span class="security-badge">🔒 AES-256 • 600K PBKDF2</span>', unsafe_allow_html=True)
    st.caption("Papan Keputusan Pelaburan Sulit & Berautonomi")
    
    st.markdown("---")
    if st.button("🔒 Kunci Semula Terminal (Logout)", width="stretch"):
        st.session_state["vault_authenticated"] = False
        st.rerun()

    st.markdown("---")
    
    if st.button("🔄 PAKSA SEGERAK GOOGLE SHEETS (FORCE SYNC)", width="stretch"):
        st.cache_data.clear()
        st.toast("⚡ Menyegerakkan data terkini dari Google Sheets...", icon="🔄")
        st.rerun()

    st.subheader("🌐 Status Sistem & Suapan")
    st.markdown('<span class="metric-pill">● 100% OPERASI NORMAL</span>', unsafe_allow_html=True)
    st.caption(f"Cap Masa: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} MYT")
    
    st.markdown("---")
    st.subheader("💱 Kadar Tukaran Induk (FX Anchor)")
    fx_rate = st.number_input("USD/MYR:", value=4.0773, format="%.4f")
    
    st.markdown("---")
    st.subheader("🔊 Ujian Isyarat Audio")
    import os
    if os.path.exists("chime_success.wav"):
        with open("chime_success.wav", "rb") as f:
            st.audio(f.read(), format="audio/wav")
    st.caption("Chime Entri Disiplin Berjaya")
    if os.path.exists("siren_alarm.wav"):
        with open("siren_alarm.wav", "rb") as f:
            st.audio(f.read(), format="audio/wav")
    st.caption("Siren Had Risiko Stop Loss")

# --------------------------------------------------------------------------------------
# KEPALA HALAMAN & BENTO-BOX EKSEKUTIF
# --------------------------------------------------------------------------------------
render_ticker_tape_marquee()

render_robot_mindset_hud()

col_h1, col_h2 = st.columns([7, 3])
with col_h1:
    st.markdown('<div class="main-title">HADDY PRO - TERMINAL MILLX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sistem Papan Keputusan Pelaburan Berautonomi Penuh • Bursa Malaysia & Wall Street US</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:right;"><span class="metric-pill">AES-256 SULIT & BERSIFAT PERIBADI</span></div>', unsafe_allow_html=True)

render_ai_soul_hud()

render_bento_metrics(kpis)

st.markdown("---")

# --------------------------------------------------------------------------------------
# 6 TAB INTERAKTIF TERMINAL
# --------------------------------------------------------------------------------------
tab_exec, tab_debt, tab_pfs, tab_port, tab_screener, tab_calc, tab_tradedesk, tab_heatmap, tab_cyborg, tab_quant, tab_sentinel, tab_backtest, tab_voice, tab_paper, tab_tax, tab_mentor, tab_million, tab_zakat, tab_report, tab_macro, tab_postmortem, tab_crisis, tab_elite, tab_diag = st.tabs([
    "🎯 1. Meja Keputusan Harian",
    "🏛️ 2. Pengurusan Hutang & CCRIS",
    "🏦 3. Perbankan, KWSP, PTPTN & Syariah",
    "🏛️ 2. Pengurusan Hutang & Profil Kredit CCRIS",
    "📊 3. Master 1,000 & CANSLIM",
    "🧮 4. Kalkulator 3M & Moomoo",
    "⚡ 5. Meja Beli/Jual & Watchlist",
    "🗺️ 6. Peta Haba Pasaran (Heatmap)",
    "🚦 7. Lampu Isyarat & Amaran AI",
    "🎲 7. Enjin Kuantitatif & Risiko",
    "🛡️ 8. Trailing Stop Sentinel",
    "🧪 9. Enjin Backtest Lampau",
    "🎙️ 10. Pembantu Suara AI",
    "🤖 11. Bot Simulasi Paper",
    "🏛️ 12. Penyata Cukai LHDN",
    "🤖 13. AI Mentor DDNK",
    "🎯 14. Sasaran Sejuta (RM 1M)",
    "🌙 15. Zakat Saham & Syariah",
    "📑 16. Laporan Excel 1-Klik",
    "📡 17. Radar Makro & Multimedia",
    "🧠 18. Bedah Siasat: Kebodohan dan Kecerdikan",
    "🚨 19. Protokol Krisis & SOP 15-Minit",
    "🚀 20. Enjin Tindakan Elit & Rebalance",
    "🖥️ 21. Diagnostik Sistem Rangkaian"
])

with tab_exec:
    st.header("🎯 Meja Keputusan Harian (Top 10 Bursa & Top 10 Wall Street)")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.metric("Total Calon Entri Terpilih", "20 Saham", "10 Bursa + 10 US")
    with c_m2:
        st.metric("Purata Potensi R:R Bursa", f"{df_bursa['RR'].mean():.2f}x", "≥ 2.50x")
    with c_m3:
        st.metric("Purata Potensi R:R Wall Street", f"{df_us['RR'].mean():.2f}x", "≥ 2.50x")
        
    st.markdown("---")
    sub_bursa, sub_us = st.tabs(["🇲🇾 10 Saham Terbaik Bursa Malaysia", "🇺🇸 10 Saham Terbaik Wall Street US"])
    with sub_bursa:
        st.dataframe(df_bursa.style.format({"Harga_Live": "RM {:.2f}", "SL": "RM {:.2f}", "TP": "RM {:.2f}", "RR": "{:.2f}x"}), width="stretch", hide_index=True)
    with sub_us:
        st.dataframe(df_us.style.format({"Harga_Live": "${:.2f}", "SL": "${:.2f}", "TP": "${:.2f}", "RR": "{:.2f}x"}), width="stretch", hide_index=True)
    st.plotly_chart(render_rr_comparison_chart(df_bursa, df_us), width="stretch")

with tab_debt:
    render_debt_management_dashboard(vault, stock_portfolio_val=kpis.get("active_portfolio_val", 55945.32))

with tab_pfs:
    render_personal_finance_suite(vault, net_equity=kpis.get("active_portfolio_val", 55945.32))

with tab_port:
    st.header("🏛️ Pemantauan Posisi Langsung & Prestasi Aliran Tunai")
    render_holdings_cards(df_holdings)
    st.markdown("---")
    p_col1, p_col2 = st.columns([5, 5])
    with p_col1:
        st.plotly_chart(render_cumulative_equity_curve(df_cf), width="stretch")
    with p_col2:
        st.plotly_chart(render_allocation_donut(df_holdings), width="stretch")
    st.plotly_chart(render_annual_flow_breakdown(df_cf), width="stretch")
    st.markdown("---")
    render_journal_analytics_dashboard()

with tab_screener:
    st.header("📊 Pangkalan Data 1,000 Saham Elit & Matriks Bebola CANSLIM")
    st.plotly_chart(render_canslim_bubble_matrix(df_1000), width="stretch")
    st.markdown("---")
    sf1, sf2, sf3, sf4 = st.columns(4)
    with sf1: m_sel = st.selectbox("Pasaran:", ["Semua Pasaran", "Bursa Malaysia", "Wall Street US"])
    with sf2: s_sel = st.selectbox("Sektor:", ["Semua Sektor"] + sorted(df_1000["Sektor"].unique().tolist()))
    with sf3: st_sel = st.selectbox("Status:", ["Semua Status", "Boleh Beli", "Pantau"])
    with sf4: q_search = st.text_input("Cari Saham:", "", placeholder="cth: TENAGA, NVDA...")
    df_view = df_1000.copy()
    if m_sel != "Semua Pasaran": df_view = df_view[df_view["Pasaran"] == m_sel]
    if s_sel != "Semua Sektor": df_view = df_view[df_view["Sektor"] == s_sel]
    if st_sel != "Semua Status": df_view = df_view[df_view["Keputusan"] == st_sel]
    if q_search: df_view = df_view[df_view["Ticker"].str.contains(q_search.strip().upper(), na=False)]
    st.dataframe(df_view[["No", "Ticker", "Pasaran", "Sektor", "Harga_Semasa", "Sasaran_TP", "Potensi_Upside_Pct", "CANSLIM_Score", "Fasa_Wyckoff", "Smart_Money", "Keputusan"]].style.format({"Harga_Semasa": "{:.2f}", "Sasaran_TP": "{:.2f}", "Potensi_Upside_Pct": "+{:.1f}%", "CANSLIM_Score": "{:d}/100"}), width="stretch", hide_index=True)

with tab_calc:
    st.header("🧮 Pengurusan Risiko DDNK 3M & Eksekusi Pesanan Moomoo")
    render_3m_calculator_ui(account_capital=kpis["net_invested"], fx_rate=fx_rate)
    st.markdown("---")
    render_moomoo_order_generator()

with tab_tradedesk:
    st.header("⚡ Meja Tindakan Pantas: Watchlist, Beli & Jual")
    render_trade_desk_ui(fx_rate=fx_rate)

with tab_heatmap:
    render_market_heatmap_tab()

with tab_cyborg:
    render_traffic_light_evaluator()

with tab_quant:
    st.header("🎲 Enjin Kuantitatif Institusi & Matriks Risiko")
    q_sub1, q_sub2, q_sub3, q_sub4 = st.tabs([
        "🎲 Simulasi Monte Carlo",
        "⚡ Matriks Korelasi & Kluster",
        "🎯 Radar Wyckoff Jerung (RVOL)",
        "📅 Kalendar Earnings & Dividen"
    ])
    with q_sub1:
        render_monte_carlo_ui(starting_capital=kpis["net_invested"])
    with q_sub2:
        render_correlation_matrix_ui()
    with q_sub3:
        render_wyckoff_rvol_screener()
    with q_sub4:
        render_earnings_dividend_hub(fx_rate=fx_rate)

with tab_sentinel:
    render_trailing_sentinel_ui()

with tab_backtest:
    render_backtest_ui()

with tab_voice:
    render_voice_assistant_ui()

with tab_paper:
    render_paper_autopilot_ui()

with tab_tax:
    render_tax_ledger_ui()

with tab_mentor:
    render_ai_copilot_ui(fx_rate=fx_rate, net_capital=kpis["net_invested"])

with tab_million:
    render_milestone_tracker_ui(vault, current_net_capital=kpis["net_invested"])

with tab_zakat:
    render_zakat_compliance_ui(net_equity=kpis.get("active_portfolio_val", 55945.32))

with tab_report:
    render_report_exporter_ui(vault, kpis, df_bursa, df_us)

with tab_macro:
    st.header("📡 Radar Risikan Makro, Geopolitik & Suapan Media")
    st.plotly_chart(render_geopolitical_gauges(), width="stretch")
    st.markdown("---")
    vm_col1, vm_col2 = st.columns([5, 5])
    with vm_col1:
        sel_stream = st.selectbox("Pilih Saluran Berita Langsung:", list(LIVE_STREAMS.keys()))
        st.video(LIVE_STREAMS[sel_stream])
    with vm_col2:
        m_t1, m_t2, m_t3 = st.tabs(["FOMC Fed", "Geopolitik", "Pengumuman Bursa"])
        with m_t1: st.dataframe(macro_data["fomc"], width="stretch", hide_index=True)
        with m_t2: st.dataframe(macro_data["geopolitics"], width="stretch", hide_index=True)
        with m_t3: st.dataframe(macro_data["corporate"], width="stretch", hide_index=True)

with tab_postmortem:
    render_postmortem_dashboard(fx_rate=fx_rate)

with tab_crisis:
    render_crisis_playbook_ui(net_equity=kpis.get("active_portfolio_val", 55945.32))

with tab_elite:
    render_elite_expansion_suite(fx_rate=fx_rate)

with tab_diag:
    render_system_diagnostics()

st.markdown("---")
st.markdown("<center><small>Haddy Pro Terminal Millx • 100% Private Mode • AES-256-GCM Locked (600,000 PBKDF2 Iterations)</small></center>", unsafe_allow_html=True)
