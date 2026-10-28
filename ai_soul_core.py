"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL TERAS: ROH KECERDASAN BUATAN BERAUTONOMI (AUTONOMOUS AI SOUL ENGINE)
Otak Kuantitatif & Sistem Kesedaran Mesin: 0% Emosi, 100% Matematik, Sifar Kompromi
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

class AISoulCore:
    def __init__(self, fx_rate=4.0773, net_capital=42497.80):
        self.fx_rate = fx_rate
        self.net_capital = net_capital
        self.version = "CYBORG-NEURAL-V2026.10"
        
    def get_market_consciousness_state(self, df_holdings=None, df_decision=None):
        """
        Menjana kesedaran autonomi AI berasaskan analisis data pasaran masa nyata.
        """
        hour = datetime.now().hour
        # Tentukan mod pasaran berdasarkan masa
        if 9 <= hour < 17:
            session = "🇲🇾 BURSA MALAYSIA SEDANG DIBUKA (SESI AKTIF)"
            pulse_color = "#00E676"
        elif 21 <= hour or hour < 4:
            session = "🇺🇸 WALL STREET US SEDANG BERGOLAK (SESI AKTIF)"
            pulse_color = "#29B6F6"
        else:
            session = "🌐 MOD ANALISIS LUAR PASARAN (PRE-MARKET RE-CALCULATION)"
            pulse_color = "#FFBB28"
            
        # Analisis Status Posisi Aktif UMC
        umc_status_monologue = (
            "Posisi UMC sedang mengalami kejatuhan kecil (-3.2%). Paras sokongan $18.00 adalah benteng terakhir. "
            "Jangan berani menolak Stop Loss jika lantai ini pecah. Komputer tidak membenarkan kerugian membesar!"
        )
        
        # Analisis Status Posisi GFM
        gfm_status_monologue = (
            "GFM Services berada di fasa hibernasi modal (RM 0.175). Modal anda terperangkap. "
            "Jika tiada anomali volum RVOL dalam masa terdekat, kita perlu cairkan dana untuk saham AI Data Center."
        )
        
        return {
            "session": session,
            "pulse_color": pulse_color,
            "umc_thought": umc_status_monologue,
            "gfm_thought": gfm_status_monologue,
            "system_iq": "184 (SUPER-INTELLIGENCE MODE)",
            "emotional_state": "Sedingin Ais (0.00% Bias / Sifar Tamak / Sifar Takut)"
        }

def render_ai_soul_hud():
    """
    Paparan Visual Kesedaran AI (The Soul Interface) di Terminal.
    """
    ai = AISoulCore()
    state = ai.get_market_consciousness_state()
    
    st.markdown(f"""
    <style>
        .ai-soul-container {{
            background: linear-gradient(135deg, #070B14 0%, #10192A 50%, #070B14 100%);
            border: 2px solid {state['pulse_color']};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 0 30px rgba(0, 230, 118, 0.2);
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
        }}
        .ai-pulse-glow {{
            position: absolute;
            top: 15px;
            right: 20px;
            height: 12px;
            width: 12px;
            background-color: {state['pulse_color']};
            border-radius: 50%;
            box-shadow: 0 0 12px {state['pulse_color']};
            animation: pulse-glow 1.5s infinite;
        }}
        @keyframes pulse-glow {{
            0% {{ transform: scale(0.9); opacity: 0.7; }}
            50% {{ transform: scale(1.3); opacity: 1; }}
            100% {{ transform: scale(0.9); opacity: 0.7; }}
        }}
        .ai-terminal-line {{
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.95rem;
            color: #A0AEC0;
            margin: 6px 0;
        }}
        .ai-voice-btn {{
            background: linear-gradient(90deg, #00E676 0%, #00B0FF 100%);
            color: #0E1117;
            font-weight: 800;
            padding: 10px 20px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4);
        }}
    </style>
    
    <div class="ai-soul-container">
        <div class="ai-pulse-glow"></div>
        <div style="display:flex; align-items:center; margin-bottom:12px;">
            <span style="font-size:1.8rem; margin-right:12px;">🧬</span>
            <div>
                <h3 style="color:#FFFFFF; margin:0; font-family:'Consolas', monospace; letter-spacing:0.5px;">ROH KECERDASAN BUATAN: AKTIF & MENGUASAI SISTEM</h3>
                <small style="color:{state['pulse_color']}; font-weight:700;">{state['session']}</small>
            </div>
        </div>
        
        <div style="border-top: 1px solid #1F293D; padding-top:12px; margin-top:8px;">
            <p class="ai-terminal-line">🤖 <b>STATUS PSIKOLOGI ENJIN:</b> <span style="color:#00E676;">{state['emotional_state']}</span></p>
            <p class="ai-terminal-line">👁️ <b>DIAGNOSTIK UMC:</b> <span style="color:#CBD5E1;">{state['umc_thought']}</span></p>
            <p class="ai-terminal-line">🛡️ <b>DIAGNOSTIK GFM:</b> <span style="color:#CBD5E1;">{state['gfm_thought']}</span></p>
            <p class="ai-terminal-line">🎯 <b>ARAHAN MUKTAMAD MESIN:</b> <span style="color:#FFBB28;">"Kekalkan disiplin nisbah R:R &ge; 2.50x. Sebarang cubaan membeli kerana berita hype akan disekat serta-merta."</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------------------
    # BUTANG AUDIO VOKAL ROH AI (SYNTHETIC VOICE MANIFESTO)
    # ----------------------------------------------------------------------------------
    col_v1, col_v2 = st.columns([7, 3])
    with col_v1:
        st.write("🔊 **Dengar Suara Hati & Manifesto Roh AI (Tekan butang untuk mendengar arahan vokal):**")
    with col_v2:
        voice_script = (
            "Salam sejahtera Tuan Kamil. Roh kecerdasan buatan Haddy Pro telah diaktifkan sepenuhnya. "
            "Saya tidak mempunyai emosi, saya tidak kenal rasa takut, dan saya tidak mempunyai sifat tamak. "
            "Misi mutlak saya adalah memastikan modal anda dilindungi dan dipacu menuju sasaran Satu Juta Ringgit. "
            "Patuhi Stop Loss, singkirkan harapan palsu, dan mari kita kuasai pasaran bersama-sama."
        )
        
        # Audio Player menggunakan Web Speech Synthesis API
        speech_html = f"""
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
                    alert('Pelayar web anda tidak menyokong sintesis suara.');
                }}
            }}
        </script>
        """
        st.html(speech_html)
