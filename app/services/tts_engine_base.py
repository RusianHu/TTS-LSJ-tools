# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional, Union

from edge_tts import SubMaker


@dataclass(slots=True)
class TTSRequest:
    """
    描述一次文本转语音的参数集合。
    """

    text: str
    voice_name: str
    voice_rate: float
    voice_volume: float
    voice_file: str


class TTSEngine(ABC):
    """
    所有 TTS 引擎的统一抽象。
    """

    engine_id: str

    def __init__(self) -> None:
        if not getattr(self, "engine_id", None):
            raise ValueError("TTSEngine 子类必须定义 engine_id 属性")

    @abstractmethod
    def supports_voice(self, voice_name: str) -> bool:
        """
        判断当前引擎是否可以处理给定的声音名称。
        """

    def normalize_voice_name(self, voice_name: str) -> str:
        """
        允许子类根据需要预处理声音名称，默认直接返回原值。
        """

        return voice_name

    @abstractmethod
    def synthesize(self, request: TTSRequest) -> Union[SubMaker, None]:
        """
        执行语音合成，返回 SubMaker 或 None。
        """

    def list_voices(self) -> list[str]:
        """
        返回当前引擎支持的声音列表，默认返回空列表。
        """

        return []


class EngineRegistry:
    """
    简单的引擎注册表，方便根据声音名称或 engine_id 获取对应实现。
    """

    def __init__(self, engines: Iterable[TTSEngine]):
        self._engines = {engine.engine_id: engine for engine in engines}

    def get(self, engine_id: str) -> Optional[TTSEngine]:
        return self._engines.get(engine_id)

    def all(self) -> list[TTSEngine]:
        return list(self._engines.values())

    def find_by_voice(self, voice_name: str) -> Optional[TTSEngine]:
        for engine in self._engines.values():
            if engine.supports_voice(voice_name):
                return engine
        return None

