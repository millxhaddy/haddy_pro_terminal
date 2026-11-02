"""User-input compounding scenarios; no return or contribution forecast is assumed."""

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from metrics_bento import extract_portfolio_kpis


def calculate_compounding_schedule(
    starting_capital: float,
    monthly_deposit: float,
    monthly_roi_pct: float,
    months: int,
    target_capital: float = 1_000_000.0,
) -> pd.DataFrame:
    """Calculate an illustrative monthly scenario from explicit user assumptions."""
    values = (starting_capital, monthly_deposit, monthly_roi_pct, target_capital)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Semua andaian mesti nombor terhingga.")
    if starting_capital < 0 or monthly_deposit < 0 or target_capital <= 0:
        raise ValueError("Modal/simpanan mesti bukan negatif dan sasaran mesti positif.")
    if monthly_roi_pct <= -100 or not 1 <= months <= 600:
        raise ValueError("Pulangan bulanan mesti melebihi -100% dan tempoh 1–600 bulan.")

    records = []
    balance = starting_capital
    principal = starting_capital
    rate = monthly_roi_pct / 100
    for month in range(1, months + 1):
        opening_balance = balance
        balance = (balance + monthly_deposit) * (1 + rate)
        principal += monthly_deposit
        records.append(
            {
                "Bulan": month,
                "Baki Awal (RM)": opening_balance,
                "Simpanan (RM)": monthly_deposit,
                "Pulangan Andaian (RM)": balance - opening_balance - monthly_deposit,
                "Baki Akhir (RM)": balance,
                "Jumlah Modal Disumbang (RM)": principal,
                "Perbezaan berbanding modal (RM)": balance - principal,
                "Kemajuan sasaran (%)": balance / target_capital * 100,
            }
        )
    return pd.DataFrame(records)


def render_milestone_tracker_ui(
    vault_data: dict | None = None,
    current_portfolio_value: float | None = None,
    fx_rate: float = 4.0773,
):
    if current_portfolio_value is None:
        current_portfolio_value = extract_portfolio_kpis(
            vault_data or {}, fx_rate=fx_rate
        ).get("active_portfolio_val")
    st.subheader("Unjuran sasaran kewangan")
    st.caption(
        "Simulasi matematik berasaskan input sendiri, bukan ramalan pulangan. "
        "Nilai permulaan daripada pegangan hanya meliputi data yang tersedia "
        "dalam snapshot."
    )
    with st.form("milestone_scenario_form"):
        starting_capital = st.number_input(
            "Nilai permulaan (RM; input atau pegangan snapshot)",
            min_value=0.0,
            value=max(float(current_portfolio_value or 0.0), 0.0),
            step=1000.0,
        )
        monthly_deposit = st.number_input(
            "Simpanan bulanan andaian (RM)",
            min_value=0.0,
            value=0.0,
            step=250.0,
        )
        monthly_return = st.number_input(
            "Pulangan bulanan andaian (%)",
            min_value=-99.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
        )
        target_capital = st.number_input(
            "Sasaran (RM)",
            min_value=1.0,
            value=1_000_000.0,
            step=10_000.0,
        )
        months = st.slider("Tempoh senario (bulan)", 1, 600, 60, step=1)
        submitted = st.form_submit_button("Kira senario", width="stretch")

    if not submitted:
        st.info("Tiada unjuran dibuat sehingga anda menghantar andaian.")
        return
    schedule = calculate_compounding_schedule(
        starting_capital=starting_capital,
        monthly_deposit=monthly_deposit,
        monthly_roi_pct=monthly_return,
        months=months,
        target_capital=target_capital,
    )
    final = schedule.iloc[-1]
    first, second, third = st.columns(3)
    first.metric("Baki akhir senario", f"RM {final['Baki Akhir (RM)']:,.2f}")
    second.metric("Jumlah modal disumbang", f"RM {final['Jumlah Modal Disumbang (RM)']:,.2f}")
    third.metric("Kemajuan sasaran", f"{final['Kemajuan sasaran (%)']:.1f}%")

    figure = go.Figure()
    figure.add_scatter(
        x=schedule["Bulan"],
        y=schedule["Baki Akhir (RM)"],
        mode="lines",
        name="Baki senario",
    )
    figure.add_hline(
        y=target_capital,
        line_dash="dash",
        annotation_text="Sasaran input",
    )
    figure.update_layout(
        title="Senario kompaun bulanan",
        xaxis_title="Bulan",
        yaxis_title="RM",
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
    )
    st.plotly_chart(
        figure,
        width="stretch",
        alt="Unjuran bulanan daripada andaian pengguna",
    )
    st.dataframe(
        schedule,
        width="stretch",
        hide_index=True,
        alt="Jadual senario kompaun bulanan",
    )
