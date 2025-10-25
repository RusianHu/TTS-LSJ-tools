# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import re
from datetime import datetime
from typing import Union

import edge_tts
from edge_tts import SubMaker
from loguru import logger

from app.config import config

from .tts_engine_base import TTSEngine, TTSRequest

AZURE_VOICES_BLOCK = """
Name: af-ZA-AdriNeural
Gender: Female

Name: af-ZA-WillemNeural
Gender: Male

Name: zh-CN-XiaoxiaoNeural
Gender: Female

Name: zh-CN-XiaoyiNeural
Gender: Female

Name: zh-CN-YunjianNeural
Gender: Male

Name: zh-CN-YunxiNeural
Gender: Male

Name: zh-CN-YunxiaNeural
Gender: Male

Name: zh-CN-YunyangNeural
Gender: Male

Name: zh-CN-liaoning-XiaobeiNeural
Gender: Female

Name: zh-CN-shaanxi-XiaoniNeural
Gender: Female

Name: zh-HK-HiuGaaiNeural
Gender: Female

Name: zh-HK-HiuMaanNeural
Gender: Female

Name: zh-HK-WanLungNeural
Gender: Male

Name: zh-TW-HsiaoChenNeural
Gender: Female

Name: zh-TW-HsiaoYuNeural
Gender: Female

Name: zh-TW-YunJheNeural
Gender: Male

Name: en-US-AnaNeural
Gender: Female

Name: en-US-AndrewNeural
Gender: Male

Name: en-US-AriaNeural
Gender: Female

Name: en-US-AvaNeural
Gender: Female

Name: en-US-BrianNeural
Gender: Male

Name: en-US-ChristopherNeural
Gender: Male

Name: en-US-EmmaNeural
Gender: Female

Name: en-US-EricNeural
Gender: Male

Name: en-US-GuyNeural
Gender: Male

Name: en-US-JennyNeural
Gender: Female

Name: en-US-MichelleNeural
Gender: Female

Name: en-US-RogerNeural
Gender: Male

Name: en-US-SteffanNeural
Gender: Male

Name: ja-JP-KeitaNeural
Gender: Male

Name: ja-JP-NanamiNeural
Gender: Female

Name: ko-KR-InJoonNeural
Gender: Male

Name: ko-KR-SunHiNeural
Gender: Female

Name: de-DE-AmalaNeural
Gender: Female

Name: de-DE-ConradNeural
Gender: Male

Name: de-DE-KatjaNeural
Gender: Female

Name: de-DE-KillianNeural
Gender: Male

Name: fr-FR-DeniseNeural
Gender: Female

Name: fr-FR-EloiseNeural
Gender: Female

Name: fr-FR-HenriNeural
Gender: Male

Name: es-ES-AlvaroNeural
Gender: Male

Name: es-ES-ElviraNeural
Gender: Female

Name: zh-CN-XiaoxiaoMultilingualNeural-V2
Gender: Female

Name: zh-CN-YunxiMultilingualNeural-V2
Gender: Male

Name: en-US-AndrewMultilingualNeural-V2
Gender: Male

Name: en-US-AvaMultilingualNeural-V2
Gender: Female

Name: en-US-BrianMultilingualNeural-V2
Gender: Male

Name: en-US-EmmaMultilingualNeural-V2
Gender: Female

Name: de-DE-FlorianMultilingualNeural-V2
Gender: Male

Name: de-DE-SeraphinaMultilingualNeural-V2
Gender: Female

Name: fr-FR-RemyMultilingualNeural-V2
Gender: Male

Name: fr-FR-VivienneMultilingualNeural-V2
Gender: Female
""".strip()

_VOICE_PATTERN = re.compile(r"Name:\s*(.+)\s*Gender:\s*(.+)\s*", re.MULTILINE)


def get_all_azure_voices(filter_locals=None) -> list[str]:
    voices = []
    matches = _VOICE_PATTERN.findall(AZURE_VOICES_BLOCK)

    for name, gender in matches:
        if filter_locals and any(
            name.lower().startswith(fl.lower()) for fl in filter_locals
        ):
            voices.append(f"{name}-{gender}")
        elif not filter_locals:
            voices.append(f"{name}-{gender}")

    voices.sort()
    return voices


def parse_voice_name(name: str) -> str:
    name = name.replace("-Female", "").replace("-Male", "").strip()
    return name


def is_azure_v2_voice(voice_name: str):
    voice_name = parse_voice_name(voice_name)
    if voice_name.endswith("-V2"):
        return voice_name.replace("-V2", "").strip()
    return ""


def convert_rate_to_percent(rate: float) -> str:
    if rate == 1.0:
        return "+0%"
    percent = round((rate - 1.0) * 100)
    if percent > 0:
        return f"+{percent}%"
    else:
        return f"{percent}%"


