from gold_master_release import render_gold_master_dashboard
from unusual_volume_anomaly import render_unusual_volume_scanner_ui
from portfolio_opt_debt_strategy import render_markowitz_efficient_frontier_ui, render_debt_payoff_strategies_ui
from fundamental_health_sankey import render_fundamental_health_and_sankey_ui
from chat_copilot_dcf import render_interactive_chat_copilot
from order_dialog_cost_engine import open_quick_order_modal
import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. Protokol Keselamatan AES-256
from security_vault import verify_vault_authentication

st.set_page_config(
    page_title="Haddy Pro - Terminal Millx",
    page_icon="haddy_logo.png" if os.path.exists("haddy_logo.png") else "⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kunci Akses Mandatori
verify_vault_authentication()

# 2. Import Modul Bersepadu
from engine_gsheets import load_all_terminal_data
from pipeline_cleaner import process_master_database
from metrics_bento import extract_portfolio_kpis, render_bento_metrics
from visuals_cashflow import get_cashflow_dataframe, render_cumulative_equity_curve, render_annual_flow_breakdown
from portfolio_holdings import get_active_holdings, render_allocation_donut, render_holdings_cards
from decision_tables import get_top10_bursa, get_top10_us, render_rr_comparison_chart
from master_screener import build_institutional_screener_data, render_canslim_bubble_matrix
from risk_calculator_audio import render_3m_calculator_ui, AUDIO_SOUNDS
from macro_multimedia import LIVE_STREAMS, get_macro_intelligence_data, render_geopolitical_gauges
from moomoo_journal_analytics import render_moomoo_order_generator, render_journal_analytics_dashboard
from system_diagnostics import render_system_diagnostics
from trade_desk import render_trade_desk_ui
from postmortem_desk import render_postmortem_dashboard
from market_heatmap import render_ticker_tape_marquee, render_market_heatmap_tab
from advanced_quant_suite import render_monte_carlo_ui, render_correlation_matrix_ui, render_wyckoff_rvol_screener, render_earnings_dividend_hub
from ai_copilot_mentor import render_ai_copilot_ui
from million_milestone import render_milestone_tracker_ui
from zakat_compliance import render_zakat_compliance_ui
from report_exporter import render_report_exporter_ui
from trailing_sentinel import render_trailing_sentinel_ui
from backtest_engine import render_backtest_ui
from voice_assistant import render_voice_assistant_ui
from paper_autopilot import render_paper_autopilot_ui
from tax_ledger import render_tax_ledger_ui
from crisis_playbook import render_crisis_playbook_ui
from ai_cyborg_sentinel import render_robot_mindset_hud, render_traffic_light_evaluator
from hardcore_ai_engine import render_hardcore_ai_soul_hud
from debt_management_ui import render_debt_management_dashboard
from personal_finance_suite import render_personal_finance_suite
from fluent_core_engine import get_dual_market_status
from modern_grid_ui import render_modern_decision_grid
from macro_intelligence_hub import render_macro_intelligence_dashboard

# 3. Gaya Visual Terminal & Responsif Mudah Alih
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; color: #FFFFFF; margin-bottom: 0px; }
    .sub-title { font-size: 0.95rem; color: #8E9AAF; margin-bottom: 16px; }
    .metric-pill { background-color: #1A1F2C; border: 1px solid #2E384D; border-radius: 8px; padding: 4px 12px; font-size: 0.85rem; font-weight: 600; color: #00E676; }
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem !important; }
        .sub-title { font-size: 0.8rem !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 8px !important; font-size: 0.78rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# 4. Pemuatan Data Latar Belakang
fx_rate = 4.0773
@st.cache_data(ttl=60, show_spinner=False)
def fetch_cached_vault():
    return load_all_terminal_data()

with st.spinner("⚡ Menyegerakkan pangkalan data Haddy Pro Vault..."):
    vault = fetch_cached_vault()
    kpis = extract_portfolio_kpis(vault)
    df_holdings = get_active_holdings(vault, fx_rate=fx_rate)
    df_cf = get_cashflow_dataframe(vault)
    df_bursa = get_top10_bursa(vault)
    df_us = get_top10_us(vault)
    df_1000 = build_institutional_screener_data(vault)
    macro_data = get_macro_intelligence_data(vault)

# 5. Bar Sisi (Sidebar)
with st.sidebar:
    if os.path.exists("haddy_logo.png"):
        st.image("haddy_logo.png", width=75)
    else:
        st.write("⚡")
    st.markdown('<div class="main-title" style="font-size:1.4rem;">HADDY PRO</div>', unsafe_allow_html=True)
    st.caption("Terminal Kuantitatif & Kewangan Holistik")
    st.markdown("---")
    
    st.subheader("🧭 PENGEMUDI MOD PAPARAN")
    mode_switch = st.radio(
        "PILIH SEGMEN KANDUNGAN:",
        [
            "🌐 Paparan Penuh (Semua 12 Hab)",
            "📈 Pasaran Saham (Bursa & US)",
            "🏛️ Bukan Saham (Liabiliti & Bank)"
        ],
        index=0
    )
    st.markdown("---")

    if st.button("🔄 PAKSA SEGERAK (FORCE SYNC)", width="stretch"):
        st.cache_data.clear()
        st.toast("⚡ Data disegerakkan dari Google Sheets!", icon="🔄")
        st.rerun()

    if st.button("🔒 Kunci Terminal (Logout)", width="stretch"):
        st.session_state["vault_authenticated"] = False
        st.rerun()

    st.markdown("---")
    st.subheader("🔊 Isyarat Audio Tempatan")
    if os.path.exists("chime_success.wav"):
        with open("chime_success.wav", "rb") as f:
            st.audio(f.read(), format="audio/wav")
    st.caption("Chime Entri Disiplin")
    if os.path.exists("siren_alarm.wav"):
        with open("siren_alarm.wav", "rb") as f:
            st.audio(f.read(), format="audio/wav")
    st.caption("Siren Stop Loss")

# 6. Pengepala Utama, Status Dwipasaran (BEBAS BACKSLASH), Ticker Tape, HUD Robot & Roh AI
m_stat = get_dual_market_status()
b_color = m_stat["bursa"]["color"]
b_status = m_stat["bursa"]["status"]
b_time = m_stat["bursa"]["time_str"]

u_color = m_stat["us"]["color"]
u_status = m_stat["us"]["status"]
u_time = m_stat["us"]["time_str"]

col_mb1, col_mb2 = st.columns([5, 5])
with col_mb1:
    st.markdown(f"""<div style="background:#161D2B; border:1px solid #2B384E; border-left:4px solid {b_color}; border-radius:8px; padding:6px 12px; margin-bottom:10px;"><small style="color:#8E9AAF; font-weight:700;">🇲🇾 BURSA MALAYSIA:</small> <span style="color:{b_color}; font-weight:800; font-size:0.85rem;">{b_status}</span><br><small style="color:#A0AEC0;">{b_time}</small></div>""", unsafe_allow_html=True)
with col_mb2:
    st.markdown(f"""<div style="background:#161D2B; border:1px solid #2B384E; border-left:4px solid {u_color}; border-radius:8px; padding:6px 12px; margin-bottom:10px;"><small style="color:#8E9AAF; font-weight:700;">🇺🇸 WALL STREET US:</small> <span style="color:{u_color}; font-weight:800; font-size:0.85rem;">{u_status}</span><br><small style="color:#A0AEC0;">{u_time}</small></div>""", unsafe_allow_html=True)

render_ticker_tape_marquee()
render_robot_mindset_hud()
render_hardcore_ai_soul_hud()

col_h1, col_h2 = st.columns([7, 3])
with col_h1:
    st.markdown('<div class="main-title">HADDY PRO — TERMINAL MILLX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sistem Operasi Kewangan Holistik & Dagangan Dwibenua • 12 Hab Bersepadu</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:right;"><span class="metric-pill">MOD: {mode_switch.upper()}</span></div>', unsafe_allow_html=True)

render_bento_metrics(kpis)
st.markdown("---")

# ======================================================================================
# 7. LOGIK PAPARAN 12 HAB MENGIKUT SUIS RADIO BUTTON
# ======================================================================================

# PILIHAN 1: HANYA SAHAM
if mode_switch == "📈 Pasaran Saham (Bursa & US)":
    st.info("📈 **MOD SEGMEN: PASARAN SAHAM (BURSA MALAYSIA & US WALL STREET)**")
    s1, s2, s3, s4, s5, s6, s7, s8 = st.tabs([
        "🎯 1. Meja Keputusan",
        "📦 2. Portfolio Aktif",
        "⚡ 3. Meja Beli & Jual",
        "📡 4. Radar Makro",
        "🗺️ 5. Peta Haba & 1000",
        "🎲 6. Enjin Kuantitatif",
        "🤖 7. Penasihat AI DDNK",
        "🎯 8. Sasaran Sejuta"
    ])
    with s1:
        st.header("🎯 Meja Keputusan Harian (Windows 11 Modern Grid)")
        
        col_btn1, col_btn2 = st.columns([7, 3])
        with col_btn2:
            if st.button("⚡ TIKET PESANAN PANTAS & KIRA KOS", width="stretch"):
                open_quick_order_modal("KLSE:TENAGA", 12.75, fx_rate=fx_rate)

        render_modern_decision_grid(df_bursa, df_us)
        st.plotly_chart(render_rr_comparison_chart(df_bursa, df_us), width="stretch")
    with s2:
        st.header("📦 Pemantauan Posisi Langsung, Trailing Stop & Aliran Tunai")
        render_holdings_cards(df_holdings)
        st.markdown("---")
        render_trailing_sentinel_ui()
        st.markdown("---")
        p1, p2 = st.columns(2)
        with p1: st.plotly_chart(render_cumulative_equity_curve(df_cf), width="stretch")
        with p2: st.plotly_chart(render_allocation_donut(df_holdings), width="stretch")
    with s3:
        st.header("⚡ Meja Tindakan Pantas: Beli, Jual, Watchlist & Carta Lilin")
        render_trade_desk_ui(fx_rate=fx_rate)
    with s4:
        st.header("📡 Radar Risikan Makro, Hasil Bon & Geopolitik")
        render_macro_intelligence_dashboard(fx_rate=fx_rate)
        st.markdown("---")
        st.plotly_chart(render_geopolitical_gauges(), width="stretch")
    with s5:
        t_hm, t_sc = st.tabs(["🗺️ Peta Haba Sektor (Treemap)", "📊 Pengimbas 1,000 Saham Elit"])
        with t_hm: render_market_heatmap_tab()
        with t_sc:
            st.plotly_chart(render_canslim_bubble_matrix(df_1000), width="stretch")
            st.dataframe(df_1000.head(100), width="stretch", hide_index=True)
    with s6:
        st.header("🎲 Enjin Kuantitatif & Simulasi Risiko")
        q1, q2, q3, q4, q5, q6, q7, q8 = st.tabs(["🎲 Monte Carlo", "⚡ Matriks Korelasi", "📊 Markowitz Frontier", "🎯 Wyckoff RVOL", "⚡ Anomali RVOL & Manipulasi", "📅 Kalendar Earnings", "🧪 Backtest Lampau", "🏆 Skor Kesihatan & Sankey"])
        with q1: render_monte_carlo_ui(starting_capital=kpis["net_invested"])
        with q2: render_correlation_matrix_ui()
        with q3: render_markowitz_efficient_frontier_ui()
        with q4: render_wyckoff_rvol_screener()
        with q5: render_unusual_volume_scanner_ui()
        with q6: render_earnings_dividend_hub(fx_rate=fx_rate)
        with q7: render_backtest_ui()
        with q8: render_fundamental_health_and_sankey_ui(fx_rate=fx_rate)
    with s7:
        st.header("🤖 Penasihat AI DDNK, Disiplin Robotik & Suara")
        a1, a2, a3, a4, a5 = st.tabs(["💬 Sembang AI & DCF", "🤖 AI Mentor DDNK", "🚦 Lampu Isyarat Robot", "🎙️ Pembantu Suara AI", "🤖 Bot Paper Trading"])
        with a1:
            render_interactive_chat_copilot(fx_rate=fx_rate)
        with a5: render_ai_copilot_ui(fx_rate=fx_rate, net_capital=kpis["net_invested"])
        with a2: render_traffic_light_evaluator()
        with a3: render_voice_assistant_ui()
        with a4: render_paper_autopilot_ui()
    with s8:
        render_milestone_tracker_ui(vault, current_net_capital=kpis["net_invested"])

# PILIHAN 2: BUKAN SAHAM
elif mode_switch == "🏛️ Bukan Saham (Liabiliti & Bank)":
    st.info("🏛️ **MOD SEGMEN: BUKAN SAHAM (LIABILITI CCRIS, SIMPANAN BANK, KWSP & ZAKAT)**")
    b1, b2, b3, b4, b5 = st.tabs([
        "🏛️ 1. Liabiliti & CCRIS",
        "🏦 2. Simpanan, KWSP & Bank",
        "🌙 3. Fiqh Syariah & Zakat",
        "📑 4. Penyata Cukai LHDN",
        "🚨 5. Protokol Krisis & SOP"
    ])
    with b1:
        render_debt_management_dashboard(vault, stock_portfolio_val=kpis.get("active_portfolio_val", 55945.32))
    with b2:
        render_personal_finance_suite(vault, net_equity=kpis.get("active_portfolio_val", 55945.32))
    with b3:
        render_zakat_compliance_ui(net_equity=kpis.get("active_portfolio_val", 55945.32))
    with b4:
        c1, c2 = st.columns(2)
        with c1: render_tax_ledger_ui()
        with c2: render_report_exporter_ui(vault, kpis, df_bursa, df_us)
    with b5:
        render_crisis_playbook_ui(net_equity=kpis.get("active_portfolio_val", 55945.32))

# PILIHAN 3: PAPARAN LENGKAP 12 HAB INDUK (DEFAULT)
else:
    st.info("🌐 **MOD SEGMEN: PAPARAN PENUH (KESELURUHAN 12 HAB BERSEPADU)**")
    h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12 = st.tabs([
        "🎯 1. Meja Keputusan",
        "🏛️ 2. Liabiliti & CCRIS",
        "🏦 3. Simpanan & Bank",
        "📦 4. Portfolio Aktif",
        "⚡ 5. Meja Beli & Jual",
        "📡 6. Radar Makro",
        "🗺️ 7. Peta Haba & 1000",
        "🎲 8. Enjin Kuantitatif",
        "🤖 9. AI Mentor & Suara",
        "🎯 10. Sasaran Sejuta",
        "🧠 11. Bedah Siasat & Audit",
        "📑 12. Cukai, Laporan & Krisis"
    ])

    # 1. Meja Keputusan
    with h1:
        st.header("🎯 Meja Keputusan Harian (Windows 11 Modern Grid)")
        
        col_btn1, col_btn2 = st.columns([7, 3])
        with col_btn2:
            if st.button("⚡ TIKET PESANAN PANTAS & KIRA KOS", width="stretch"):
                open_quick_order_modal("KLSE:TENAGA", 12.75, fx_rate=fx_rate)

        render_modern_decision_grid(df_bursa, df_us)
        st.plotly_chart(render_rr_comparison_chart(df_bursa, df_us), width="stretch")

    # 2. Liabiliti & CCRIS
    with h2:
        render_debt_management_dashboard(vault, stock_portfolio_val=kpis.get("active_portfolio_val", 55945.32))

    # 3. Simpanan, Bank & KWSP
    with h3:
        render_personal_finance_suite(vault, net_equity=kpis.get("active_portfolio_val", 55945.32))

    # 4. Portfolio Aktif & Trailing Sentinel
    with h4:
        st.header("📦 Pemantauan Posisi Langsung, Trailing Stop & Aliran Tunai")
        render_holdings_cards(df_holdings)
        st.markdown("---")
        render_trailing_sentinel_ui()
        st.markdown("---")
        p1, p2 = st.columns(2)
        with p1: st.plotly_chart(render_cumulative_equity_curve(df_cf), width="stretch")
        with p2: st.plotly_chart(render_allocation_donut(df_holdings), width="stretch")
        st.plotly_chart(render_annual_flow_breakdown(df_cf), width="stretch")

    # 5. Meja Beli/Jual & Watchlist
    with h5:
        st.header("⚡ Meja Tindakan Pantas: Beli, Jual, Watchlist & Carta Lilin")
        render_trade_desk_ui(fx_rate=fx_rate)

    # 6. RADAR MAKRO (LENGKAP DENGAN FRED & VIDEO)
    with h6:
        st.header("📡 Radar Risikan Makroekonomi, Hasil Bon & Geopolitik")
        render_macro_intelligence_dashboard(fx_rate=fx_rate)
        st.markdown("---")
        st.subheader("🛢️ Tolok Risiko Komoditi & Sentimen Global")
        st.plotly_chart(render_geopolitical_gauges(), width="stretch")
        st.markdown("---")
        vm_col1, vm_col2 = st.columns([5, 5])
        with vm_col1:
            st.subheader("📺 Suapan Video Kewangan Langsung")
            sel_stream = st.selectbox("Pilih Saluran Berita Langsung:", list(LIVE_STREAMS.keys()))
            st.video(LIVE_STREAMS[sel_stream])
        with vm_col2:
            st.subheader("🏛️ Radar Keputusan Fed & Pengumuman Bursa")
            m_t1, m_t2, m_t3 = st.tabs(["FOMC Fed", "Geopolitik Selat Hormuz", "Pengumuman Bursa"])
            with m_t1: st.dataframe(macro_data["fomc"], width="stretch", hide_index=True)
            with m_t2: st.dataframe(macro_data["geopolitics"], width="stretch", hide_index=True)
            with m_t3: st.dataframe(macro_data["corporate"], width="stretch", hide_index=True)

    # 7. Peta Haba & Pangkalan 1000
    with h7:
        t_hm, t_sc = st.tabs(["🗺️ Peta Haba Sektor (Treemap)", "📊 Pengimbas 1,000 Saham Elit"])
        with t_hm: render_market_heatmap_tab()
        with t_sc:
            st.plotly_chart(render_canslim_bubble_matrix(df_1000), width="stretch")
            st.dataframe(df_1000.head(100), width="stretch", hide_index=True)

    # 8. Enjin Kuantitatif, Kesihatan Fundamental & Aliran Sankey
    with h8:
        q1, q2, q3, q4, q5, q6, q7, q8 = st.tabs(["🎲 Monte Carlo", "⚡ Matriks Korelasi", "📊 Markowitz Frontier", "🎯 Wyckoff RVOL", "⚡ Anomali RVOL & Manipulasi", "📅 Kalendar Earnings", "🧪 Backtest Lampau", "🏆 Skor Kesihatan & Sankey"])
        with q1: render_monte_carlo_ui(starting_capital=kpis["net_invested"])
        with q2: render_correlation_matrix_ui()
        with q3: render_markowitz_efficient_frontier_ui()
        with q4: render_wyckoff_rvol_screener()
        with q5: render_unusual_volume_scanner_ui()
        with q6: render_earnings_dividend_hub(fx_rate=fx_rate)
        with q7: render_backtest_ui()
        with q8: render_fundamental_health_and_sankey_ui(fx_rate=fx_rate)

    # 9. AI Mentor, Lampu Isyarat, Suara & Sembang Interaktif
    with h9:
        a1, a2, a3, a4, a5 = st.tabs(["💬 Sembang AI & DCF", "🤖 AI Mentor DDNK", "🚦 Lampu Isyarat Robot", "🎙️ Pembantu Suara AI", "🤖 Bot Paper Trading"])
        with a1:
            render_interactive_chat_copilot(fx_rate=fx_rate)
        with a1: render_ai_copilot_ui(fx_rate=fx_rate, net_capital=kpis["net_invested"])
        with a2: render_traffic_light_evaluator()
        with a3: render_voice_assistant_ui()
        with a4: render_paper_autopilot_ui()

    # 10. Sasaran Sejuta
    with h10:
        render_milestone_tracker_ui(vault, current_net_capital=kpis["net_invested"])

    # 11. Bedah Siasat & Audit Diri
    with h11:
        st.header("🧠 Bedah Siasat Forensik: Kebodohan dan Kecerdikan Saya")
        render_postmortem_dashboard(fx_rate=fx_rate)

    # 12. Cukai, Laporan & Krisis
    with h12:
        st.header("📑 Cukai LHDN, Laporan Excel 1-Klik & Protokol Krisis")
        x1, x2, x3, x4 = st.tabs(["🏆 Rilis Induk v2.0", "🏛️ Penyata Cukai LHDN", "📑 Penjana Excel 1-Klik", "🚨 Protokol Krisis Black Swan"])
        with x1: render_gold_master_dashboard(kpis, vault, fx_rate=fx_rate)
        with x2: render_tax_ledger_ui()
        with x3: render_report_exporter_ui(vault, kpis, df_bursa, df_us)
        with x4: render_crisis_playbook_ui(net_equity=kpis.get("active_portfolio_val", 55945.32))

st.markdown("---")
st.markdown("<center><small>Haddy Pro Terminal Millx • 12 Hab Bersepadu Penuh • AES-256 Kriptografi Kebal</small></center>", unsafe_allow_html=True)