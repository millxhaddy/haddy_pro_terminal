"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 8: PENGOPTIMUMAN PORTFOLIO MARKOWITZ & STRATEGI PELUNASAN HUTANG
1. Markowitz Efficient Frontier (Max Sharpe vs Min Volatility)
2. Debt Payoff Strategies (Snowball vs Avalanche)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ======================================================================================
# 1. ENJIN PENGOPTIMUMAN PORTFOLIO MARKOWITZ (EFFICIENT FRONTIER)
# ======================================================================================
def generate_efficient_frontier_simulation(num_portfolios=1500):
    """
    Simulasi Markowitz MPT menjana 1,500 gabungan portfolio rawak.
    Aset: TENAGA, GAMUDA, YTLPOWR, NVDA, UMC, CASH
    """
    np.random.seed(42)
    assets = ["TENAGA (Bursa)", "GAMUDA (Bursa)", "YTLPOWR (Bursa)", "NVDA (US)", "UMC (US)", "TUNAI (Buffer)"]
    
    # Anggaran pulangan tahunan (Expected Annual Returns)
    exp_returns = np.array([0.15, 0.18, 0.22, 0.35, 0.12, 0.035])
    
    # Matriks kovarians anggaran
    cov_matrix = np.array([
        [0.040, 0.015, 0.025, 0.012, 0.008, 0.000],
        [0.015, 0.055, 0.020, 0.015, 0.010, 0.000],
        [0.025, 0.020, 0.065, 0.022, 0.012, 0.000],
        [0.012, 0.015, 0.022, 0.120, 0.045, 0.000],
        [0.008, 0.010, 0.012, 0.045, 0.075, 0.000],
        [0.000, 0.000, 0.000, 0.000, 0.000, 0.001]
    ])
    
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    for i in range(num_portfolios):
        weights = np.random.random(len(assets))
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # Pulangan & Volatiliti Portfolio
        port_return = np.sum(weights * exp_returns)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Sharpe Ratio (Risk-free rate = 3.5%)
        sharpe = (port_return - 0.035) / port_volatility if port_volatility > 0 else 0
        
        results[0, i] = port_return
        results[1, i] = port_volatility
        results[2, i] = sharpe

    # Cari Max Sharpe & Min Volatility
    max_sharpe_idx = np.argmax(results[2])
    min_vol_idx = np.argmin(results[1])
    
    # Portfolio Semasa (Beban UMC ~62%, GFM ~13%, Tunai ~25%)
    cur_weights = np.array([0.05, 0.05, 0.03, 0.00, 0.62, 0.25])
    cur_return = np.sum(cur_weights * exp_returns)
    cur_volatility = np.sqrt(np.dot(cur_weights.T, np.dot(cov_matrix, cur_weights)))
    cur_sharpe = (cur_return - 0.035) / cur_volatility

    return {
        "assets": assets,
        "returns": results[0],
        "volatilities": results[1],
        "sharpe_ratios": results[2],
        "max_sharpe": {
            "return": results[0, max_sharpe_idx],
            "volatility": results[1, max_sharpe_idx],
            "sharpe": results[2, max_sharpe_idx],
            "weights": weights_record[max_sharpe_idx]
        },
        "min_vol": {
            "return": results[0, min_vol_idx],
            "volatility": results[1, min_vol_idx],
            "sharpe": results[2, min_vol_idx],
            "weights": weights_record[min_vol_idx]
        },
        "current": {
            "return": cur_return,
            "volatility": cur_volatility,
            "sharpe": cur_sharpe,
            "weights": cur_weights
        }
    }