class AzureTTSV1Engine(TTSEngine):
    engine_id = "azure-tts-v1"

    def supports_voice(self, voice_name: str) -> bool:
        if not voice_name or voice_name.startswith("siliconflow:"):
            return False
        return not bool(is_azure_v2_voice(voice_name))

    def list_voices(self) -> list[str]:
        return [voice for voice in get_all_azure_voices() if "-V2" not in voice]

    def synthesize(self, request: TTSRequest) -> Union[SubMaker, None]:
        voice_name = parse_voice_name(request.voice_name)
        text = request.text.strip()
        rate_str = convert_rate_to_percent(request.voice_rate)

        for i in range(3):
            try:
                logger.info(f"start, voice name: {voice_name}, try: {i + 1}")

                async def _do() -> SubMaker:
                    communicate = edge_tts.Communicate(text, voice_name, rate=rate_str)
                    sub_maker = edge_tts.SubMaker()
                    with open(request.voice_file, "wb") as file:
                        async for chunk in communicate.stream():
                            if chunk["type"] == "audio":
                                file.write(chunk["data"])
                            elif chunk["type"] == "WordBoundary":
                                sub_maker.create_sub(
                                    (chunk["offset"], chunk["duration"]), chunk["text"]
                                )
                    return sub_maker

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                sub_maker = loop.run_until_complete(_do())
                loop.close()
                logger.success(f"completed, output file: {request.voice_file}")
                return sub_maker
            except Exception as exc:
                logger.error(f"failed, error: {str(exc)}")
        return None


class AzureTTSV2Engine(TTSEngine):
    engine_id = "azure-tts-v2"

    def supports_voice(self, voice_name: str) -> bool:
        return bool(is_azure_v2_voice(voice_name))

    def list_voices(self) -> list[str]:
        return [voice for voice in get_all_azure_voices() if "-V2" in voice]

    def synthesize(self, request: TTSRequest) -> Union[SubMaker, None]:
        azure_voice_name = is_azure_v2_voice(request.voice_name)
        if not azure_voice_name:
            logger.error(f"invalid voice name: {request.voice_name}")
            raise ValueError(f"invalid voice name: {request.voice_name}")
        text = request.text.strip()

        def _format_duration_to_offset(duration) -> int:
            if isinstance(duration, str):
                time_obj = datetime.strptime(duration, "%H:%M:%S.%f")
                milliseconds = (
                    (time_obj.hour * 3600000)
                    + (time_obj.minute * 60000)
                    + (time_obj.second * 1000)
                    + (time_obj.microsecond // 1000)
                )
                return milliseconds * 10000

            if isinstance(duration, int):
                return duration

            return 0

        for i in range(3):
            try:
                logger.info(f"start, voice name: {azure_voice_name}, try: {i + 1}")

                import azure.cognitiveservices.speech as speechsdk

                sub_maker = SubMaker()

                def speech_synthesizer_word_boundary_cb(evt: speechsdk.SessionEventArgs):
                    duration = _format_duration_to_offset(str(evt.duration))
                    offset = _format_duration_to_offset(evt.audio_offset)
                    sub_maker.subs.append(evt.text)
                    sub_maker.offset.append((offset, offset + duration))

                speech_key = config.azure.get("speech_key", "")
                service_region = config.azure.get("speech_region", "")
                if not speech_key or not service_region:
                    logger.error("Azure speech key or region is not set")
                    return None

                audio_config = speechsdk.audio.AudioOutputConfig(
                    filename=request.voice_file, use_default_speaker=True
                )
                speech_config = speechsdk.SpeechConfig(
                    subscription=speech_key, region=service_region
                )
                speech_config.speech_synthesis_voice_name = azure_voice_name
                speech_config.set_property(
                    property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestWordBoundary,
                    value="true",
                )

                speech_config.set_speech_synthesis_output_format(
                    speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
                )
                speech_synthesizer = speechsdk.SpeechSynthesizer(
                    audio_config=audio_config, speech_config=speech_config
                )
                speech_synthesizer.synthesis_word_boundary.connect(
                    speech_synthesizer_word_boundary_cb
                )

                result = speech_synthesizer.speak_text_async(text).get()
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.success(
                        f"azure v2 speech synthesis succeeded: {request.voice_file}"
                    )
                    return sub_maker
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    logger.error(
                        f"azure v2 speech synthesis canceled: {cancellation_details.reason}"
                    )
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        logger.error(
                            f"azure v2 speech synthesis error: {cancellation_details.error_details}"
                        )
                logger.info(f"completed, output file: {request.voice_file}")
            except Exception as exc:
                logger.error(f"failed, error: {str(exc)}")
        return None


__all__ = [
    "AzureTTSV1Engine",
    "AzureTTSV2Engine",
    "convert_rate_to_percent",
    "get_all_azure_voices",
    "is_azure_v2_voice",
    "parse_voice_name",
]

