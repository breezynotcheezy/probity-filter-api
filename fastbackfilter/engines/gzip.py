from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_GZIP_MAGIC = b"\x1f\x8b"

@register
class GzipEngine(EngineBase):
    name = "gzip"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        has_magic = payload.startswith(_GZIP_MAGIC)
        conf, bd = weighted_confidence([
            ("magic", has_magic, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/gzip",
                extension="gz",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
