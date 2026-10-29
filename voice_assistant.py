"""
HADDY PRO - TERMINAL MILLX
MODUL 1: KAWALAN SUARA & PEMBANTU VOKAL AI (VOICE-ACTIVATED TRADING ASSISTANT)
"""

import streamlit as st
# import streamlit.components.v1 as components

def process_voice_query(command: str) -> str:
    cmd = command.lower().strip()
    if "tenaga" in cmd:
        return "Saham Tenaga Nasional kini berada pada paras rujukan RM 12.75. Zon sokongan entri di RM 12.50 dan sasaran untung RM 14.38."
    elif "nvidia" in cmd or "nvda" in cmd:
        return "Nvidia berada pada paras 141.20 Dolar. Fasa Wyckoff Mark-Up dengan aliran jerung 94 peratus."
    elif "umc" in cmd:
        return "Posisi aktif UMC sedang dipegang pada kos 19.26 Dolar. Had lantai trailing stop ketat berada pada 18.00 Dolar."
    elif "gfm" in cmd:
        return "GFM Services berada pada paras pulang modal RM 0.175 dengan pegangan 56,400 unit."
    elif "baki" in cmd or "modal" in cmd:
        return "Modal bersih terkumpul akaun anda adalah RM 42,497.80 dengan kadar pengekalan modal 50.1 peratus."
    else:
        return f"Arahan '{command}' telah direkodkan. Sila semak Meja Keputusan Harian untuk butiran penuh."

def render_voice_assistant_ui():
    st.subheader("🎙️ Kawalan Suara & Pembantu Vokal AI (Voice Assistant)")
    st.caption("Gunakan suara untuk menyemak harga saham, kedudukan portfolio, dan disiplin SOP tanpa menaip.")

    voice_html = """
    <div style="background:#161D2B; padding:20px; border-radius:12px; border:1px solid #2B384E; text-align:center;">
        <button id="voiceBtn" style="background:#00E676; color:#0E1117; font-weight:bold; font-size:16px; padding:12px 24px; border:none; border-radius:30px; cursor:pointer;">
            🎤 Tekan & Mula Bercakap
        </button>
        <p id="speechOutput" style="color:#8E9AAF; margin-top:12px; font-size:14px;">Status: Menunggu arahan suara...</p>
    </div>

    <script>
        const btn = document.getElementById('voiceBtn');
        const output = document.getElementById('speechOutput');

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'ms-MY';
            recognition.continuous = false;
            recognition.interimResults = false;

            btn.onclick = () => {
                recognition.start();
                output.innerText = "Status: 🔴 Sedang mendengar... Sila sebut nama saham (cth: Tenaga, Nvidia, UMC)";
                btn.style.background = "#FF5252";
            };

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                output.innerText = "Arahan Dikesan: \"" + text + "\"";
                btn.style.background = "#00E676";
                
                // Balasan Vokal Suara (Speech Synthesis)
                const synth = window.speechSynthesis;
                const utter = new SpeechSynthesisUtterance("Menerima arahan untuk " + text);
                utter.lang = 'ms-MY';
                synth.speak(utter);
            };

            recognition.onerror = () => {
                output.innerText = "Status: ⚠️ Ralat pengecaman suara. Sila cuba lagi.";
                btn.style.background = "#00E676";
            };
        } else {
            output.innerText = "Pelayar web ini tidak menyokong Web Speech API. Sila gunakan Google Chrome.";
        }
    </script>
    """
    st.html(voice_html) if hasattr(st, 'html') else st.iframe(voice_html, height=180)

    st.markdown("---")
    st.markdown("#### ⌨️ Input Ujian Pantas (Simulasi Suara):")
    sim_col1, sim_col2 = st.columns([7, 3])
    with sim_col1:
        query_text = st.text_input("Atau taip arahan teks vokal di sini:", "Semak harga Tenaga")
    with sim_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        ask_btn = st.button("Jawab Pertanyaan", width="stretch")

    if ask_btn and query_text:
        jawapan = process_voice_query(query_text)
        st.info(f"🤖 **Maklum Balas AI:** {jawapan}")
