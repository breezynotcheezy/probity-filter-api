from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_MAGIC = b"RIDX"

@register
class GitRevEngine(EngineBase):
    name = "rev"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_MAGIC):
            cand = Candidate(media_type="application/x-git-rev-index", extension="rev", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
