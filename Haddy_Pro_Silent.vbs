Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\haddy_pro-millx_terminalv1 && .\.venv\Scripts\activate.bat && .\.venv\Scripts\python.exe -m streamlit run app.py", 0, False
WScript.Sleep 2500
WshShell.Run "http://localhost:8501"
