from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_TAR_MAGIC = b"ustar"

@register
class TAREngine(EngineBase):
    name = "tar"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        has_magic = len(payload) > 262 and payload[257:262] == _TAR_MAGIC
        conf, bd = weighted_confidence([
            ("magic", has_magic, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/x-tar",
                extension="tar",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
