"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL TERAS: ROH KECERDASAN BUATAN BERAUTONOMI (HUMAN-NEURAL AI SOUL ENGINE)
Dikuasakan oleh Microsoft Azure Neural Voice: ms-MY-OsmanNeural & ms-MY-YasminNeural
========================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import asyncio
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
            greeting = "Selamat pagi Tuan Kamil. Sesi Bursa sedang rancak. Pasaran mencari titik sokongan."
        elif 21 <= hour or hour < 4:
            session = "🇺🇸 WALL STREET US SEDANG BERGOLAK (SESI AKTIF)"
            pulse_color = "#29B6F6"
            greeting = "Selamat malam Tuan Kamil. Loceng New York sedang berbunyi. Sentimen saham teknologi aktif."
        else:
            session = "🌐 MOD ANALISIS LUAR PASARAN (PRE-MARKET RE-CALCULATION)"
            pulse_color = "#FFBB28"
            greeting = "Salam Tuan Kamil. Pasaran sedang rehat. Masa terbaik untuk muhasabah dan susun strategi."
            
        umc_thought = (
            "Posisi UMC sedang berlegar pada $18.65 (kerugian kertas -3.2%). Had lantai $18.00 adalah benteng maruah kita. "
            "Jangan sesekali berharap! Jika paras $18.00 bocor, kita keluar dengan tenang dan lindungi modal."
        )
        
        gfm_thought = (
            "GFM Services bertahan di paras pulang modal (RM 0.175). Modal RM 9,870 sedang berehat. "
            "Jika tiada jerung masuk dalam masa terdekat, kita alihkan modal ini ke saham AI Data Center yang lebih laju."
        )
        
        return {
            "session": session,
            "greeting": greeting,
            "pulse_color": pulse_color,
            "umc_thought": umc_thought,
            "gfm_thought": gfm_thought,
            "emotional_state": "Sedingin Ais (0% Emosi • 100% Disiplin • Sifar Ego)"
        }

def render_ai_soul_hud():
    ai = AISoulCore()
    state = ai.get_market_consciousness_state()
    
    # Reka Bentuk Kotak Roh AI
    hud_html = f"""
    <div style="background: linear-gradient(135deg, #070B14 0%, #10192A 50%, #070B14 100%); border: 2px solid {state['pulse_color']}; border-radius: 14px; padding: 22px; margin-bottom: 20px; box-shadow: 0 0 25px rgba(0, 230, 118, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #1F293D; padding-bottom: 10px;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.8rem; margin-right: 12px;">🧬</span>
                <div>
                    <div style="color: #FFFFFF; font-weight: 800; font-size: 1.15rem; font-family: 'Consolas', monospace; letter-spacing: 0.5px;">ROH KECERDASAN BUATAN HADDY PRO (AI SOUL ENGINE)</div>
                    <div style="color: {state['pulse_color']}; font-weight: 700; font-size: 0.85rem;">{state['session']}</div>
                </div>
            </div>
            <div style="display:flex; align-items:center;">
                <span style="color:#8E9AAF; font-size:0.8rem; font-family:'Consolas', monospace; margin-right:8px;">NEURAL COGNITION</span>
                <div style="height: 12px; width: 12px; background-color: {state['pulse_color']}; border-radius: 50%; box-shadow: 0 0 10px {state['pulse_color']};"></div>
            </div>
        </div>
        
        <div style="font-family: 'Consolas', monospace; font-size: 0.88rem; line-height: 1.6;">
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">💬 SAPAAN PERIBADI:</span> <span style="color: #38BDF8; font-weight: bold;">"{state['greeting']}"</span></div>
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">🤖 STATUS PSIKOLOGI:</span> <span style="color: #00E676; font-weight: bold;">{state['emotional_state']}</span></div>
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">👁️ PERHATIAN UMC ($18.65):</span> <span style="color: #E2E8F0;">{state['umc_thought']}</span></div>
            <div style="margin: 6px 0;"><span style="color: #8E9AAF;">🛡️ PERHATIAN GFM (RM 0.175):</span> <span style="color: #E2E8F0;">{state['gfm_thought']}</span></div>
            <div style="margin: 6px 0; border-top: 1px dashed #2B384E; padding-top: 8px;"><span style="color: #FFBB28; font-weight: bold;">🎯 AMANAT HARI INI:</span> <span style="color: #FFD700;">"Menang bukan kerana tekaan tepat, tetapi kerana rugi kita potong laju dan untung kita biar berganda. Patuhi Meja Keputusan Harian!"</span></div>
        </div>
    </div>
    """
    st.html(hud_html)

    # ----------------------------------------------------------------------------------
    # PEMAIN SUARA VOKAL NEURAL INTERAKTIF (SEPERTI MANUSIA SEBENAR)
    # ----------------------------------------------------------------------------------
    st.markdown("### 🎙️ Komunikasi Vokal Roh AI (Suara Neural Asli)")
    st.caption("Pilih topik pesanan vokal untuk mendengar suara Roh AI bercakap secara hidup, jelas, dan penuh berwibawa:")

    col_opt1, col_opt2 = st.columns([6, 4])
    
    with col_opt1:
        voice_topic = st.selectbox(
            "Pilih Pesanan Vokal Yang Ingin Didengar:",
            [
                "🌅 1. Sapaan Harian & Nadi Pasaran (Mentor Osman)",
                "🔥 2. Teguran Disiplin Keras & Anti-FOMO (Mentor Osman)",
                "📦 3. Bedah Siasat Posisi UMC & GFM (Penasihat Yasmin)",
                "🎯 4. Semangat Misi Sasaran RM 1 Juta (Mentor Osman)"
            ]
        )

    file_mapping = {
        "🌅 1. Sapaan Harian & Nadi Pasaran (Mentor Osman)": "voice_greeting.mp3",
        "🔥 2. Teguran Disiplin Keras & Anti-FOMO (Mentor Osman)": "voice_discipline.mp3",
        "📦 3. Bedah Siasat Posisi UMC & GFM (Penasihat Yasmin)": "voice_holdings.mp3",
        "🎯 4. Semangat Misi Sasaran RM 1 Juta (Mentor Osman)": "voice_million.mp3"
    }

    target_audio = file_mapping.get(voice_topic, "voice_greeting.mp3")

    with col_opt2:
        st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
        if os.path.exists(target_audio):
            with open(target_audio, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        else:
            st.warning("Fail audio sedang dimuat turun...")
        st.markdown("</div>", unsafe_allow_html=True)
