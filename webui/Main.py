# -*- coding: utf-8 -*-
import os
import sys
from uuid import uuid4

import streamlit as st
from loguru import logger

# Add the root directory of the project to the system path
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.config import config
from app.services import voice
from app.utils import utils

st.set_page_config(
    page_title="TTS Standalone",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="auto",
)

streamlit_style = """
<style>
h1 {
    padding-top: 0 !important;
}
</style>
"""
st.markdown(streamlit_style, unsafe_allow_html=True)

i18n_dir = os.path.join(root_dir, "webui", "i18n")
system_locale = utils.get_system_locale()

if "ui_language" not in st.session_state:
    st.session_state["ui_language"] = config.ui.get("language", system_locale)

locales = utils.load_locales(i18n_dir)

# 创建顶部栏
title_col, lang_col = st.columns([3, 1])

with title_col:
    st.title(f"🎙️ TTS Standalone v{config.project_version}")

with lang_col:
    display_languages = []
    selected_index = 0
    for i, code in enumerate(locales.keys()):
        display_languages.append(f"{code} - {locales[code].get('Language')}")
        if code == st.session_state.get("ui_language", ""):
            selected_index = i

    selected_language = st.selectbox(
        "Language / 语言",
        options=display_languages,
        index=selected_index,
        key="top_language_selector",
        label_visibility="collapsed",
    )
    if selected_language:
        code = selected_language.split(" - ")[0].strip()
        st.session_state["ui_language"] = code
        config.ui["language"] = code


def tr(key):
    loc = locales.get(st.session_state["ui_language"], {})
    return loc.get("Translation", {}).get(key, key)


# 主界面
st.markdown(f"### {tr('TTS Settings')}")

# TTS服务器选择
tts_servers = [
    ("azure-tts-v1", tr("Azure TTS V1")),
    ("azure-tts-v2", tr("Azure TTS V2")),
    ("siliconflow", tr("SiliconFlow")),
]

saved_tts_server = config.ui.get("tts_server", "azure-tts-v1")
saved_tts_server_index = 0
for i, (server_id, _) in enumerate(tts_servers):
    if server_id == saved_tts_server:
        saved_tts_server_index = i
        break

selected_tts_server_index = st.selectbox(
    tr("TTS Server"),
    options=range(len(tts_servers)),
    format_func=lambda x: tts_servers[x][1],
    index=saved_tts_server_index,
)

selected_tts_server = tts_servers[selected_tts_server_index][0]
config.ui["tts_server"] = selected_tts_server

# 根据选择的TTS服务器获取声音列表
filtered_voices = []

if selected_tts_server == "siliconflow":
    filtered_voices = voice.get_siliconflow_voices()
else:
    all_voices = voice.get_all_azure_voices(filter_locals=None)
    for v in all_voices:
        if selected_tts_server == "azure-tts-v2":
            if "V2" in v:
                filtered_voices.append(v)
        else:
            if "V2" not in v:
                filtered_voices.append(v)

friendly_names = {
    v: v.replace("Female", tr("Female"))
    .replace("Male", tr("Male"))
    .replace("Neural", "")
    for v in filtered_voices
}

saved_voice_name = config.ui.get("voice_name", "")
saved_voice_name_index = 0

if saved_voice_name in friendly_names:
    saved_voice_name_index = list(friendly_names.keys()).index(saved_voice_name)
else:
    for i, v in enumerate(filtered_voices):
        if v.lower().startswith(st.session_state["ui_language"].lower()):
            saved_voice_name_index = i
            break

if saved_voice_name_index >= len(friendly_names) and friendly_names:
    saved_voice_name_index = 0

voice_name = ""
if friendly_names:
    selected_friendly_name = st.selectbox(
        tr("Speech Synthesis"),
        options=list(friendly_names.values()),
        index=min(saved_voice_name_index, len(friendly_names) - 1)
        if friendly_names
        else 0,
    )

    voice_name = list(friendly_names.keys())[
        list(friendly_names.values()).index(selected_friendly_name)
    ]
    config.ui["voice_name"] = voice_name
else:
    st.warning(
        tr(
            "No voices available for the selected TTS server. Please select another server."
        )
    )

# 当选择V2版本或者声音是V2声音时，显示服务区域和API key输入框
if selected_tts_server == "azure-tts-v2" or (
    voice_name and voice.is_azure_v2_voice(voice_name)
):
    saved_azure_speech_region = config.azure.get("speech_region", "")
    saved_azure_speech_key = config.azure.get("speech_key", "")
    azure_speech_region = st.text_input(
        tr("Speech Region"),
        value=saved_azure_speech_region,
        key="azure_speech_region_input",
    )
    azure_speech_key = st.text_input(
        tr("Speech Key"),
        value=saved_azure_speech_key,
        type="password",
        key="azure_speech_key_input",
    )
    config.azure["speech_region"] = azure_speech_region
    config.azure["speech_key"] = azure_speech_key

