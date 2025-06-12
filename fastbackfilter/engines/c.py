from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_KEYWORDS = [b"#include", b"int main", b"void main", b"printf("]

@register
class CEngine(EngineBase):
    name = "c"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        text = payload[:512]
        has_kw = any(k in text for k in _KEYWORDS)
        conf, bd = weighted_confidence([
            ("keyword", has_kw, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="text/x-c",
                extension="c",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
