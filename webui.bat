@echo off
chcp 65001 > nul
echo Starting TTS Standalone WebUI...
streamlit run webui/Main.py
pause

