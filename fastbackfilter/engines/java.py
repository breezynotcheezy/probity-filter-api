from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_KEYWORDS = [b"public class", b"import java.", b"package "]

@register
class JavaEngine(EngineBase):
    name = "java"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        text = payload[:512]
        has_kw = any(k in text for k in _KEYWORDS)
        conf, bd = weighted_confidence([
            ("keyword", has_kw, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="text/x-java-source",
                extension="java",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
