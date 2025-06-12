from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class JSONEngine(EngineBase):
    name = "json"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        window = payload.lstrip()[:1]
        has_brace = window in (b"{", b"[")
        conf, bd = weighted_confidence([
            ("brace", has_brace, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/json",
                extension="json",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
