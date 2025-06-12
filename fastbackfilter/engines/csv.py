from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class CSVEngine(EngineBase):
    name = "csv"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        sample = payload.splitlines()[:2]
        has_comma = bool(sample and any(b"," in line for line in sample))
        conf, bd = weighted_confidence([
            ("comma", has_comma, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="text/csv",
                extension="csv",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
