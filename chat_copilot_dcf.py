"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 6: PEMBANTU SEMBANG AI INTERAKTIF & KALKULATOR NILAI WAJAR DCF
========================================================================================
"""

import math

import pandas as pd
import streamlit as st
from metrics_bento import extract_portfolio_kpis
from portfolio_holdings import get_active_holdings
from wealth_debt_engine import get_holistic_balance_sheet

CHAT_HISTORY_KEY = "terminal_chat_history_source_v2"


def calculate_dcf_valuation(fcf_per_share: float, growth_rate_pct: float, terminal_growth_pct: float = 2.5, discount_rate_pct: float = 9.0, years: int = 5) -> dict:
    """
    Mengira Nilai Intrinsik Saham menggunakan Model Aliran Tunai Terdiskaun (DCF).
    """
    inputs = (fcf_per_share, growth_rate_pct, terminal_growth_pct, discount_rate_pct)
    if not all(math.isfinite(value) for value in inputs):
        raise ValueError("Semua andaian DCF mesti nombor terhingga.")
    g = growth_rate_pct / 100.0
    tg = terminal_growth_pct / 100.0
    r = discount_rate_pct / 100.0
    
    if fcf_per_share < 0 or g <= -1 or years < 1 or r <= tg:
        raise ValueError("FCF mesti bukan negatif, tempoh positif, dan kadar diskaun melebihi pertumbuhan terminal.")
        
    projected_fcf = []
    discounted_fcf = []
    current_fcf = fcf_per_share
    
    for yr in range(1, years + 1):
        current_fcf *= (1 + g)
        projected_fcf.append(current_fcf)
        discounted_fcf.append(current_fcf / ((1 + r) ** yr))
        
    # Terminal Value (Gordon Growth Model)
    terminal_value = (projected_fcf[-1] * (1 + tg)) / (r - tg)
    discounted_tv = terminal_value / ((1 + r) ** years)
    
    intrinsic_value = sum(discounted_fcf) + discounted_tv
    return {
        "intrinsic_value": intrinsic_value,
        "pv_fcf_sum": sum(discounted_fcf),
        "pv_terminal_val": discounted_tv,
        "projected_fcf": projected_fcf
    }

def process_ai_chat_response(
    prompt: str,
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
) -> str:
    """Provide deterministic answers from the current source snapshot, not invented advice."""
    prompt_lower = prompt.lower().strip()
    if any(term in prompt_lower for term in ("hutang", "ccris", "liabiliti", "loan", "pinjaman")):
        balance_sheet = get_holistic_balance_sheet(vault_data=vault_data)
        total = balance_sheet["total_liabilities"]
        if total is None:
            return "Baki liabiliti tidak tersedia dalam snapshot sumber semasa."
        monthly = balance_sheet["total_monthly_commitment"]
        monthly_text = (
            "tidak tersedia"
            if monthly is None
            else f"RM {monthly:,.2f}"
        )
        return (
            f"Baki liabiliti daripada sumber: RM {total:,.2f}. "
            f"Komitmen bulanan: {monthly_text}. "
            "Semak penyata institusi kewangan untuk pengesahan."
        )

    holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
    if any(term in prompt_lower for term in ("pegangan", "portfolio", "portfolio semasa")):
        if holdings.empty:
            return "Tiada pegangan bersumber dalam snapshot semasa."
        return "Ticker dalam snapshot semasa: " + ", ".join(holdings["Ticker"].astype(str))

    matching_rows = []
    for _, position in holdings.iterrows():
        ticker = str(position["Ticker"]).strip().lower()
        symbols = {ticker, ticker.rsplit(":", 1)[-1]}
        name = str(position["Nama_Syarikat"]).strip().lower()
        if any(len(symbol) > 1 and symbol in prompt_lower for symbol in symbols) or (
            name and name in prompt_lower
        ):
            matching_rows.append(position)
    if matching_rows:
        position = matching_rows[0]
        pnl = position["Untung_Rugi_MYR"]
        pnl_text = "tidak tersedia" if pd.isna(pnl) else f"RM {pnl:,.2f}"
        return (
            f"{position['Ticker']} dalam snapshot: {position['Unit']:,.4g} unit, "
            f"nilai pasaran RM {position['Nilai_Semasa_MYR']:,.2f}, "
            f"P&L belum realisasi {pnl_text}. "
            "Ini ringkasan data sumber, bukan cadangan beli/jual."
        )
    if any(term in prompt_lower for term in ("ticker", "kaunter", "saham", "status")):
        return "Ticker itu tidak ditemui dalam pegangan snapshot semasa."

    if any(term in prompt_lower for term in ("sejuta", "1m", "sasaran")):
        kpis = extract_portfolio_kpis(vault_data or {}, fx_rate=fx_rate)
        net_invested = kpis.get("net_invested")
        if net_invested is None:
            return "Data aliran tunai untuk mengira modal bersih tidak tersedia dalam snapshot."
        return (
            f"Modal bersih daripada rekod aliran tunai ialah RM {net_invested:,.2f}. "
            "Sasaran dan unjuran tidak dipaparkan kerana sasaran pengguna belum disambungkan."
        )

    return (
        "Pembantu ini hanya membuat carian deterministik dalam snapshot Google Sheets; "
        "ia bukan model AI generatif. Tanya tentang ticker pegangan, baki liabiliti, "
        "atau modal bersih yang tersedia dalam sumber."
    )

def render_interactive_chat_copilot(
    fx_rate: float = 4.0773,
    vault_data: dict | None = None,
):
    st.subheader("💬 Semakan data sumber & kalkulator DCF")
    st.caption("Jawapan portfolio dipetik daripada snapshot; kalkulator DCF menggunakan andaian yang anda masukkan.")

    tab_chat, tab_dcf = st.tabs(["💬 Carian data sumber", "🧮 Kalkulator DCF manual"])

    # 1. Antaramuka Sembang Langsung
    with tab_chat:
        if CHAT_HISTORY_KEY not in st.session_state:
            st.session_state[CHAT_HISTORY_KEY] = [
                {"role": "assistant", "content": "Saya boleh mencari nilai yang tersedia dalam snapshot Google Sheets. Saya bukan model AI generatif dan tidak memberi arahan beli/jual."}
            ]

        # Quick queries stay tied to the current source, not a fixed ticker list.
        q_cols = st.columns(4)
        quick_queries = [
            ("Pegangan semasa", "Senaraikan pegangan semasa"),
            ("Liabiliti", "Semak baki liabiliti"),
            ("Modal bersih", "Semak modal bersih"),
        ]
        current_holdings = get_active_holdings(vault_data, fx_rate=fx_rate)
        if not current_holdings.empty:
            first_ticker = str(current_holdings.iloc[0]["Ticker"])
            quick_queries.append((f"Status {first_ticker}", f"Status {first_ticker}"))
        for column, (label, query) in zip(q_cols, quick_queries):
            with column:
                if st.button(label, width="stretch"):
                    st.session_state[CHAT_HISTORY_KEY].append(
                        {"role": "user", "content": query}
                    )
                    st.session_state[CHAT_HISTORY_KEY].append(
                        {
                            "role": "assistant",
                            "content": process_ai_chat_response(query, fx_rate, vault_data),
                        }
                    )
                    st.rerun()

        st.markdown("---")

        # Paparkan Sejarah Sembang
        for msg in st.session_state[CHAT_HISTORY_KEY]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Medan Input Sembang Natif Streamlit
        user_input = st.chat_input("Tanya tentang ticker, liabiliti, atau modal bersih...")
        if user_input:
            st.session_state[CHAT_HISTORY_KEY].append({"role": "user", "content": user_input})
            reply = process_ai_chat_response(user_input, fx_rate, vault_data)
            st.session_state[CHAT_HISTORY_KEY].append({"role": "assistant", "content": reply})
            st.rerun()

    # 2. Antaramuka Penilaian Wajar DCF
    with tab_dcf:
        st.subheader("🧮 Model Penilaian Aliran Tunai Terdiskaun (Discounted Cash Flow)")
        st.caption("Anggaran matematik daripada andaian manual sahaja; tiada harga atau FCF pasaran yang ditarik secara automatik.")

        d_c1, d_c2 = st.columns(2)
        with d_c1:
            dcf_ticker = st.text_input("Kod saham (label sahaja):", value="", placeholder="Contoh: KLSE:XXXX").upper().strip()
            current_mkt_price = st.number_input("Harga pasaran (input manual, RM / $):", min_value=0.0, value=0.0, step=0.10, format="%.2f")
            fcf_share = st.number_input("FCF sesaham (input manual):", min_value=0.0, value=0.0, step=0.05, format="%.2f")
            growth_5yr = st.slider("Andaian pertumbuhan FCF 5 tahun (% setahun):", 2.0, 25.0, 8.5, step=0.5)
            discount_wacc = st.slider("Andaian kadar diskaun (%):", 6.0, 15.0, 9.0, step=0.5)
            term_growth = st.slider("Andaian pertumbuhan terminal (%):", 1.5, 4.0, 2.5, step=0.1)

        with d_c2:
            if not dcf_ticker or current_mkt_price <= 0 or fcf_share <= 0:
                st.info("Masukkan ticker, harga pasaran dan FCF sesaham yang disahkan sebelum mengira.")
            elif discount_wacc <= term_growth:
                st.warning("Kadar diskaun mesti melebihi kadar pertumbuhan terminal.")
            else:
                dcf_res = calculate_dcf_valuation(
                    fcf_per_share=fcf_share,
                    growth_rate_pct=growth_5yr,
                    terminal_growth_pct=term_growth,
                    discount_rate_pct=discount_wacc,
                    years=5
                )
                intrinsic_val = dcf_res["intrinsic_value"]
                if intrinsic_val <= 0:
                    st.info("Model tidak menghasilkan nilai intrinsik positif untuk andaian ini.")
                else:
                    mos_pct = ((intrinsic_val - current_mkt_price) / intrinsic_val) * 100.0
                    st.markdown("#### Hasil berdasarkan andaian manual:")
                    res_c1, res_c2 = st.columns(2)
                    with res_c1:
                        st.metric("Nilai DCF indikatif", f"{intrinsic_val:.2f}")
                    with res_c2:
                        st.metric("Perbezaan berbanding harga input", f"{mos_pct:+.1f}%")
                    st.caption("Ini bukan fair value yang disahkan atau cadangan pelaburan.")

                    with st.expander("Pecahan model DCF"):
                        st.write(f"PV FCF: {dcf_res['pv_fcf_sum']:.2f}")
                        st.write(f"PV terminal value: {dcf_res['pv_terminal_val']:.2f}")