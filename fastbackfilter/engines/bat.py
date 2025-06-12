from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class BATEngine(EngineBase):
    name = "bat"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        first_line = payload.splitlines()[:1]
        has_cmd = False
        if first_line:
            line = first_line[0].lower()
            has_cmd = line.startswith((b"@echo", b"echo", b"rem", b"::"))
        conf, bd = weighted_confidence([
            ("command", has_cmd, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/x-bat",
                extension="bat",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
