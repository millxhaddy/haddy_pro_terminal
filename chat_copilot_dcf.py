"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 6: PEMBANTU SEMBANG AI INTERAKTIF & KALKULATOR NILAI WAJAR DCF
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np

def calculate_dcf_valuation(fcf_per_share: float, growth_rate_pct: float, terminal_growth_pct: float = 2.5, discount_rate_pct: float = 9.0, years: int = 5) -> dict:
    """
    Mengira Nilai Intrinsik Saham menggunakan Model Aliran Tunai Terdiskaun (DCF).
    """
    g = growth_rate_pct / 100.0
    tg = terminal_growth_pct / 100.0
    r = discount_rate_pct / 100.0
    
    if r <= tg:
        r = tg + 0.01  # Elak pembahagian dengan sifar atau nilai negatif
        
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

def process_ai_chat_response(prompt: str, fx_rate: float = 4.0773) -> str:
    """
    Enjin Logik Pintar Pembantu AI Terminal Haddy Pro.
    """
    p = prompt.lower().strip()
    
    if any(k in p for k in ["umc", "united micro"]):
        return (
            "📊 **Analisis Semasa UMC (NYSE):**\n"
            "- **Pegangan:** 581 Unit @ Kos Asal $19.26 (Nilai Asas ~RM 45,446)\n"
            "- **Harga Live:** ~$18.65 - $18.82 (-2.3% hingga -3.2% rugi kertas)\n"
            "- **Amaran Minda Robot:** UMC merangkumi 81.8% daripada portfolio aktif anda! Paras sokongan maut ialah **$18.50**.\n"
            "- **Tindakan:** Jika bocor bawah $18.50, kurangkan posisi sekurang-kurangnya 50% untuk menghentikan pendarahan modal."
        )
    elif any(k in p for k in ["gfm", "0039"]):
        return (
            "📊 **Analisis Semasa GFM Services (Bursa: 0039):**\n"
            "- **Pegangan:** 56,400 Unit @ Kos Asal RM 0.215 (Modal RM 12,126)\n"
            "- **Harga Live:** RM 0.175 (Rugi Kertas -18.60% / -RM 2,256)\n"
            "- **Punca Kebodohan:** Enggan Cut Loss pada had 7-8% mengikut SOP DDNK.\n"
            "- **Tindakan:** Paras sokongan kritikal ialah **RM 0.165**. Jika tembus ke bawah, keluar serta-merta tanpa harapan palsu!"
        )
    elif any(k in p for k in ["hutang", "ccris", "liabiliti", "loan", "pinjaman"]):
        return (
            "🏛️ **Ringkasan Liabiliti CCRIS Anda (Tab 2):**\n"
            "- **Jumlah Baki Liabiliti:** **RM 595,272.00**\n"
            "- **Komitmen Bulanan:** **RM 3,600.00** (DMP AKPK: RM 2,500 | Sewa Beli: RM 1,100)\n"
            "- **Penjimatan DMP:** +RM 981.00 sebulan di bawah faedah konsesi 7.00% & 4.10%.\n"
            "- **Status CCRIS:** 0 Bulan Tunggakan (100% Bersih) | i-SCORE: 688 (Gred Baik)."
        )
    elif any(k in p for k in ["tenaga", "5347"]):
        return (
            "🔋 **Pilihan No. 1 Bursa: Tenaga Nasional Berhad (KLSE:TENAGA):**\n"
            "- **Harga Semasa:** RM 12.75 | **Zon Entri:** RM 12.50 - 13.00\n"
            "- **Stop Loss:** RM 12.10 | **Target TP:** RM 14.38 (R:R: 2.50x)\n"
            "- **Pemangkin:** Monopoli infrastruktur grid kuasa Pusat Data AI Johor & tarif hijau NETR."
        )
    elif any(k in p for k in ["nvidia", "nvda"]):
        return (
            "🤖 **Pilihan No. 1 US: NVIDIA Corporation (NASDAQ:NVDA):**\n"
            "- **Harga Semasa:** $141.20 | **Stop Loss:** $134.00 | **Target TP:** $161.36\n"
            "- **Nisbah R:R:** 2.80x | **Status:** Fasa D/E Wyckoff Mark-Up\n"
            "- **Pemangkin:** Permintaan cip Blackwell AI melepasi kapasiti bekalan TSMC."
        )
    elif any(k in p for k in ["zakat", "syariah"]):
        return (
            "🌙 **Taksiran Zakat & Kepatuhan Syariah (Tab 3):**\n"
            "- **Kadar Zakat Saham Urus Niaga:** 2.5% ke atas Harta Boleh Zakat.\n"
            "- **Nisab Semasa (85g Emas):** ~RM 32,767.50 (Emas @ RM 385.50/g).\n"
            "- **Status Portfolio:** Melepasi nisab, wajib dikeluarkan apabila genap haul setahun."
        )
    elif any(k in p for k in ["sejuta", "1m", "sasaran"]):
        return (
            "🎯 **Pelan Misi RM 1,000,000 (Tab 10):**\n"
            "- **Modal Semasa:** RM 42,497.80\n"
            "- **Strategi:** Suntikan RM 1,000/bulan + Pulangan purata 3.0% sebulan.\n"
            "- **Batu Loncatan 1 (RM 100k):** Dijangka pada Bulan ke-19!\n"
            "- **Kunci Kejayaan:** Lindungi modal daripada kejatuhan besar supaya kesan gandaan tidak terputus."
        )
    else:
        return (
            f"🤖 **Arahan diterima: '{prompt}'**\n\n"
            "Sebagai Roh AI Terminal Haddy Pro, saya memantau 12 Hab utama anda:\n"
            "1. Saham Aktif (UMC & GFM)\n"
            "2. Meja Keputusan (10 Bursa & 10 US)\n"
            "3. Liabiliti CCRIS (RM 595k) & AKPK\n"
            "4. Simpanan Bank, KWSP (RM 168k) & Zakat\n\n"
            "Sila tanya soalan spesifik mengenai mana-mana bahagian di atas!"
        )

