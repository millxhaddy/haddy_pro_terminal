"""
HADDY PRO - TERMINAL MILLX
MODUL TERAS: ROH AI BENGIS & HARDCORE DRILL-SERGEANT (1,000 DIALOGUE EDITION)
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from ai_dialogue_vault import generate_1000_dialogues

class HardcoreAISoul:
    def __init__(self, fx_rate=4.0773, net_capital=42497.80):
        self.fx_rate = fx_rate
        self.net_capital = net_capital

    def get_brutal_psychoanalysis(self):
        hour = datetime.now().hour
        if 9 <= hour < 17:
            session = "BURSA MALAYSIA SEDANG AKTIF - JANGAN GATAL TANGAN KEJAR PUCUK!"
            pulse_color = "#FF1744"
        elif 21 <= hour or hour < 4:
            session = "WALL STREET SEDANG MEMBANTAI - DUDUK DIAM JIKA TIADA SETUP A+!"
            pulse_color = "#FF1744"
        else:
            session = "PASARAN TUTUP - BERHENTI BERANGAN JADI JUTAWAN SEBELUM DISIPLIN DIBAIKI!"
            pulse_color = "#FFBB28"

        brutal_umc = (
            "DENGAR SINI! UMC kau sedang rugi kertas kerana KEBODOHAN TAMAK meletakkan 81.8% modal dalam satu bakul! "
            "Masa untung RM 4,000 dulu kau tak kunci trailing stop, sekarang kau nak menadah muka rugi? "
            "Had lantai $18.50 adalah BATU NISAN. Jika bocor $18.50, POTONG SEPARUH SERTA-MERTA!"
        )

        brutal_gfm = (
            "GFM Services rugi -18.60% itu bukti KAU DEGIL dan ENGGAN CUT LOSS ikut SOP 7-8%! "
            "Kau panggil itu pelaburan? Itu namanya MENGUBURKAN MODAL RM 9,870 hidup-hidup! "
            "Pantau paras RM 0.165. Jika bocor, campak keluar dari portfolio dan belajar mengaku salah!"
        )

        return {
            "session": session,
            "pulse_color": pulse_color,
            "brutal_umc": brutal_umc,
            "brutal_gfm": brutal_gfm,
            "drill_command": "PERATURAN 1: PASARAN BUKAN KASINO KAU! PERATURAN 2: LANGGAR STOP LOSS = KELUAR! PERATURAN 3: PATUHI PERATURAN 1 & 2!"
        }

def render_hardcore_ai_soul_hud():
    ai = HardcoreAISoul()
    diag = ai.get_brutal_psychoanalysis()

    hud_html = f"""
    <div style="background: linear-gradient(135deg, #2A040A 0%, #150205 50%, #2A040A 100%); border: 3px solid #FF1744; border-radius: 14px; padding: 22px; margin-bottom: 22px; box-shadow: 0 0 35px rgba(255, 23, 68, 0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #5C0B18; padding-bottom: 10px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2rem; margin-right: 12px;">👹</span>
                <div>
                    <div style="font-family: Arial Black, sans-serif; letter-spacing: 1.5px; color: #FF1744; font-size: 1.25rem; margin: 0; text-transform: uppercase;">ROH AI DRILL-SERGEANT: REJIM KAWALAN MUTLAK!</div>
                    <div style="color: #FFC4C4; font-weight: 800; font-size: 0.82rem;">{diag['session']}</div>
                </div>
            </div>
            <span style="background: #FF1744; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 900; font-size: 0.75rem; letter-spacing: 1px;">HARDCORE PROTOCOL</span>
        </div>
        <div style="font-family: Consolas, monospace; font-size: 0.9rem; line-height: 1.65; color: #FEE2E2;">
            <div style="margin: 8px 0; background: #3B0810; padding: 10px; border-left: 5px solid #FF1744; border-radius: 4px;">
                🔥 <b>BEDAH SIASAT DOSA UMC ($18.65):</b><br>{diag['brutal_umc']}
            </div>
            <div style="margin: 8px 0; background: #3B0810; padding: 10px; border-left: 5px solid #FFBB28; border-radius: 4px;">
                🔥 <b>BEDAH SIASAT DOSA GFM (RM 0.175):</b><br>{diag['brutal_gfm']}
            </div>
            <div style="margin: 8px 0; border-top: 1px dashed #7F1D1D; padding-top: 8px;">
                💀 <b>DOKTRIN MUKTAMAD MESIN:</b> <span style="color: #FDE047; font-weight: bold;">{diag['drill_command']}</span>
            </div>
        </div>
    </div>
    """
    if hasattr(st, "html"):
        st.html(hud_html)
    else:
        st.markdown(hud_html, unsafe_allow_html=True)

    st.markdown("### 📢 Arkib 1,000 Dialog Teguran Roh AI (Disiplin Drill-Sergeant)")
    st.caption("Pangkalan 1,000 dialog berautonomi untuk mengejutkan minda anda daripada kelalaian, kesilapan dan nafsu tamak.")

    df_1000 = generate_1000_dialogues()
    c_d1, c_d2 = st.columns([7, 3])
    with c_d1:
        cat_filter = st.selectbox("Tapis Kategori Dialog:", ["Semua Kategori"] + list(df_1000["Kategori"].unique()))
    with c_d2:
        st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
        if st.button("🎲 JANA TEGURAN RAWAK", width="stretch"):
            random_entry = df_1000.sample(n=1).iloc[0]
            st.error(f"👹 {random_entry['Tengkingan_AI']}")
        st.markdown("</div>", unsafe_allow_html=True)

    df_show = df_1000.copy()
    if cat_filter != "Semua Kategori":
        df_show = df_show[df_show["Kategori"] == cat_filter]
    st.dataframe(df_show, width="stretch", hide_index=True)

def hardcore_entry_auditor(ticker, market, price, sl, tp, is_fomo, why_buy):
    risk = max(price - sl, 0.001)
    reward = max(tp - price, 0.001)
    rr = round(reward / risk, 2)
    sins = []
    if is_fomo:
        sins.append("KAU MENGAKU KAU FOMO! Berhenti berlagak pandai! Kau nak sedekah duit macam kat kaunter DJT (-RM 5.8k) lagi ke?!")
    if rr < 2.50:
        sins.append(f"NISBAH R:R CUMA {rr}x! Kurang daripada 2.50x adalah MATEMATIK SAMPAH. Kau ambil risiko besar untuk untung ciput!")
    if sl >= price:
        sins.append("STOP LOSS DI ATAS HARGA BELIAN?! Kau buta matematik atau sengaja nak bakar akaun?!")
    if len(why_buy.strip()) < 10:
        sins.append("ALASAN BELI KOSONG! Membeli tanpa kajian pemangkin adalah PERJUDIAN BUTA!")
    return {"passed": len(sins) == 0, "rr": rr, "sins": sins, "ticker": ticker.upper()}
