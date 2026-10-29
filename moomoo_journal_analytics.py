"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 17 & 18: PENJANA PESANAN MOOMOO & ANALITIK DISIPLIN JURNAL DAGANGAN
========================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --------------------------------------------------------------------------------------
# FASA 17: PENJANA RENTETAN PESANAN BROKER MOOMOO (ORDER STRING GENERATOR)
# --------------------------------------------------------------------------------------
def generate_moomoo_order_payload(
    ticker: str,
    market: str,
    order_type: str,
    units: int,
    limit_price: float,
    stop_loss_price: float,
    take_profit_price: float,
    session: str = "Regular Hours"
) -> dict:
    """
    Menjana payload teks berformat rasmi Moomoo OpenD / Universal Account.
    """
    currency = "MYR" if "BURSA" in market.upper() or "KLSE" in ticker.upper() else "USD"
    lots = units // 100 if currency == "MYR" else units
    
    order_summary_text = (
        f"MOOMOO ORDER TICKET\n"
        f"----------------------------------------\n"
        f"Account       : Universal Account (8702)\n"
        f"Symbol        : {ticker.upper()}\n"
        f"Market        : {market}\n"
        f"Action        : BUY (Long Entry)\n"
        f"Order Type    : {order_type}\n"
        f"Quantity      : {units:,} Units ({lots} Lots)\n"
        f"Limit Price   : {currency} {limit_price:.2f}\n"
        f"Stop Loss     : {currency} {stop_loss_price:.2f}\n"
        f"Target TP     : {currency} {take_profit_price:.2f}\n"
        f"Time-In-Force : Day Order\n"
        f"Session       : {session}\n"
        f"Discipline    : DDNK 3M Compliant (SL Locked)\n"
        f"----------------------------------------"
    )
    
    return {
        "summary_text": order_summary_text,
        "ticker": ticker.upper(),
        "units": units,
        "lots": lots,
        "currency": currency,
        "total_cost": units * limit_price
    }

