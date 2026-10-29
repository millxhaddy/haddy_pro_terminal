"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL: PELAN SASARAN KEWANGAN SEJUTA (ROAD TO RM 1,000,000 MILESTONE TRACKER)
Unjuran Pengkompaunan Modal DDNK (Simpanan Tetap + Untung Dagangan Konsisten)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def calculate_compounding_schedule(
    starting_capital: float = 42497.80,
    monthly_deposit: float = 1000.0,
    monthly_roi_pct: float = 3.0,
    months: int = 60
) -> pd.DataFrame:
    """
    Menjana jadual unjuran pengkompaunan modal bulanan.
    """
    records = []
    current_balance = starting_capital
    cumulative_deposited = starting_capital
    
    rate = monthly_roi_pct / 100.0
    target_million = 1_000_000.0
    
    for m in range(1, months + 1):
        baki_awal = current_balance
        suntikan = monthly_deposit
        untung_dagangan = (baki_awal + suntikan) * rate
        baki_akhir = baki_awal + suntikan + untung_dagangan
        cumulative_deposited += suntikan
        pct_capai = (baki_akhir / target_million) * 100.0
        
        # Penentuan Fasa Batu Loncatan
        if baki_akhir >= 1_000_000:
            status_fasa = "🏆 BATU LONCATAN 4: SASARAN SEJUTA"
        elif baki_akhir >= 500_000:
            status_fasa = "💎 BATU LONCATAN 3: RM 500K"
        elif baki_akhir >= 250_000:
            status_fasa = "🚀 BATU LONCATAN 2: RM 250K"
        elif baki_akhir >= 100_000:
            status_fasa = "🏁 BATU LONCATAN 1: ASAS KUKUH (RM 100K)"
        else:
            status_fasa = "🌱 FASA MEMBINA"
            
        records.append({
            "Bulan": m,
            "Tahun": f"Tahun {(m - 1) // 12 + 1}",
            "Baki Awal (RM)": baki_awal,
            "Suntikan Simpanan (RM)": suntikan,
            "Untung Dagangan (RM)": untung_dagangan,
            "Baki Akhir (RM)": baki_akhir,
            "Modal Pokok Disuntik (RM)": cumulative_deposited,
            "Untung Bersih Kompaun (RM)": baki_akhir - cumulative_deposited,
            "% Capai Sejuta": pct_capai,
            "Status Batu Loncatan": status_fasa
        })
        current_balance = baki_akhir
        
    return pd.DataFrame(records)

