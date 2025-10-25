# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
from typing import Union
from xml.sax.saxutils import unescape

from edge_tts import SubMaker, submaker
from edge_tts.submaker import mktimestamp
from loguru import logger
from moviepy.video.tools import subtitles

from app.services.tts_engine_base import EngineRegistry, TTSRequest
from app.services.azure_engines import (
    AzureTTSV1Engine,
    AzureTTSV2Engine,
    convert_rate_to_percent,
    get_all_azure_voices,
    is_azure_v2_voice,
    parse_voice_name,
)
from app.services.siliconflow_engine import (
    SiliconFlowEngine,
    get_siliconflow_voices,
    is_siliconflow_voice,
)
from app.utils import utils

_ENGINE_REGISTRY = EngineRegistry(
    [
        AzureTTSV2Engine(),
        SiliconFlowEngine(),
        AzureTTSV1Engine(),
    ]
)


def get_registered_engine(engine_id: str):
    return _ENGINE_REGISTRY.get(engine_id)


def get_registered_engines():
    return _ENGINE_REGISTRY.all()


def tts(
    text: str,
    voice_name: str,
    voice_rate: float,
    voice_file: str,
    voice_volume: float = 1.0,
) -> Union[SubMaker, None]:
    """
    根据声音名称自动匹配合适的引擎并执行合成。
    """

    request = TTSRequest(
        text=text,
        voice_name=voice_name,
        voice_rate=voice_rate,
        voice_volume=voice_volume,
        voice_file=voice_file,
    )

    engine = _ENGINE_REGISTRY.find_by_voice(voice_name)
    if engine is None:
        # 默认兜底使用 Azure V1
        engine = _ENGINE_REGISTRY.get(AzureTTSV1Engine.engine_id)

    if engine is None:
        logger.error(f"no tts engine matched voice: {voice_name}")
        return None

    normalized_voice = engine.normalize_voice_name(request.voice_name)
    request.voice_name = normalized_voice
    return engine.synthesize(request)


def _format_text(text: str) -> str:
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("{", " ")
    text = text.replace("}", " ")
    text = text.strip()
    return text


def create_subtitle(sub_maker: submaker.SubMaker, text: str, subtitle_file: str):
    """
    优化字幕文件
    1. 将字幕文件按照标点符号分割成多行
    2. 逐行匹配字幕文件中的文本
    3. 生成新的字幕文件
    """

    text = _format_text(text)

    def formatter(idx: int, start_time: float, end_time: float, sub_text: str) -> str:
        start_t = mktimestamp(start_time).replace(".", ",")
        end_t = mktimestamp(end_time).replace(".", ",")
        return f"{idx}\n{start_t} --> {end_t}\n{sub_text}\n"

    start_time = -1.0
    sub_items = []
    sub_index = 0

    script_lines = utils.split_string_by_punctuations(text)

    def match_line(_sub_line: str, _sub_index: int):
        if len(script_lines) <= _sub_index:
            return ""

        _line = script_lines[_sub_index]
        if _sub_line == _line:
            return script_lines[_sub_index].strip()

        _sub_line_ = re.sub(r"[^\w\s]", "", _sub_line)
        _line_ = re.sub(r"[^\w\s]", "", _line)
        if _sub_line_ == _line_:
            return _line_.strip()

        _sub_line_ = re.sub(r"\W+", "", _sub_line)
        _line_ = re.sub(r"\W+", "", _line)
        if _sub_line_ == _line_:
            return _line.strip()

        return ""

    sub_line = ""

    try:
        for _, (offset, sub) in enumerate(zip(sub_maker.offset, sub_maker.subs)):
            _start_time, end_time = offset
            if start_time < 0:
                start_time = _start_time

            sub = unescape(sub)
            sub_line += sub
            sub_text = match_line(sub_line, sub_index)
            if sub_text:
                sub_index += 1
                line = formatter(
                    idx=sub_index,
                    start_time=start_time,
                    end_time=end_time,
                    sub_text=sub_text,
                )
                sub_items.append(line)
                start_time = -1.0
                sub_line = ""

        if len(sub_items) == len(script_lines):
            with open(subtitle_file, "w", encoding="utf-8") as file:
                file.write("\n".join(sub_items) + "\n")
            try:
                sbs = subtitles.file_to_subtitles(subtitle_file, encoding="utf-8")
                duration = max([tb for ((ta, tb), txt) in sbs])
                logger.info(
                    f"completed, subtitle file created: {subtitle_file}, duration: {duration}"
                )
            except Exception as exc:
                logger.error(f"failed, error: {str(exc)}")
                os.remove(subtitle_file)
        else:
            logger.warning(
                f"failed, sub_items len: {len(sub_items)}, script_lines len: {len(script_lines)}"
            )

    except Exception as exc:
        logger.error(f"failed, error: {str(exc)}")


def get_audio_duration(sub_maker: submaker.SubMaker):
    """
    获取音频时长
    """
    if not sub_maker.offset:
        return 0.0
    return sub_maker.offset[-1][1] / 10000000


__all__ = [
    "convert_rate_to_percent",
    "create_subtitle",
    "get_all_azure_voices",
    "get_audio_duration",
    "get_registered_engine",
    "get_registered_engines",
    "get_siliconflow_voices",
    "is_azure_v2_voice",
    "is_siliconflow_voice",
    "parse_voice_name",
    "tts",
]