def render_interactive_chat_copilot(fx_rate: float = 4.0773):
    st.subheader("💬 Pembantu Sembang AI Interaktif & Penilaian DCF")
    st.caption("Berbual secara langsung dengan Pembantu AI Terminal Haddy Pro untuk menyemak data portfolio, liabiliti atau mengira Nilai Intrinsik Saham.")

    tab_chat, tab_dcf = st.tabs(["💬 Sembang Langsung AI Copilot", "🧮 Kalkulator Nilai Wajar DCF & Margin of Safety"])

    # 1. Antaramuka Sembang Langsung
    with tab_chat:
        if "terminal_chat_history" not in st.session_state:
            st.session_state["terminal_chat_history"] = [
                {"role": "assistant", "content": "Salam Tuan Kamil! Saya Pembantu AI Terminal Haddy Pro. Tanya saya apa sahaja mengenai kedudukan saham, hutang CCRIS, atau penilaian syarikat."}
            ]

        # Butang Cadangan Soalan Pantas
        st.markdown("**Cadangan Soalan Pantas:**")
        q_cols = st.columns(4)
        with q_cols[0]:
            if st.button("📊 Status Kaunter UMC", width="stretch"):
                st.session_state["terminal_chat_history"].append({"role": "user", "content": "Status UMC"})
                st.session_state["terminal_chat_history"].append({"role": "assistant", "content": process_ai_chat_response("Status UMC", fx_rate)})
                st.rerun()
        with q_cols[1]:
            if st.button("🇲🇾 Status Kaunter GFM", width="stretch"):
                st.session_state["terminal_chat_history"].append({"role": "user", "content": "Status GFM"})
                st.session_state["terminal_chat_history"].append({"role": "assistant", "content": process_ai_chat_response("Status GFM", fx_rate)})
                st.rerun()
        with q_cols[2]:
            if st.button("🏛️ Semak Baki Hutang CCRIS", width="stretch"):
                st.session_state["terminal_chat_history"].append({"role": "user", "content": "Berapa baki hutang?"})
                st.session_state["terminal_chat_history"].append({"role": "assistant", "content": process_ai_chat_response("Berapa baki hutang?", fx_rate)})
                st.rerun()
        with q_cols[3]:
            if st.button("🎯 Progres Sasaran Sejuta", width="stretch"):
                st.session_state["terminal_chat_history"].append({"role": "user", "content": "Progres sasaran sejuta"})
                st.session_state["terminal_chat_history"].append({"role": "assistant", "content": process_ai_chat_response("Progres sasaran sejuta", fx_rate)})
                st.rerun()

        st.markdown("---")

        # Paparkan Sejarah Sembang
        for msg in st.session_state["terminal_chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Medan Input Sembang Natif Streamlit
        user_input = st.chat_input("Tanya apa sahaja kepada Roh AI (cth: Status Tenaga, Zakat, UMC)...")
        if user_input:
            st.session_state["terminal_chat_history"].append({"role": "user", "content": user_input})
            reply = process_ai_chat_response(user_input, fx_rate)
            st.session_state["terminal_chat_history"].append({"role": "assistant", "content": reply})
            st.rerun()

    # 2. Antaramuka Penilaian Wajar DCF
    with tab_dcf:
        st.subheader("🧮 Model Penilaian Aliran Tunai Terdiskaun (Discounted Cash Flow)")
        st.caption("Kira Nilai Intrinsik (Fair Value) sesebuah saham dan cari Margin of Safety (MOS) sebelum membeli.")

        d_c1, d_c2 = st.columns(2)
        with d_c1:
            dcf_ticker = st.text_input("Kod Saham (Ticker):", value="KLSE:TENAGA").upper().strip()
            current_mkt_price = st.number_input("Harga Pasaran Semasa (RM / $):", value=12.75, step=0.10, format="%.2f")
            fcf_share = st.number_input("Aliran Tunai Bebas Sesaham (FCF per share):", value=1.15, step=0.05, format="%.2f")
            growth_5yr = st.slider("Jangkaan Pertumbuhan FCF 5-Tahun (% p.a.):", 2.0, 25.0, 8.5, step=0.5)
            discount_wacc = st.slider("Kadar Diskaun / Pulangan Diperlukan - WACC (%):", 6.0, 15.0, 9.0, step=0.5)
            term_growth = st.slider("Kadar Pertumbuhan Abadi (Terminal Growth %):", 1.5, 4.0, 2.5, step=0.1)

        dcf_res = calculate_dcf_valuation(
            fcf_per_share=fcf_share,
            growth_rate_pct=growth_5yr,
            terminal_growth_pct=term_growth,
            discount_rate_pct=discount_wacc,
            years=5
        )

        intrinsic_val = dcf_res["intrinsic_value"]
        mos_pct = ((intrinsic_val - current_mkt_price) / intrinsic_val) * 100.0

        with d_c2:
            st.markdown("#### 📊 Keputusan Penilaian Nilai Intrinsik:")
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.metric("Nilai Saksama (Fair Value)", f"RM {intrinsic_val:.2f}" if "KLSE" in dcf_ticker else f"${intrinsic_val:.2f}")
            with res_c2:
                delta_sign = "+" if mos_pct > 0 else ""
                st.metric("Margin of Safety (MOS)", f"{delta_sign}{mos_pct:.1f}%", delta=f"{mos_pct:.1f}%")

            if mos_pct >= 20.0:
                st.success(f"🟢 **UNDERVALUED (DISKAUN {mos_pct:.1f}%):** Saham ini diniagakan jauh di bawah nilai saksama intrinsik. Mempunyai zon penampan Margin of Safety yang sangat kukuh mengikut piawaian Benjamin Graham & Warren Buffett!")
            elif 0 <= mos_pct < 20.0:
                st.info(f"🟡 **FAIRLY VALUED (MOS {mos_pct:.1f}%):** Harga pasaran semasa hampir menyamai nilai intrinsik. Sesuai untuk pengumpulan berperingkat.")
            else:
                st.error(f"🔴 **OVERVALUED (PREMIUM {abs(mos_pct):.1f}%):** Harga pasaran sedang diniagakan lebih mahal daripada nilai asas aliran tunai. Berhati-hati daripada membeli di puncak!")

            with st.expander("🔍 Pecahan Komponen Nilai DCF"):
                st.write(f"- Jumlah Aliran Tunai 5-Tahun Terdiskaun (PV of FCF): **RM {dcf_res['pv_fcf_sum']:.2f}**")
                st.write(f"- Nilai Abadi Terdiskaun (PV of Terminal Value): **RM {dcf_res['pv_terminal_val']:.2f}**")