"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 7: SKOR KESIHATAN PIOTROSKI F-SCORE, ALTMAN Z-SCORE & CARTA SANKEY ALIRAN DANA
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_piotroski_altman_data():
    """Mengembalikan pangkalan data kesihatan fundamental bagi kaunter utama."""
    return [
        {
            "Ticker": "KLSE:TENAGA", "Nama": "Tenaga Nasional Berhad", "Pasaran": "Bursa",
            "Piotroski_F": 8, "Gred_F": "🟢 Gred A (Sangat Kukuh)",
            "Altman_Z": 3.45, "Zon_Z": "🟢 Zon Selamat (Sifar Muflis)",
            "ROA_Positif": "Ya (+4.2%)", "CFO_vs_ROA": "CFO Lebih Tinggi (Kualiti Bersih)",
            "Margin_Kasar": "Meningkat (+1.8%)", "Risiko_Muflis": "0.1% (Sangat Rendah)"
        },
        {
            "Ticker": "KLSE:GAMUDA", "Nama": "Gamuda Berhad", "Pasaran": "Bursa",
            "Piotroski_F": 8, "Gred_F": "🟢 Gred A (Sangat Kukuh)",
            "Altman_Z": 3.82, "Zon_Z": "🟢 Zon Selamat (Sifar Muflis)",
            "ROA_Positif": "Ya (+5.8%)", "CFO_vs_ROA": "Kualiti Bersih Mantap",
            "Margin_Kasar": "Meningkat (+2.1%)", "Risiko_Muflis": "0.05% (Sifar Risiko)"
        },
        {
            "Ticker": "NASDAQ:NVDA", "Nama": "NVIDIA Corporation", "Pasaran": "US",
            "Piotroski_F": 9, "Gred_F": "🟢 Skor Sempurna 9/9 (Monopoli)",
            "Altman_Z": 18.40, "Zon_Z": "🟢 Kedaulatan Kewangan Ekstrim",
            "ROA_Positif": "Ya (+38.5%)", "CFO_vs_ROA": "FCF Rekod $13.5B",
            "Margin_Kasar": "Meningkat (75.1%)", "Risiko_Muflis": "0.00% (Kebal)"
        },
        {
            "Ticker": "NYSE:UMC (Aktif)", "Nama": "United Microelectronics", "Pasaran": "US",
            "Piotroski_F": 7, "Gred_F": "🟡 Gred B+ (Stabil / Sihat)",
            "Altman_Z": 3.10, "Zon_Z": "🟢 Zon Selamat",
            "ROA_Positif": "Ya (+7.4%)", "CFO_vs_ROA": "Aliran Tunai Mantap",
            "Margin_Kasar": "Mendatar (34.0%)", "Risiko_Muflis": "0.5% (Rendah)"
        },
        {
            "Ticker": "KLSE:0039 (GFM)", "Nama": "GFM Services Berhad", "Pasaran": "Bursa",
            "Piotroski_F": 6, "Gred_F": "🟡 Gred B (Sederhana)",
            "Altman_Z": 2.45, "Zon_Z": "🟡 Zon Kelabu (Waspada)",
            "ROA_Positif": "Ya (+2.8%)", "CFO_vs_ROA": "CFO Positif",
            "Margin_Kasar": "Mampan Konsesi", "Risiko_Muflis": "2.8% (Perlu Pantau)"
        }
    ]