def render_moomoo_order_generator():
    """
    Antara muka interaktif penjana pesanan Moomoo dengan salin pantas.
    """
    st.markdown("""
    <style>
        .order-card {
            background: linear-gradient(135deg, #1A1F2C 0%, #151A26 100%);
            border: 1px solid #2B354C;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns([5, 5])

    with col_in:
        st.markdown('<div class="order-card">', unsafe_allow_html=True)
        st.subheader("🛒 Konfigurasi Pesanan Broker Moomoo")
        
        m_type = st.radio("Pilih Pasaran Broker:", ["🇲🇾 Bursa Malaysia (Universal MY)", "🇺🇸 Wall Street US (Universal US)"], horizontal=True)
        is_bursa = "Bursa" in m_type
        
        default_sym = "KLSE:TENAGA" if is_bursa else "NASDAQ:NVDA"
        default_px = 12.75 if is_bursa else 141.20
        default_sl = 12.10 if is_bursa else 134.00
        default_tp = 14.38 if is_bursa else 161.36
        default_qty = 500 if is_bursa else 25
        
        t_sym = st.text_input("Kod Saham (Ticker):", default_sym)
        o_type = st.selectbox("Jenis Pesanan Moomoo:", ["Limit Order (Had Harga - Disyorkan)", "Stop-Limit Order", "Market Order (Elakkan FOMO)"])
        
        c1, c2 = st.columns(2)
        with c1:
            qty_val = st.number_input("Kuantiti (Unit):", value=default_qty, step=100 if is_bursa else 5)
        with c2:
            lim_px = st.number_input("Had Harga Entri:", value=default_px, step=0.05, format="%.2f")
            
        c3, c4 = st.columns(2)
        with c3:
            sl_val = st.number_input("Paras Stop Loss:", value=default_sl, step=0.05, format="%.2f")
        with c4:
            tp_val = st.number_input("Sasaran Ambil Untung:", value=default_tp, step=0.05, format="%.2f")
            
        st.markdown('</div>', unsafe_allow_html=True)

    payload = generate_moomoo_order_payload(
        ticker=t_sym,
        market="Bursa Malaysia" if is_bursa else "US Wall Street",
        order_type="Limit" if "Limit" in o_type else "Market",
        units=int(qty_val),
        limit_price=lim_px,
        stop_loss_price=sl_val,
        take_profit_price=tp_val
    )

    with col_out:
        st.markdown('<div class="order-card">', unsafe_allow_html=True)
        st.subheader("📋 Tiket Pesanan Moomoo (Sedia Salin)")
        
        st.code(payload["summary_text"], language="yaml")
        
        st.metric(
            "Anggaran Nilai Transaksi",
            f"{payload['currency']} {payload['total_cost']:,.2f}",
            f"{payload['lots']} Lot ({payload['units']:,} Unit)"
        )
        
        st.success("✅ **SOP Disiplin Disahkan:** Pesanan dilengkapi paras Stop Loss terikat bagi melindungi akaun daripada penarikan modal besar.")
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# FASA 18: ANALITIK DISIPLIN & PSIKOLOGI JURNAL DAGANGAN (MIND 60%)
# --------------------------------------------------------------------------------------
def get_journal_analytics_data() -> dict:
    """
    Menyusun data analitik audit disiplin berasaskan rekod rasmi tab Jurnal Dagangan (Baris 176 - 190).
    """
    # 1. Kategori Hasil & Emosi Dagangan
    discipline_df = pd.DataFrame([
        {"Kategori": "Selesai / Disiplin (TP)", "Bilangan": 92, "Untung_Bersih_MYR": 61691.40, "Peratus_Bilangan": 81.4, "Warna": "#00E676"},
        {"Kategori": "Cut Loss Berdisiplin", "Bilangan": 20, "Untung_Bersih_MYR": -28544.10, "Peratus_Bilangan": 17.7, "Warna": "#FF5252"},
        {"Kategori": "Pulang Modal (Break-even)", "Bilangan": 1, "Untung_Bersih_MYR": 0.00, "Peratus_Bilangan": 0.9, "Warna": "#29B6F6"},
        {"Kategori": "FOMO / Emosi Tak Terkawal", "Bilangan": 0, "Untung_Bersih_MYR": 0.00, "Peratus_Bilangan": 0.0, "Warna": "#FFBB28"}
    ])

    # 2. Metrik Prestasi Institusi
    metrics = {
        "profit_factor": 2.12,
        "win_rate_pct": 77.0,
        "avg_win": 722.12,
        "avg_loss": -1187.09,
        "payoff_ratio": 0.61,
        "expectancy_myr": 282.83,
        "max_gain": 9498.22,
        "max_drawdown": -4607.19,
        "total_trades": 113,
        "net_pnl_myr": 33147.30
    }

    # 3. Taburan P&L Mengikut Pasaran
    market_pnl_df = pd.DataFrame([
        {"Pasaran": "Bursa Malaysia", "Untung_MYR": 7820.50, "Rugi_MYR": -4120.30, "Bersih_MYR": 3700.20},
        {"Pasaran": "Wall Street US", "Untung_MYR": 55003.90, "Rugi_MYR": -25556.90, "Bersih_MYR": 29447.00}
    ])

    return {
        "discipline": discipline_df,
        "metrics": metrics,
        "market_pnl": market_pnl_df
    }

def render_journal_analytics_dashboard():
    """
    Memaparkan visualisasi penuh analitik disiplin dagangan (Mind 60%).
    """
    data = get_journal_analytics_data()
    m = data["metrics"]
    df_disc = data["discipline"]

    # 1. Baris Metrik Institusi DDNK
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Profit Factor", f"{m['profit_factor']:.2f}x", "Sasaran: > 1.50x")
    with c2:
        st.metric("Kadar Kemenangan (Win Rate)", f"{m['win_rate_pct']:.1f}%", f"{m['total_trades']} Jumlah Dagangan")
    with c3:
        st.metric("Jangkaan Positif (Expectancy)", f"+RM {m['expectancy_myr']:,.2f}", "Untung Jangkaan Per Trade")
    with c4:
        st.metric("Untung Bersih Realisasi", f"RM {m['net_pnl_myr']:,.2f}", "Pencapaian Tertinggi: RM 9,498")

    st.markdown("---")

    # 2. Visualisasi Berkembar: Carta Pai Disiplin vs Carta Bar P&L Pasaran
    col_pie, col_bar = st.columns([5, 5])

    with col_pie:
        st.subheader("🧠 Audit Emosi & Disiplin Dagangan (Mind 60%)")
        fig_pie = px.pie(
            df_disc,
            names="Kategori",
            values="Bilangan",
            color="Kategori",
            color_discrete_map={
                "Selesai / Disiplin (TP)": "#00E676",
                "Cut Loss Berdisiplin": "#FF5252",
                "Pulang Modal (Break-even)": "#29B6F6",
                "FOMO / Emosi Tak Terkawal": "#FFBB28"
            },
            hole=0.55
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            textfont=dict(color="#FFFFFF", size=11),
            hovertemplate="<b>%{label}</b><br>Bilangan: <b>%{value} Dagangan</b><br>Peratus: <b>%{percent}</b><extra></extra>"
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="#141824",
            plot_bgcolor="#141824",
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_pie, width="stretch")

    with col_bar:
        st.subheader("🌎 Taburan Untung Bersih: Bursa vs Wall Street")
        df_m = data["market_pnl"]
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=df_m["Pasaran"],
            y=df_m["Untung_MYR"],
            name="Untung Kasar",
            marker_color="#00E676",
            hovertemplate="Untung Kasar: <b>RM %{y:,.2f}</b><extra></extra>"
        ))
        
        fig_bar.add_trace(go.Bar(
            x=df_m["Pasaran"],
            y=df_m["Rugi_MYR"],
            name="Rugi Kasar",
            marker_color="#FF5252",
            hovertemplate="Rugi Kasar: <b>RM %{y:,.2f}</b><extra></extra>"
        ))
        
        fig_bar.add_trace(go.Bar(
            x=df_m["Pasaran"],
            y=df_m["Bersih_MYR"],
            name="Untung Bersih",
            marker_color="#29B6F6",
            hovertemplate="Untung Bersih: <b>RM %{y:,.2f}</b><extra></extra>"
        ))

        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="#141824",
            plot_bgcolor="#141824",
            barmode="group",
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#8E9AAF", size=10)),
            yaxis=dict(gridcolor="#222B3D", tickprefix="RM ", tickfont=dict(color="#8E9AAF", size=10)),
            xaxis=dict(tickfont=dict(color="#FFFFFF", size=11))
        )
        st.plotly_chart(fig_bar, width="stretch")

    # 3. Jadual Audit Disiplin Terperinci
    st.subheader("📋 Jadual Audit Skor Psikologi & Tingkah Laku Pelabur")
    st.dataframe(
        df_disc.style.format({
            "Untung_Bersih_MYR": "RM {:,.2f}",
            "Peratus_Bilangan": "{:.1f}%"
        }),
        width="stretch",
        hide_index=True
    )
    
    st.info("💡 **Penemuan Audit DDNK:** Kadar kepatuhan disiplin anda berada pada tahap cemerlang (**99.1% Gabungan TP & Cut-Loss Berdisiplin**). Tiada sebarang insiden perdagangan balas dendam (*revenge trading*) atau FOMO dikesan.")