# 当选择硅基流动时，显示API key输入框
if selected_tts_server == "siliconflow" or (
    voice_name and voice.is_siliconflow_voice(voice_name)
):
    saved_siliconflow_api_key = config.siliconflow.get("api_key", "")

    siliconflow_api_key = st.text_input(
        tr("SiliconFlow API Key"),
        value=saved_siliconflow_api_key,
        type="password",
        key="siliconflow_api_key_input",
    )

    st.info(
        tr("SiliconFlow TTS Settings")
        + ":\n"
        + "- "
        + tr("Speed: Range [0.25, 4.0], default is 1.0")
        + "\n"
        + "- "
        + tr("Volume: Uses Speech Volume setting, default 1.0 maps to gain 0")
    )

    config.siliconflow["api_key"] = siliconflow_api_key

voice_volume = st.selectbox(
    tr("Speech Volume"),
    options=[0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0],
    index=2,
)

voice_rate = st.selectbox(
    tr("Speech Rate"),
    options=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.0],
    index=2,
)

# 文本输入
st.markdown("---")
text_to_convert = st.text_area(
    tr("Text to Convert"),
    height=200,
    placeholder=tr("Enter the text you want to convert to speech"),
)

# 生成按钮
col1, col2 = st.columns([1, 4])
with col1:
    generate_button = st.button(tr("Generate Speech"), use_container_width=True, type="primary")
with col2:
    if voice_name:
        play_button = st.button(tr("Play Voice"), use_container_width=True)
    else:
        play_button = False

# 处理试听按钮
if play_button and voice_name:
    play_content = text_to_convert if text_to_convert else tr("Voice Example")
    with st.spinner(tr("Synthesizing Voice")):
        temp_dir = utils.storage_dir("temp", create=True)
        audio_file = os.path.join(temp_dir, f"tmp-voice-{str(uuid4())}.mp3")
        sub_maker = voice.tts(
            text=play_content,
            voice_name=voice_name,
            voice_rate=voice_rate,
            voice_file=audio_file,
            voice_volume=voice_volume,
        )

        if sub_maker and os.path.exists(audio_file):
            st.audio(audio_file, format="audio/mp3")
            if os.path.exists(audio_file):
                os.remove(audio_file)
        else:
            st.error(tr("Speech synthesis failed"))

# 处理生成按钮
if generate_button:
    if not text_to_convert:
        st.error(tr("Please enter text to convert"))
    elif not voice_name:
        st.error(tr("Please select a voice"))
    else:
        # 检查必要的配置
        if selected_tts_server == "azure-tts-v2" or voice.is_azure_v2_voice(voice_name):
            if not config.azure.get("speech_key") or not config.azure.get("speech_region"):
                st.error(tr("Azure Speech Key and Region are required for Azure TTS V2"))
                st.stop()
        
        if selected_tts_server == "siliconflow" or voice.is_siliconflow_voice(voice_name):
            if not config.siliconflow.get("api_key"):
                st.error(tr("SiliconFlow API Key is required"))
                st.stop()
        
        with st.spinner(tr("Synthesizing Voice")):
            output_dir = utils.storage_dir("output", create=True)
            audio_file = os.path.join(output_dir, f"tts-{str(uuid4())}.mp3")
            subtitle_file = audio_file.replace(".mp3", ".srt")
            
            sub_maker = voice.tts(
                text=text_to_convert,
                voice_name=voice_name,
                voice_rate=voice_rate,
                voice_file=audio_file,
                voice_volume=voice_volume,
            )
            
            if sub_maker and os.path.exists(audio_file):
                # 生成字幕
                voice.create_subtitle(sub_maker=sub_maker, text=text_to_convert, subtitle_file=subtitle_file)
                audio_duration = voice.get_audio_duration(sub_maker)
                
                st.success(tr("Speech synthesis completed"))
                st.audio(audio_file, format="audio/mp3")
                
                st.markdown(f"**{tr('Audio Duration')}**: {audio_duration:.2f} {tr('seconds')}")
                
                # 提供下载按钮
                col1, col2 = st.columns(2)
                with col1:
                    with open(audio_file, "rb") as f:
                        st.download_button(
                            label=tr("Download Audio"),
                            data=f,
                            file_name=os.path.basename(audio_file),
                            mime="audio/mp3",
                        )
                
                with col2:
                    if os.path.exists(subtitle_file):
                        with open(subtitle_file, "rb") as f:
                            st.download_button(
                                label=tr("Download Subtitle"),
                                data=f,
                                file_name=os.path.basename(subtitle_file),
                                mime="text/plain",
                            )
            else:
                st.error(tr("Speech synthesis failed"))

# 保存配置
config.save_config()