def render_milestone_tracker_ui(vault_data: dict, current_net_capital: float = 42497.80):
    st.markdown("""
    <style>
        .milestone-badge {
            background: linear-gradient(135deg, #1A1F2C 0%, #111520 100%);
            border: 1px solid #2B384E;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .ddnk-principle {
            background-color: #161D2B;
            border-left: 4px solid #00E676;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 8px;
            font-size: 0.88rem;
            color: #E2E8F0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("🎯 Pelan Sasaran Kewangan Sejuta (Road to RM 1,000,000)")
    st.caption("Pelan Strategik Pengkompaunan Modal Pelaburan DDNK • Pantau Kemajuan Fasa, Lebihan Simpanan & Gandaan Untung")

    # ----------------------------------------------------------------------------------
    # 1. EMPAT KAD BATU LONCATAN (MILESTONE CARDS)
    # ----------------------------------------------------------------------------------
    target_cap = current_net_capital
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        pct_100k = min(target_cap / 100_000.0, 1.0)
        st.markdown(f"""
        <div class="milestone-badge" style="border-color:#29B6F6;">
            <small style="color:#29B6F6; font-weight:700;">🏁 BATU LONCATAN 1</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">RM 100,000</h3>
            <small style="color:#8E9AAF;">Sasaran: Bulan Ke-19</small>
            <div style="background:#222B3D; border-radius:10px; height:8px; margin-top:8px;">
                <div style="background:#29B6F6; width:{pct_100k*100:.1f}%; height:8px; border-radius:10px;"></div>
            </div>
            <small style="color:#29B6F6; font-weight:700;">Kemajuan: {target_cap/100000*100:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        pct_250k = min(target_cap / 250_000.0, 1.0)
        st.markdown(f"""
        <div class="milestone-badge" style="border-color:#00E676;">
            <small style="color:#00E676; font-weight:700;">🚀 BATU LONCATAN 2</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">RM 250,000</h3>
            <small style="color:#8E9AAF;">Sasaran: Bulan Ke-45</small>
            <div style="background:#222B3D; border-radius:10px; height:8px; margin-top:8px;">
                <div style="background:#00E676; width:{pct_250k*100:.1f}%; height:8px; border-radius:10px;"></div>
            </div>
            <small style="color:#00E676; font-weight:700;">Kemajuan: {target_cap/250000*100:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        pct_500k = min(target_cap / 500_000.0, 1.0)
        st.markdown(f"""
        <div class="milestone-badge" style="border-color:#FFBB28;">
            <small style="color:#FFBB28; font-weight:700;">💎 BATU LONCATAN 3</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">RM 500,000</h3>
            <small style="color:#8E9AAF;">Sasaran: Fasa Pertumbuhan</small>
            <div style="background:#222B3D; border-radius:10px; height:8px; margin-top:8px;">
                <div style="background:#FFBB28; width:{pct_500k*100:.1f}%; height:8px; border-radius:10px;"></div>
            </div>
            <small style="color:#FFBB28; font-weight:700;">Kemajuan: {target_cap/500000*100:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        pct_1m = min(target_cap / 1_000_000.0, 1.0)
        st.markdown(f"""
        <div class="milestone-badge" style="border-color:#E040FB;">
            <small style="color:#E040FB; font-weight:700;">🏆 BATU LONCATAN 4</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">RM 1,000,000</h3>
            <small style="color:#8E9AAF;">Matlamat Kebebasan Kewangan</small>
            <div style="background:#222B3D; border-radius:10px; height:8px; margin-top:8px;">
                <div style="background:#E040FB; width:{pct_1m*100:.1f}%; height:8px; border-radius:10px;"></div>
            </div>
            <small style="color:#E040FB; font-weight:700;">Kemajuan: {target_cap/1000000*100:.2f}%</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 2. PANEL INPUT PARAMETER DINAMIK
    # ----------------------------------------------------------------------------------
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        param_capital = st.number_input("Modal Permulaan Semasa (MYR):", value=float(current_net_capital), step=1000.0, format="%.2f")
    with col_p2:
        param_monthly_savings = st.number_input("Suntikan Simpanan Bulanan (MYR):", value=1000.0, step=250.0, format="%.2f")
    with col_p3:
        param_roi = st.slider("Sasaran Pulangan Bulanan Konsisten (% ROI):", 1.0, 8.0, 3.0, step=0.5, help="Sasaran realistik DDNK: 3% - 5% sebulan.")

    param_months = st.slider("Tempoh Unjuran (Bulan):", 24, 120, 60, step=12)

    # Jana Jadual Pengkompaunan
    df_schedule = calculate_compounding_schedule(
        starting_capital=param_capital,
        monthly_deposit=param_monthly_savings,
        monthly_roi_pct=param_roi,
        months=param_months
    )

    final_row = df_schedule.iloc[-1]

    # Kad Rumusan Pencapaian
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric(f"Baki Akhir (Bulan ke-{param_months})", f"RM {final_row['Baki Akhir (RM)']:,.2f}")
    with r2:
        st.metric("Jumlah Pokok Disuntik", f"RM {final_row['Modal Pokok Disuntik (RM)']:,.2f}")
    with r3:
        st.metric("Jumlah Untung Bersih Kompaun", f"RM {final_row['Untung Bersih Kompaun (RM)']:,.2f}", f"+{(final_row['Untung Bersih Kompaun (RM)']/final_row['Modal Pokok Disuntik (RM)']*100):.1f}% Gandaan")
    with r4:
        st.metric("Kemajuan Capai Sejuta", f"{final_row['% Capai Sejuta']:.1f}%", f"Baki: RM {max(1_000_000 - final_row['Baki Akhir (RM)'], 0):,.0f}")

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 3. CARTA KAWASAN PENGKOMPAUNAN MODAL (COMPOUNDING AREA CHART)
    # ----------------------------------------------------------------------------------
    st.subheader("📈 Trajektori Pertumbuhan Modal: Pokok Disuntik vs Untung Kompaun Terkumpul")

    fig_comp = go.Figure()

    fig_comp.add_trace(go.Scatter(
        x=df_schedule["Bulan"],
        y=df_schedule["Modal Pokok Disuntik (RM)"],
        mode="lines",
        name="Modal Sendiri Disuntik (Pokok)",
        line=dict(color="#29B6F6", width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(41, 182, 246, 0.15)",
        hovertemplate="Bulan %{x}: Pokok <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    fig_comp.add_trace(go.Scatter(
        x=df_schedule["Bulan"],
        y=df_schedule["Baki Akhir (RM)"],
        mode="lines",
        name="Nilai Portfolio Berganda (Pokok + Kompaun)",
        line=dict(color="#00E676", width=3.5, shape="spline"),
        fill="tonexty",
        fillcolor="rgba(0, 230, 118, 0.25)",
        hovertemplate="Bulan %{x}: Jumlah Portfolio <b>RM %{y:,.2f}</b><extra></extra>"
    ))

    # Garisan Sasaran Batu Loncatan
    fig_comp.add_hline(y=100_000, line_dash="dot", line_color="#29B6F6", annotation_text="RM 100K (Asas Kukuh)", annotation_position="top left")
    fig_comp.add_hline(y=250_000, line_dash="dot", line_color="#00E676", annotation_text="RM 250K (Skala Besar)", annotation_position="top left")
    fig_comp.add_hline(y=500_000, line_dash="dot", line_color="#FFBB28", annotation_text="RM 500K (Fasa Pecutan)", annotation_position="top left")
    fig_comp.add_hline(y=1_000_000, line_dash="dash", line_color="#E040FB", annotation_text="RM 1,000,000 (SASARAN SEJUTA)", annotation_position="top left")

    fig_comp.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=450,
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(title="Bulan Unjuran", gridcolor="#222B3D"),
        yaxis=dict(title="Nilai Portfolio (MYR)", gridcolor="#222B3D", tickprefix="RM "),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, width="stretch")

    st.markdown("---")

    # ----------------------------------------------------------------------------------
    # 4. JADUAL UNJURAN BULANAN & PRINSIP DDNK
    # ----------------------------------------------------------------------------------
    col_tbl, col_law = st.columns([7, 3])

    with col_tbl:
        st.subheader("📋 Jadual Unjuran Pengkompaunan Bulanan")
        st.dataframe(
            df_schedule[[
                "Bulan", "Baki Awal (RM)", "Suntikan Simpanan (RM)", "Untung Dagangan (RM)", 
                "Baki Akhir (RM)", "% Capai Sejuta", "Status Batu Loncatan"
            ]].style.format({
                "Baki Awal (RM)": "RM {:,.2f}",
                "Suntikan Simpanan (RM)": "RM {:,.2f}",
                "Untung Dagangan (RM)": "RM {:,.2f}",
                "Baki Akhir (RM)": "RM {:,.2f}",
                "% Capai Sejuta": "{:.1f}%"
            }),
            width="stretch",
            hide_index=True
        )

    with col_law:
        st.subheader("💡 5 Prinsip Pengkompaunan DDNK")
        st.markdown("""
        <div class="ddnk-principle">
            <b>1. Kawal Risiko & Disiplin Stop Loss (1.5% - 2.0%)</b><br>
            Lindungi modal daripada kejatuhan besar supaya kesan gandaan tidak terputus.
        </div>
        <div class="ddnk-principle">
            <b>2. Pulangan Konsisten Bulanan (Sasaran 3% - 5%)</b><br>
            Jangan kejar keuntungan 100% semalaman; konsisten 3% sebulan melipatgandakan modal secara eksponen.
        </div>
        <div class="ddnk-principle">
            <b>3. Suntikan Simpanan Tetap Membina Snowball</b><br>
            Suntikan RM 1,000 setiap bulan mempercepatkan fasa awal pembinaan portfolio.
        </div>
        <div class="ddnk-principle">
            <b>4. Sabar Menghadapi Fasa Pembinaan (Mind 60%)</b><br>
            Tahun pertama adalah fasa paling perlahan. Jangan putus asa semasa modal bawah RM 100K.
        </div>
        <div class="ddnk-principle">
            <b>5. Fasa Pecutan Bermula Selepas RM 100K</b><br>
            Kesan pengkompaunan mula berganda laju apabila baki portfolio melepasi RM 100,000.
        </div>
        """, unsafe_allow_html=True)
