from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_MAGIC = b"RIDX"

@register
class GitRevEngine(EngineBase):
    name = "rev"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        has_magic = payload.startswith(_MAGIC)
        conf, bd = weighted_confidence([
            ("magic", has_magic, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/x-git-rev-index",
                extension="rev",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
