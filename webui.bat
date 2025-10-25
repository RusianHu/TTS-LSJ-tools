@echo off
chcp 65001 > nul
echo Starting TTS-LSJ-Tools WebUI...
streamlit run webui/Main.py
pause
