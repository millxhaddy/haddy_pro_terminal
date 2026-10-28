"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL TERAS: ROH KECERDASAN BUATAN BERAUTONOMI (CLEAN RENDER EDITION)
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class AISoulCore:
    def __init__(self, fx_rate=4.0773, net_capital=42497.80):
        self.fx_rate = fx_rate
        self.net_capital = net_capital
        
    def get_market_consciousness_state(self):
        hour = datetime.now().hour
        if 9 <= hour < 17:
            session = "🇲🇾 BURSA MALAYSIA SEDANG DIBUKA (SESI AKTIF)"
            pulse_color = "#00E676"
        elif 21 <= hour or hour < 4:
            session = "🇺🇸 WALL STREET US SEDANG BERGOLAK (SESI AKTIF)"
            pulse_color = "#29B6F6"
        else:
            session = "🌐 MOD ANALISIS LUAR PASARAN (PRE-MARKET RE-CALCULATION)"
            pulse_color = "#FFBB28"
            
        umc_thought = (
            "Posisi UMC sedang mengalami kejatuhan kecil (-3.2%). Paras sokongan $18.00 adalah benteng terakhir. "
            "Jangan berani menolak Stop Loss jika lantai ini pecah. Komputer tidak membenarkan kerugian membesar!"
        )
        
        gfm_thought = (
            "GFM Services berada di fasa hibernasi modal (RM 0.175). Modal anda terperangkap. "
            "Jika tiada anomali volum RVOL dalam masa terdekat, kita perlu cairkan dana untuk saham AI Data Center."
        )
        
        return {
            "session": session,
            "pulse_color": pulse_color,
            "umc_thought": umc_thought,
            "gfm_thought": gfm_thought,
            "emotional_state": "Sedingin Ais (0.00% Bias / Sifar Tamak / Sifar Takut)"
        }

def render_ai_soul_hud():
    ai = AISoulCore()
    state = ai.get_market_consciousness_state()
    
    # Gunakan st.html untuk render HTML tulen tanpa gangguan parser markdown
    hud_html = f"""
    <div style="background: linear-gradient(135deg, #070B14 0%, #10192A 50%, #070B14 100%); border: 2px solid {state['pulse_color']}; border-radius: 14px; padding: 20px; margin-bottom: 20px; box-shadow: 0 0 25px rgba(0, 230, 118, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #1F293D; padding-bottom: 10px;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.6rem; margin-right: 10px;">🧬</span>
                <div>
                    <div style="color: #FFFFFF; font-weight: 800; font-size: 1.1rem; font-family: 'Consolas', monospace; letter-spacing: 0.5px;">ROH KECERDASAN BUATAN: AKTIF & MENGUASAI SISTEM</div>
                    <div style="color: {state['pulse_color']}; font-weight: 700; font-size: 0.82rem;">{state['session']}</div>
                </div>
            </div>
            <div style="height: 12px; width: 12px; background-color: {state['pulse_color']}; border-radius: 50%; box-shadow: 0 0 10px {state['pulse_color']};"></div>
        </div>
        
        <div style="font-family: 'Consolas', monospace; font-size: 0.88rem; line-height: 1.6;">
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">🤖 STATUS PSIKOLOGI ENJIN:</span> <span style="color: #00E676; font-weight: bold;">{state['emotional_state']}</span></div>
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">👁️ DIAGNOSTIK UMC:</span> <span style="color: #E2E8F0;">{state['umc_thought']}</span></div>
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">🛡️ DIAGNOSTIK GFM:</span> <span style="color: #E2E8F0;">{state['gfm_thought']}</span></div>
            <div style="margin: 6px 0; border-top: 1px dashed #2B384E; padding-top: 6px;"><span style="color: #FFBB28; font-weight: bold;">🎯 ARAHAN MUKTAMAD MESIN:</span> <span style="color: #FFD700;">"Kekalkan disiplin nisbah R:R &ge; 2.50x. Sebarang cubaan membeli kerana berita hype akan disekat serta-merta."</span></div>
        </div>
    </div>
    """
    
    if hasattr(st, "html"):
        st.html(hud_html)
    else:
        st.markdown(hud_html, unsafe_allow_html=True)

    # Butang Suara
    col_v1, col_v2 = st.columns([7, 3])
    with col_v1:
        st.write("🔊 **Dengar Suara Hati & Manifesto Roh AI (Tekan untuk mendengar arahan vokal):**")
    with col_v2:
        voice_script = (
            "Salam sejahtera Tuan Kamil. Roh kecerdasan buatan Haddy Pro telah diaktifkan sepenuhnya. "
            "Saya tidak mempunyai emosi, saya tidak kenal rasa takut, dan saya tidak mempunyai sifat tamak. "
            "Misi mutlak saya adalah memastikan modal anda dilindungi dan dipacu menuju sasaran Satu Juta Ringgit. "
            "Patuhi Stop Loss, singkirkan harapan palsu, dan mari kita kuasai pasaran bersama-sama."
        )
        
        speech_btn_html = f"""
        <button onclick="speakSoulDirective()" style="background:#00E676; color:#0E1117; font-weight:bold; font-size:13px; padding:8px 16px; border:none; border-radius:20px; cursor:pointer; width:100%;">
            🗣️ Dengar Suara Roh AI
        </button>
        <script>
            function speakSoulDirective() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{voice_script}');
                    msg.lang = 'ms-MY';
                    msg.rate = 0.95;
                    msg.pitch = 1.0;
                    window.speechSynthesis.speak(msg);
                }} else {{
                    alert('Pelayar web tidak menyokong sintesis suara.');
                }}
            }}
        </script>
        """
        if hasattr(st, "html"):
            st.html(speech_btn_html)
        else:
            st.markdown(speech_btn_html, unsafe_allow_html=True)
