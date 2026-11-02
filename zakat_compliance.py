"""Manual zakat estimate calculator with explicit, user-supplied assumptions."""

import math

import streamlit as st


def calculate_stock_zakat(
    active_portfolio_val: float,
    cash_buffer: float,
    short_term_liabilities: float,
    gold_price_per_gram: float,
) -> dict:
    """Calculate an illustrative estimate; confirm eligibility with a zakat authority."""
    values = (
        active_portfolio_val,
        cash_buffer,
        short_term_liabilities,
        gold_price_per_gram,
    )
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Semua nilai mesti nombor terhingga.")
    if min(active_portfolio_val, cash_buffer, short_term_liabilities) < 0:
        raise ValueError("Nilai aset dan liabiliti tidak boleh negatif.")
    if gold_price_per_gram <= 0:
        raise ValueError("Harga emas per gram mesti positif.")

    total_assets = active_portfolio_val + cash_buffer
    zakatable_wealth = max(total_assets - short_term_liabilities, 0.0)
    nisab_value = 85.0 * gold_price_per_gram
    zakat_payable = zakatable_wealth * 0.025 if zakatable_wealth >= nisab_value else 0.0
    return {
        "active_portfolio_val": active_portfolio_val,
        "cash_buffer": cash_buffer,
        "total_assets": total_assets,
        "short_term_liabilities": short_term_liabilities,
        "net_zakatable_wealth": zakatable_wealth,
        "gold_price_per_gram": gold_price_per_gram,
        "nisab_value": nisab_value,
        "is_nisab_reached": zakatable_wealth >= nisab_value,
        "zakat_rate_pct": 2.5,
        "zakat_payable": zakat_payable,
    }


def render_zakat_compliance_ui(
    net_equity: float | None = None,
):
    st.subheader("Anggaran zakat saham")
    st.caption(
        "Anggaran berdasarkan kaedah input dan nisab 85g yang dipilih; bukan "
        "keputusan rasmi. Sahkan kaedah, tempoh haul dan harga emas dengan "
        "pihak zakat negeri."
    )
    with st.form("zakat_calculator_form"):
        portfolio_default = (
            float(net_equity)
            if net_equity is not None and math.isfinite(float(net_equity))
            else 0.0
        )
        portfolio_value = st.number_input(
            "Nilai pasaran saham (RM; sumber atau input manual)",
            min_value=0.0,
            value=portfolio_default,
            step=1000.0,
        )
        cash_buffer = st.number_input(
            "Tunai yang layak dipertimbangkan (RM; input manual)",
            min_value=0.0,
            value=0.0,
            step=500.0,
        )
        short_term_liabilities = st.number_input(
            "Liabiliti jangka pendek (RM; input manual)",
            min_value=0.0,
            value=0.0,
            step=500.0,
        )
        gold_price = st.number_input(
            "Harga emas semasa per gram (RM; input manual)",
            min_value=0.0,
            value=0.0,
            step=1.0,
        )
        confirmed = st.checkbox(
            "Saya telah mengesahkan semua baki dan andaian di atas."
        )
        submitted = st.form_submit_button("Kira anggaran", width="stretch")

    if not submitted:
        st.info("Lengkapkan nilai dan sahkan input sebelum membuat pengiraan.")
        return
    if not confirmed:
        st.warning("Sahkan dahulu semua baki dan andaian yang dimasukkan.")
        return
    if gold_price <= 0:
        st.warning("Masukkan harga emas semasa yang telah disahkan.")
        return

    result = calculate_stock_zakat(
        active_portfolio_val=portfolio_value,
        cash_buffer=cash_buffer,
        short_term_liabilities=short_term_liabilities,
        gold_price_per_gram=gold_price,
    )
    first, second = st.columns(2)
    first.metric("Nisab input (85g)", f"RM {result['nisab_value']:,.2f}")
    second.metric(
        "Harta bersih untuk anggaran",
        f"RM {result['net_zakatable_wealth']:,.2f}",
    )
    if result["is_nisab_reached"]:
        st.success(f"Anggaran 2.5%: RM {result['zakat_payable']:,.2f}")
    else:
        st.info("Nilai input berada di bawah nisab yang dikira; anggaran bayaran ialah RM 0.")
