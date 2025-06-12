from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_KEYWORDS = [b"#include", b"int main", b"void main", b"printf("]

@register
class CEngine(EngineBase):
    name = "c"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        text = payload[:512]
        if any(k in text for k in _KEYWORDS):
            cand = Candidate(media_type="text/x-c", extension="c", confidence=0.8)
            return Result(candidates=[cand])
        return Result(candidates=[])
