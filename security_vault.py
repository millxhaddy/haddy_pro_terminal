"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL KESELAMATAN VAULT: RECURSIVE SMART KEY DETECTOR & AES-256 (600,000 PBKDF2)
========================================================================================
"""

import hashlib
import hmac
import os
import streamlit as st

PBKDF2_ITERATIONS = 600_000
KEY_LENGTH = 32
VAULT_SALT = b"HaddyProMillx2026SecureSaltKey16"

def derive_password_verifier(passphrase: str, salt: bytes = VAULT_SALT) -> bytes:
    clean_pass = str(passphrase).strip().strip("'").strip('"')
    return hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=clean_pass.encode('utf-8'),
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        dklen=KEY_LENGTH
    )

def find_key_recursively(data):
    """Mencari VAULT_MASTER_KEY di semua peringkat sub-table TOML"""
    if isinstance(data, dict) or hasattr(data, "items"):
        for k, v in data.items():
            if str(k).strip() == "VAULT_MASTER_KEY":
                return str(v).strip().strip("'").strip('"')
            if isinstance(v, (dict, list)) or hasattr(v, "items"):
                res = find_key_recursively(v)
                if res:
                    return res
    return None

def get_master_configured_key() -> str:
    # 1. Cari dalam Streamlit Secrets (Root & Nested)
    try:
        if hasattr(st, "secrets"):
            found = find_key_recursively(st.secrets)
            if found:
                return found
    except Exception:
        pass
    
    # 2. Cari dalam fail tempatan .streamlit/secrets.toml
    try:
        import tomllib
        sec_path = os.path.join(".streamlit", "secrets.toml")
        if os.path.exists(sec_path):
            with open(sec_path, "r", encoding="utf-8-sig") as f:
                cfg = tomllib.loads(f.read())
            found = find_key_recursively(cfg)
            if found:
                return found
    except Exception:
        pass
        
    return ""

def verify_vault_authentication():
    configured_key = get_master_configured_key()
    if not configured_key:
        st.error(
            "Vault dikunci: tetapkan VAULT_MASTER_KEY dalam Streamlit Secrets "
            "sebelum membuka aplikasi."
        )
        st.stop()

    st.session_state.pop("master_key", None)
    if "vault_authenticated" not in st.session_state:
        st.session_state["vault_authenticated"] = False

    if not st.session_state["vault_authenticated"]:
        st.markdown("""
        <style>
            .lock-card {
                background: linear-gradient(135deg, #1A1F2C 0%, #0E1117 100%);
                border: 2px solid #00E676;
                border-radius: 16px;
                padding: 35px 30px;
                max-width: 520px;
                margin: 40px auto;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0, 230, 118, 0.2);
            }
            .shield-icon { font-size: 3.5rem; margin-bottom: 10px; }
            .cipher-badge {
                background-color: rgba(0, 230, 118, 0.15);
                color: #00E676;
                border: 1px solid rgba(0, 230, 118, 0.4);
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 700;
            }
        </style>
        """, unsafe_allow_html=True)

        _, col_center, _ = st.columns([1, 2, 1])
        with col_center:
            st.markdown("""
            <div class="lock-card">
                <div class="shield-icon">🛡️</div>
                <h2 style="color: #FFFFFF; margin-bottom: 5px;">HADDY PRO VAULT</h2>
                <span class="cipher-badge">PENGESAHAN KATA LALUAN • PBKDF2-HMAC-SHA256</span>
                <p style="color: #8E9AAF; font-size: 0.88rem; margin-top: 15px;">
                    Ini ialah pintu kawalan akses aplikasi, bukan penyulitan data.
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("vault_login_form"):
                passphrase_input = st.text_input(
                    "Kata laluan akses:",
                    type="password",
                    placeholder="Masukkan kata laluan..."
                )
                submitted = st.form_submit_button(
                    "Sahkan dan buka aplikasi",
                    width="stretch",
                )

                if submitted:
                    with st.spinner("Mengesahkan kata laluan..."):
                        derived_test = derive_password_verifier(passphrase_input)
                        derived_target = derive_password_verifier(configured_key)

                        if hmac.compare_digest(derived_test, derived_target):
                            st.session_state["vault_authenticated"] = True
                            st.success("Kata laluan disahkan.")
                            st.rerun()
                        else:
                            st.error("Akses ditolak: kata laluan tidak sah.")

        st.stop()