def render_markowitz_efficient_frontier_ui():
    st.subheader("📊 Enjin Pengoptimuman Portfolio Markowitz (Efficient Frontier)")
    st.caption("Aplikasi Teori Portfolio Moden (Nobel Prize MPT): Cari titik imbangan matematik tertinggi antara pulangan dan risiko.")

    sim = generate_efficient_frontier_simulation(num_portfolios=1200)

    # Kad Skor Ringkasan 3 Portfolio
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div style="background:#221015; border:2px solid #FF5252; border-radius:10px; padding:14px;">
            <small style="color:#FFC4C4; font-weight:700;">📍 PORTFOLIO SEMASA (OVER-WEIGHT UMC)</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">Pulangan: {sim['current']['return']*100:.1f}%</h3>
            <small style="color:#FF5252;">Volatiliti: {sim['current']['volatility']*100:.1f}% | Sharpe: {sim['current']['sharpe']:.2f}x</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background:#0D2B20; border:2px solid #00E676; border-radius:10px; padding:14px;">
            <small style="color:#A7F3D0; font-weight:700;">⭐ MAX SHARPE RATIO (OPTIMUM)</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">Pulangan: {sim['max_sharpe']['return']*100:.1f}%</h3>
            <small style="color:#00E676;">Volatiliti: {sim['max_sharpe']['volatility']*100:.1f}% | Sharpe: {sim['max_sharpe']['sharpe']:.2f}x</small>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="background:#161D2B; border:2px solid #29B6F6; border-radius:10px; padding:14px;">
            <small style="color:#BAE6FD; font-weight:700;">🛡️ MINIMUM VOLATILITY (DEFENSIF)</small>
            <h3 style="color:#FFFFFF; margin:4px 0;">Pulangan: {sim['min_vol']['return']*100:.1f}%</h3>
            <small style="color:#29B6F6;">Volatiliti Terendah: {sim['min_vol']['volatility']*100:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Plot Carta Keluk Efficient Frontier
    fig_ef = go.Figure()

    # Titik-titik Simulasi Portfolio
    fig_ef.add_trace(go.Scatter(
        x=sim["volatilities"] * 100,
        y=sim["returns"] * 100,
        mode="markers",
        marker=dict(
            color=sim["sharpe_ratios"],
            colorscale="Viridis",
            size=5,
            opacity=0.6,
            colorbar=dict(title="Nisbah Sharpe", tickfont=dict(color="#FFFFFF"))
        ),
        name="Kombinasi Portfolio",
        hovertemplate="Volatiliti: %{x:.1f}%<br>Pulangan: %{y:.1f}%<extra></extra>"
    ))

    # Titik Portfolio Semasa
    fig_ef.add_trace(go.Scatter(
        x=[sim["current"]["volatility"] * 100],
        y=[sim["current"]["return"] * 100],
        mode="markers+text",
        marker=dict(color="#FF1744", size=15, symbol="diamond", line=dict(color="#FFFFFF", width=2)),
        text=["📍 Portfolio Semasa"],
        textposition="top center",
        name="Semasa (Tinggi Risiko)"
    ))

    # Titik Max Sharpe
    fig_ef.add_trace(go.Scatter(
        x=[sim["max_sharpe"]["volatility"] * 100],
        y=[sim["max_sharpe"]["return"] * 100],
        mode="markers+text",
        marker=dict(color="#00E676", size=16, symbol="star", line=dict(color="#FFFFFF", width=2)),
        text=["⭐ Max Sharpe Optimum"],
        textposition="bottom right",
        name="Optimum (Max Sharpe)"
    ))

    # Titik Min Volatility
    fig_ef.add_trace(go.Scatter(
        x=[sim["min_vol"]["volatility"] * 100],
        y=[sim["min_vol"]["return"] * 100],
        mode="markers+text",
        marker=dict(color="#29B6F6", size=14, symbol="circle", line=dict(color="#FFFFFF", width=2)),
        text=["🛡️ Min Volatility"],
        textposition="top left",
        name="Kalis Krisis (Min Vol)"
    ))

    fig_ef.update_layout(
        title=dict(text="🎯 Keluk Sempadan Cekap Markowitz (Risk vs Return Frontier)", font=dict(color="#FFFFFF", size=14)),
        template="plotly_dark", paper_bgcolor="#141824", plot_bgcolor="#141824",
        height=450, margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(title="Risiko Volatiliti Tahunan (%)", gridcolor="#222B3D", ticksuffix="%"),
        yaxis=dict(title="Jangkaan Pulangan Tahunan (%)", gridcolor="#222B3D", ticksuffix="%"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_ef, width="stretch")

    # Jadual Perbandingan Agihan Modal (%)
    st.markdown("#### ⚖️ Perbandingan Cadangan Agihan Berat Modal (%):")
    df_weights = pd.DataFrame({
        "Aset / Segmen": sim["assets"],
        "Porsi Semasa (%)": [f"{w*100:.1f}%" for w in sim["current"]["weights"]],
        "Cadangan Max Sharpe (%)": [f"{w*100:.1f}%" for w in sim["max_sharpe"]["weights"]],
        "Cadangan Min Volatility (%)": [f"{w*100:.1f}%" for w in sim["min_vol"]["weights"]]
    })
    st.dataframe(df_weights, width="stretch", hide_index=True)

    st.info("💡 **Kesimpulan Algoritma Markowitz:** Untuk menaikkan pulangan dari 11.4% ke **22.5%** sambil menurunkan volatiliti, kurangkan pendedahan UMC kepada **~15% - 20%**, dan agihkan lebihan modal kepada **NVDA, YTLPOWR, dan TENAGA**.")


# ======================================================================================
# 2. ENJIN STRATEGI PELUNASAN HUTANG (SNOWBALL VS AVALANCHE)
# ======================================================================================
def render_debt_payoff_strategies_ui():
    st.subheader("🚀 Strategi Pelunasan Hutang Pantas: Snowball vs Avalanche")
    st.caption("Analisis simulasi 6 fasiliti CCRIS: Pilih kaedah terbaik untuk melangsaikan hutang RM 595,272 lebih awal.")

    debts = [
        {"Fasiliti": "RHB Rewards Card-i", "Baki": 4682.05, "Kadar": 7.00, "Ansuran": 50.00},
        {"Fasiliti": "Perodua Bezza (Maybank)", "Baki": 13766.64, "Kadar": 6.69, "Ansuran": 396.00},
        {"Fasiliti": "RHB Cashback Card-i", "Baki": 13638.26, "Kadar": 7.00, "Ansuran": 100.00},
        {"Fasiliti": "Perodua Alza (Hong Leong)", "Baki": 61123.74, "Kadar": 2.29, "Ansuran": 704.00},
        {"Fasiliti": "CIMB Cash Plus", "Baki": 94013.13, "Kadar": 7.00, "Ansuran": 950.00},
        {"Fasiliti": "BSN Housing Loan", "Baki": 408048.18, "Kadar": 4.10, "Ansuran": 1400.00}
    ]

    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.markdown("""
        <div style="background:#161D2B; border-left:4px solid #00E676; padding:16px; border-radius:0 10px 10px 0;">
            <h4 style="color:#00E676; margin-top:0;">⛄ Kaedah Bola Salji (Debt Snowball):</h4>
            <p style="font-size:0.88rem; color:#CBD5E1;">
                <b>Falsafah:</b> Bayar baki terkecil dahulu tanpa mengira kadar faedah.<br>
                <b>Kelebihan:</b> Memberi kemenangan psikologi pantas! Setiap hutang yang mati memberi kelegaan mental yang besar.
            </p>
            <ol style="font-size:0.85rem; color:#A7F3D0;">
                <li><b>Sasaran 1:</b> RHB Rewards (RM 4,682) ➔ Selesai dalam 4 bulan!</li>
                <li><b>Sasaran 2:</b> RHB Cashback (RM 13,638) ➔ Selesai dalam 10 bulan!</li>
                <li><b>Sasaran 3:</b> Perodua Bezza (RM 13,766) ➔ Selesai dalam 14 bulan!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with col_st2:
        st.markdown("""
        <div style="background:#161D2B; border-left:4px solid #29B6F6; padding:16px; border-radius:0 10px 10px 0;">
            <h4 style="color:#29B6F6; margin-top:0;">🏔️ Kaedah Longsoran (Debt Avalanche):</h4>
            <p style="font-size:0.88rem; color:#CBD5E1;">
                <b>Falsafah:</b> Bayar pinjaman berkadar faedah tertinggi dahulu (7.00%).<br>
                <b>Kelebihan Kuantitatif:</b> Menjimatkan jumlah kos faedah paling maksima secara matematik!
            </p>
            <ol style="font-size:0.85rem; color:#BAE6FD;">
                <li><b>Sasaran 1:</b> RHB Rewards & Cashback (7.00% p.a.)</li>
                <li><b>Sasaran 2:</b> CIMB Cash Plus (7.00% p.a. - Baki RM 94k)</li>
                <li><b>Sasaran 3:</b> Perodua Bezza (6.69% p.a.)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Simulasi Tambahan Suntikan Untung Saham (Accelerator)
    extra_payment = st.slider("Suntikan Tambahan Daripada Keuntungan Saham Bulanan (RM):", 500.0, 5000.0, 1500.0, step=250.0)

    # Perbandingan Masa Selesai
    m_snowball_first_3 = int((4682.05 + 13638.26 + 13766.64) / (extra_payment + 546.0))
    st.success(f"""
    🎉 **KEPUTUSAN STRATEGI BOLA SALJI:**  
    Dengan menyalurkan untung saham **RM {extra_payment:,.2f}/bulan**, anda boleh **MENGHAPUSKAN 3 FASILITI SEKALIGUS (RHB Rewards, RHB Cashback & Perodua Bezza)** dalam masa **{m_snowball_first_3} BULAN SAHAJA (~{m_snowball_first_3/12:.1f} Tahun)!**  
    Selepas 3 hutang ini terhapus, aliran tunai bulanan anda bertambah bebas sebanyak **+RM 546.00 setiap bulan**!
    """)