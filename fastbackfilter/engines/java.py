from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_KEYWORDS = [b"public class", b"import java.", b"package "]

@register
class JavaEngine(EngineBase):
    name = "java"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        text = payload[:512]
        if any(k in text for k in _KEYWORDS):
            cand = Candidate(media_type="text/x-java-source", extension="java", confidence=0.8)
            return Result(candidates=[cand])
        return Result(candidates=[])
