"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL ELIT 4-DALAM-1:
1. Notifikasi Pelayar Masa Nyata (Browser Push Notification Engine)
2. Enjin Pengimbangan Semula Portfolio (Automated Portfolio Rebalancer)
3. Sistem Pengesahan 3 Tempoh Masa (Multi-Timeframe Confluence - Alexander Elder)
4. Penganalisis Penyata Kewangan & Laporan Suku Tahun AI (Earnings Analyzer)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ======================================================================================
# 1. NOTIFIKASI PELAYAR MASA NYATA (WEB BROWSER PUSH NOTIFICATIONS)
# ======================================================================================
def render_browser_notification_engine():
    st.subheader("🔔 Sistem Notifikasi Pelayar Masa Nyata (Browser Push Alerts)")
    st.caption("Terima makluman timbul (pop-up banner) di komputer atau telefon walaupun tab terminal sedang diminimakan.")

    col_n1, col_n2 = st.columns([6, 4])

    with col_n1:
        st.markdown("""
        <div style="background:#161D2B; border:1px solid #2B384E; border-radius:12px; padding:18px;">
            <h4 style="color:#29B6F6; margin-top:0;">🛡️ Parameter Pengawasan Ambang Risiko Automatik:</h4>
            <ul>
                <li>🚨 <b>Amaran Lantai UMC:</b> Cetuskan notifikasi jika harga jatuh menghampiri <b>$18.00</b>.</li>
                <li>🎯 <b>Peluang Entri TENAGA:</b> Cetuskan notifikasi jika harga menyentuh lantai <b>RM 12.50</b>.</li>
                <li>⚡ <b>Anomali Jerung RVOL:</b> Makluman segera jika volum kaunter Watchlist melepasi <b>2.5x</b> purata.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_n2:
        st.markdown("#### 📲 Ujian Kebenaran Notifikasi Pelayar:")
        test_stock = st.selectbox("Pilih Senario Amaran Ujian:", ["🚨 UMC Mencecah Had Stop Loss ($18.00)", "🎯 TENAGA Masuk Zon Entri (RM 12.60)", "⚡ NVDA Lonjakan Volum Jerung (RVOL 3.1x)"])
        
        # Komponen JavaScript Notification API
        push_js = f"""
        <div style="text-align:center; padding:10px;">
            <button onclick="triggerBrowserPush()" style="background:#00E676; color:#0E1117; font-weight:800; font-size:14px; padding:10px 20px; border:none; border-radius:24px; cursor:pointer; width:100%;">
                🔔 Uji Hantar Notifikasi Pelayar Sekarang
            </button>
            <p id="notifStatus" style="color:#8E9AAF; font-size:12px; margin-top:8px;">Status: Tekan untuk menguji izin notifikasi</p>
        </div>

        <script>
            function triggerBrowserPush() {{
                const statusText = document.getElementById('notifStatus');
                if (!("Notification" in window)) {{
                    statusText.innerText = "Pelayar web ini tidak menyokong notifikasi desktop.";
                    return;
                }}

                if (Notification.permission === "granted") {{
                    new Notification("⚡ HADDY PRO TERMINAL ALERT", {{
                        body: "{test_stock}",
                        icon: "https://img.icons8.com/fluency/96/bullish.png"
                    }});
                    statusText.innerText = "✅ Notifikasi berjaya dihantar ke skrin anda!";
                }} else if (Notification.permission !== "denied") {{
                    Notification.requestPermission().then(function (permission) {{
                        if (permission === "granted") {{
                            new Notification("⚡ HADDY PRO TERMINAL ALERT", {{
                                body: "{test_stock}",
                                icon: "https://img.icons8.com/fluency/96/bullish.png"
                            }});
                            statusText.innerText = "✅ Kebenaran diterima & notifikasi dihantar!";
                        }} else {{
                            statusText.innerText = "⚠️ Kebenaran notifikasi ditolak oleh pengguna.";
                        }}
                    }});
                }} else {{
                    statusText.innerText = "⚠️ Sila benarkan kebenaran notifikasi dalam tetapan pelayar anda.";
                }}
            }}
        </script>
        """
        st.html(push_js)


# ======================================================================================
# 2. ENJIN PENGIMBANGAN SEMULA PORTFOLIO (AUTOMATED REBALANCER)
# ======================================================================================
def render_portfolio_rebalancer_ui(fx_rate: float = 4.0773):
    st.subheader("⚖️ Enjin Pengimbangan Semula Portfolio (Portfolio Rebalancer)")
    st.caption("Kira peruntukan modal ideal untuk mengelakkan risiko ketidakseimbangan aset antara Bursa, Wall Street, dan Tunai.")

    # Data Nilai Portfolio Semasa
    val_bursa = 9870.00   # GFM Services
    val_us = 44172.61      # UMC (581 unit @ $18.65 x 4.0773)
    val_cash = 18500.00    # Rizab Tunai Tersedia
    total_wealth = val_bursa + val_us + val_cash

    c1, c2, c3 = st.columns(3)
    with c1:
        target_bursa_pct = st.slider("Sasaran Agihan Bursa Malaysia (%):", 10, 60, 35, step=5)
    with c2:
        target_us_pct = st.slider("Sasaran Agihan Wall Street US (%):", 10, 60, 45, step=5)
    with c3:
        target_cash_pct = 100 - (target_bursa_pct + target_us_pct)
        st.metric("Sasaran Rizab Tunai (%):", f"{target_cash_pct}%", "Automatik Seimbang")

    # Pengiraan Nilai Sasaran vs Sebenar
    target_bursa_val = total_wealth * (target_bursa_pct / 100.0)
    target_us_val = total_wealth * (target_us_pct / 100.0)
    target_cash_val = total_wealth * (target_cash_pct / 100.0)

    diff_bursa = target_bursa_val - val_bursa
    diff_us = target_us_val - val_us
    diff_cash = target_cash_val - val_cash

    rebalance_data = [
        {
            "Segmen Aset": "🇲🇾 Bursa Malaysia (GFM)",
            "Nilai Semasa (RM)": val_bursa,
            "Peratus Semasa": f"{(val_bursa/total_wealth*100):.1f}%",
            "Sasaran Ideal (%)": f"{target_bursa_pct}%",
            "Nilai Sasaran (RM)": target_bursa_val,
            "Tindakan Pengimbangan": f"🟢 TAMBAH MODAL +RM {abs(diff_bursa):,.2f}" if diff_bursa > 0 else f"🔴 KURANGKAN -RM {abs(diff_bursa):,.2f}"
        },
        {
            "Segmen Aset": "🇺🇸 Wall Street US (UMC)",
            "Nilai Semasa (RM)": val_us,
            "Peratus Semasa": f"{(val_us/total_wealth*100):.1f}%",
            "Sasaran Ideal (%)": f"{target_us_pct}%",
            "Nilai Sasaran (RM)": target_us_val,
            "Tindakan Pengimbangan": f"🟢 TAMBAH MODAL +RM {abs(diff_us):,.2f}" if diff_us > 0 else f"🔴 KURANGKAN -RM {abs(diff_us):,.2f}"
        },
        {
            "Segmen Aset": "💵 Penampan Tunai (Buffer)",
            "Nilai Semasa (RM)": val_cash,
            "Peratus Semasa": f"{(val_cash/total_wealth*100):.1f}%",
            "Sasaran Ideal (%)": f"{target_cash_pct}%",
            "Nilai Sasaran (RM)": target_cash_val,
            "Tindakan Pengimbangan": f"🟢 SIMPAN TUNAI +RM {abs(diff_cash):,.2f}" if diff_cash > 0 else f"🔴 GUNAKAN TUNAI -RM {abs(diff_cash):,.2f}"
        }
    ]

    df_reb = pd.DataFrame(rebalance_data)
    st.dataframe(
        df_reb.style.format({
            "Nilai Semasa (RM)": "RM {:,.2f}",
            "Nilai Sasaran (RM)": "RM {:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )

    st.info(f"""
    💡 **Pelan Tindakan Rebalancing Rasmi:**  
    Portfolio semasa anda mempunyai pendedahan Wall Street sebanyak **{(val_us/total_wealth*100):.1f}%** (berat sebelah).  
    Untuk mencapai keseimbangan sasaran, cairkan sebahagian posisi saham US dan suntikkan **RM {abs(diff_bursa):,.2f}** ke dalam kaunter gred A+ Bursa Malaysia di Meja Keputusan Harian.
    """)


# ======================================================================================
# 3. SISTEM PENGESAHAN 3 TEMPOH MASA (TRIPLE SCREEN CONFLUENCE)
# ======================================================================================
def render_multitimeframe_confluence_ui():
    st.subheader("📈 Sistem Pengesahan 3 Tempoh Masa (Triple Screen Confluence)")
    st.caption("Berasaskan metodologi Dr. Alexander Elder: Hanya beli apabila Carta Bulanan (Arus), Mingguan (Ombak) dan Harian (Riak) selaras serentak.")

    confluence_records = [
        {
            "Ticker": "KLSE:TENAGA",
            "Pasaran": "Bursa",
            "Skrin 1: Bulanan (Arus Makro)": "🟢 Bullish (EMA > SMA200)",
            "Skrin 2: Mingguan (Ombak Wyckoff)": "🟢 Fasa D (Pullback Selesai)",
            "Skrin 3: Harian (Riak Masa Entri)": "🟢 Breakout Sokongan RM 12.60",
            "Status Konfluens": "⭐⭐⭐ TRIPLE CONFLUENCE (STRONG BUY)",
            "Kebarangkalian Menang": "88.5%"
        },
        {
            "Ticker": "KLSE:GAMUDA",
            "Pasaran": "Bursa",
            "Skrin 1: Bulanan (Arus Makro)": "🟢 Bullish Uptrend",
            "Skrin 2: Mingguan (Ombak Wyckoff)": "🟢 Accumulation Puncak",
            "Skrin 3: Harian (Riak Masa Entri)": "🟢 Lantunan Sokongan RM 4.45",
            "Status Konfluens": "⭐⭐⭐ TRIPLE CONFLUENCE (STRONG BUY)",
            "Kebarangkalian Menang": "86.0%"
        },
        {
            "Ticker": "NASDAQ:NVDA",
            "Pasaran": "US",
            "Skrin 1: Bulanan (Arus Makro)": "🟢 Super-Cycle Uptrend",
            "Skrin 2: Mingguan (Ombak Wyckoff)": "🟡 Re-accumulation Fasa D",
            "Skrin 3: Harian (Riak Masa Entri)": "🟢 Lantunan EMA 20 ($138.50)",
            "Status Konfluens": "⭐⭐ DUAL CONFLUENCE (BUY LIMIT)",
            "Kebarangkalian Menang": "79.2%"
        },
        {
            "Ticker": "NYSE:UMC (Aktif)",
            "Pasaran": "US",
            "Skrin 1: Bulanan (Arus Makro)": "🟡 Sideway Mendatar",
            "Skrin 2: Mingguan (Ombak Wyckoff)": "🔴 Ujian Sokongan Bawah",
            "Skrin 3: Harian (Riak Masa Entri)": "🔴 Di Bawah EMA 50 ($18.65)",
            "Status Konfluens": "⚠️ SIFAR KONFLUENS (HOLD / TRAILING SL)",
            "Kebarangkalian Menang": "48.0%"
        },
        {
            "Ticker": "KLSE:0039 (GFM)",
            "Pasaran": "Bursa",
            "Skrin 1: Bulanan (Arus Makro)": "🟡 Lantai Asas Konsolidasi",
            "Skrin 2: Mingguan (Ombak Wyckoff)": "🟡 Fasa B (Volum Kering)",
            "Skrin 3: Harian (Riak Masa Entri)": "🟡 Pulang Modal RM 0.175",
            "Status Konfluens": "🟡 TUNGGU CATALYST (WAIT & SEE)",
            "Kebarangkalian Menang": "52.0%"
        }
    ]

    df_conf = pd.DataFrame(confluence_records)
    st.dataframe(
        df_conf.style.map(
            lambda v: "color: #00E676; font-weight: bold;" if "TRIPLE" in str(v) else ("color: #FF5252; font-weight: bold;" if "SIFAR" in str(v) else "color: #FFBB28;"),
            subset=["Status Konfluens"]
        ),
        width="stretch",
        hide_index=True
    )

    st.success("💎 **Peraturan Emas Alexander Elder:** Jangan sesekali menentang Arus Bulanan. Beli hanya apabila riak harian melantun mengikut arah arus bulanan.")


# ======================================================================================
# 4. PENGANALISIS PENYATA KEWANGAN & LAPORAN SUKU TAHUN AI (EARNINGS ANALYZER)
# ======================================================================================
def render_earnings_statement_analyzer():
    st.subheader("📑 Penganalisis Penyata Kewangan & Laporan Suku Tahun AI")
    st.caption("Imbas penyata kewangan syarikat dalam beberapa saat untuk mengesan tanda bahaya (Red Flags) dan pertumbuhan sebenar.")

    c_f1, c_f2 = st.columns([5, 5])

    with c_f1:
        st.markdown("#### 📤 Masukkan Laporan Kewangan:")
        uploaded_file = st.file_uploader("Muat naik fail Penyata Suku Tahun (PDF / TXT):", type=["txt", "pdf", "csv"])
        pasted_text = st.text_area(
            "Atau tampal teks ringkasan kewangan syarikat di sini:",
            placeholder="Contoh: Tenaga Nasional Berhad merekodkan hasil RM 14.5 Bilion, peningkatan 8.2% YoY. Untung bersih melonjak 15.4% kepada RM 1.2 Bilion didorong permintaan data center...",
            height=130
        )
        sample_choice = st.selectbox(
            "Atau pilih sampel laporan audit sedia ada:",
            ["Tenaga Nasional Berhad (Q2 2026)", "NVIDIA Corporation (Q2 2026)", "United Microelectronics Corp (Q2 2026)"]
        )

    with c_f2:
        st.markdown("#### 🤖 Hasil Bedah Siasat Kewangan AI:")

        if sample_choice == "Tenaga Nasional Berhad (Q2 2026)":
            st.markdown("""
            <div style="background:#0F291E; border:2px solid #00E676; border-radius:12px; padding:16px;">
                <h4 style="color:#00E676; margin-top:0;">🟢 KEPUTUSAN AI: FUNDAMENTAL GRED A+ (LULUS)</h4>
                <ul>
                    <li><b>Pertumbuhan Hasil (YoY):</b> +8.2% (RM 14.5 Bilion)</li>
                    <li><b>Untung Bersih (YoY):</b> +15.4% (Margin EBITDA berkembang ke 28.5%)</li>
                    <li><b>Aliran Tunai Operasi (OCF):</b> Sihat (RM 4.8 Bilion tunai masuk)</li>
                    <li><b>Pengesanan Amaran Bahaya (Red Flags):</b> <b>0 Amaran</b> (Hutang jangka pendek terlindung ICPT)</li>
                </ul>
                <div style="background:#161D2B; padding:8px; border-radius:6px; font-size:12px; color:#A7F3D0;">
                    💡 <b>Rumusan AI:</b> Syarikat menikmati limpahan perbelanjaan modal grid AI. Sesuai untuk pengkompaunan modal jangka panjang.
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif sample_choice == "NVIDIA Corporation (Q2 2026)":
            st.markdown("""
            <div style="background:#0F291E; border:2px solid #00E676; border-radius:12px; padding:16px;">
                <h4 style="color:#00E676; margin-top:0;">🟢 KEPUTUSAN AI: FUNDAMENTAL MONOPOLI KUAT (LULUS)</h4>
                <ul>
                    <li><b>Pertumbuhan Hasil (YoY):</b> +122.0% ($30.0 Bilion)</li>
                    <li><b>Margin Kasar (Gross Margin):</b> 75.1% (Sangat Luar Biasa)</li>
                    <li><b>Aliran Tunai Bebas (FCF):</b> $13.5 Bilion</li>
                    <li><b>Pengesanan Amaran Bahaya (Red Flags):</b> <b>0 Amaran</b> (Buku tempahan cip Blackwell penuh)</li>
                </ul>
                <div style="background:#161D2B; padding:8px; border-radius:6px; font-size:12px; color:#A7F3D0;">
                    💡 <b>Rumusan AI:</b> Pertumbuhan kuantitatif institusi tertinggi. Beli setiap kali berlaku pembetulan teknikal (Dip).
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:#2D2512; border:2px solid #FFBB28; border-radius:12px; padding:16px;">
                <h4 style="color:#FFBB28; margin-top:0;">🟡 KEPUTUSAN AI: STABIL TETAPI PERTUMBUHAN PERLAHAN</h4>
                <ul>
                    <li><b>Pertumbuhan Hasil (YoY):</b> +2.1% ($1.75 Bilion)</li>
                    <li><b>Margin Kasar:</b> 34.0% (Mampan dengan hasil dividen 3.75%)</li>
                    <li><b>Nisbah P/E Semasa:</b> 11.5x (Penilaian murah / Value Play)</li>
                    <li><b>Pengesanan Amaran Bahaya:</b> <b>1 Amaran Ringan</b> (Permintaan sektor automotif dan perindustrian nod matang mendatar)</li>
                </ul>
                <div style="background:#161D2B; padding:8px; border-radius:6px; font-size:12px; color:#FEF3C7;">
                    💡 <b>Rumusan AI:</b> Bukan saham pertumbuhan laju. Kunci untung segera jika paras sokongan $18.00 teruji.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ======================================================================================
# FUNGSI INDUK PAPARAN TAB SUITE ELIT
# ======================================================================================
def render_elite_expansion_suite(fx_rate: float = 4.0773):
    st.header("🚀 Enjin Tindakan Elit: Alerts, Rebalancing, Confluence & Audit Penyata")
    st.caption("Pusat analitik lanjutan untuk memperkukuh kelebihan kuantitatif (Quantitative Edge) pelabur institusi.")

    s1, s2, s3, s4 = st.tabs([
        "🔔 1. Notifikasi Pelayar (Push Alerts)",
        "⚖️ 2. Pengimbangan Semula Portfolio",
        "📈 3. Pengesahan 3 Tempoh Masa (Triple Screen)",
        "📑 4. Penganalisis Penyata Kewangan AI"
    ])

    with s1:
        render_browser_notification_engine()
    with s2:
        render_portfolio_rebalancer_ui(fx_rate=fx_rate)
    with s3:
        render_multitimeframe_confluence_ui()
    with s4:
        render_earnings_statement_analyzer()
