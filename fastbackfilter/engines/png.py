from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

@register
class PNGEngine(EngineBase):
    name = "png"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        has_magic = payload.startswith(_PNG_MAGIC)
        conf, bd = weighted_confidence([
            ("magic", has_magic, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="image/png",
                extension="png",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