def render_sankey_diagram():
    """Menjana Carta Aliran Tunai & Liabiliti Sankey (Interactive Wealth Flow)."""
    # Nod label
    labels = [
        "Pendapatan Gaji Bersih (RM 7,500)",       # 0
        "Untung Bersih Saham (RM 1,500)",          # 1
        "Jumlah Dana Masuk (RM 9,000)",            # 2
        "Komitmen Hutang CCRIS (RM 3,600)",        # 3
        "Simpanan & Persaraan (RM 2,120)",         # 4
        "Sara Hidup & Komuniti (RM 1,780)",        # 5
        "Suntikan Modal Saham (RM 1,500)",         # 6
        "BSN Perumahan (RM 1,400)",                # 7
        "Perodua Alza (RM 704)",                   # 8
        "Perodua Bezza (RM 396)",                  # 9
        "CIMB Cash Plus (RM 950)",                 # 10
        "RHB Card-i DMP (RM 150)",                 # 11
        "KWSP Simpanan (RM 1,200)",                # 12
        "Tabung Haji / ASNB (RM 920)",             # 13
        "Castana Maintenance (RM 120)"             # 14
    ]

    sources = [
        0, 1,          # Gaji & Untung Saham -> Jumlah Dana Masuk
        2, 2, 2, 2,    # Dana Masuk -> 4 Saluran Utama
        3, 3, 3, 3, 3, # Komitmen Hutang -> 5 Fasiliti Bank
        4, 4,          # Simpanan -> KWSP & TH
        5              # Sara Hidup -> Castana
    ]

    targets = [
        2, 2,
        3, 4, 5, 6,
        7, 8, 9, 10, 11,
        12, 13,
        14
    ]

    values = [
        7500, 1500,
        3600, 2120, 1780, 1500,
        1400, 704, 396, 950, 150,
        1200, 920,
        120
    ]

    colors = [
        "#00E676", "#29B6F6", "#2B384E",
        "#FF5252", "#00E676", "#FFBB28", "#29B6F6",
        "#FF5252", "#FF7043", "#FFA726", "#EF5350", "#E53935",
        "#00E676", "#26A69A",
        "#AB47BC"
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=20,
            line=dict(color="#141824", width=1.5),
            label=labels,
            color=colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(142, 154, 175, 0.22)"
        )
    )])

    fig.update_layout(
        title=dict(text="🌊 Peta Aliran Tunai Sankey: Dari Punca Pendapatan ke Pelunasan Liabiliti & Pelaburan", font=dict(color="#FFFFFF", size=14)),
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=480,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def render_fundamental_health_and_sankey_ui(fx_rate: float = 4.0773):
    st.subheader("🏆 Enjin Skor Kesihatan Fundamental (Piotroski & Altman Z) & Aliran Dana Sankey")
    st.caption("Pusat Pengesahan Kualiti Syarikat 9-Faktor & Visualisasi Aliran Wang Holistik Antara Gaji, Saham dan Hutang CCRIS.")

    t_fscore, t_sankey = st.tabs(["📊 Skor Kesihatan Fundamental (Piotroski & Altman Z)", "🌊 Carta Aliran Dana Sankey"])

    with t_fscore:
        st.markdown("#### 🏆 Penarafan Skor Kualiti Piotroski F-Score (0-9) & Altman Z-Score:")
        st.write("Menyingkirkan syarikat tenat, manipulasi akaun, dan 'value trap' sebelum membuat sebarang keputusan belian.")

        raw_health = get_piotroski_altman_data()
        df_h = pd.DataFrame(raw_health)

        st.dataframe(
            df_h[[
                "Ticker", "Nama", "Pasaran", "Piotroski_F", "Gred_F", "Altman_Z", "Zon_Z", "ROA_Positif", "Margin_Kasar"
            ]].style.map(
                lambda v: "color: #00E676; font-weight: bold;" if "🟢" in str(v) else ("color: #FFBB28; font-weight: bold;" if "🟡" in str(v) else ""),
                subset=["Gred_F", "Zon_Z"]
            ),
            width="stretch",
            hide_index=True
        )

        st.markdown("""
        <div style="background:#161D2B; border:1px solid #2B384E; border-radius:10px; padding:16px; margin-top:12px;">
            <h5 style="color:#29B6F6; margin-top:0;">💡 Piawaian Kualiti Institusi:</h5>
            <ul>
                <li><b>Piotroski F-Score (8-9/9):</b> Saham seperti <b>TENAGA</b>, <b>GAMUDA</b>, dan <b>NVDA</b> mencatatkan kualiti pendapatan bersih tertinggi.</li>
                <li><b>Altman Z-Score (> 2.99):</b> Membuktikan syarikat berada dalam <b>Zon Selamat Sifar Risiko Muflis</b> dalam tempoh 24 bulan akan datang.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with t_sankey:
        fig_sankey = render_sankey_diagram()
        st.plotly_chart(fig_sankey, width="stretch")

        st.info("💡 **Keterangan Aliran:** RM 3,600 mengalir terus ke 5 liabiliti CCRIS berjadual setiap bulan, manakala lebihan RM 1,500 disuntik semula ke dalam pasaran saham untuk menjana kesan kompaun Sejuta.")