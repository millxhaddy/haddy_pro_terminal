@echo off
title Haddy Pro - Terminal Millx (AES-256 Vault)
color 0A
echo ========================================================
echo   MELANCARKAN HADDY PRO TERMINAL MILLX (PRIVATE VAULT)
echo ========================================================
echo.
cd /d "C:\haddy_pro-millx_terminalv1"
echo Mengaktifkan Persekitaran Python (.venv)...
call .\.venv\Scripts\activate.bat
echo Memulakan Enjin Streamlit...
start "" "http://localhost:8501"
.\.venv\Scripts\python.exe -m streamlit run app.py
pause
