from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class MP4Engine(EngineBase):
    name = "mp4"
    cost = 0.2
    _MAGIC = b"ftyp"

    def sniff(self, payload: bytes) -> Result:
        has_ftyp = len(payload) >= 12 and payload[4:8] == self._MAGIC
        conf, bd = weighted_confidence([
            ("ftyp", has_ftyp, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="video/mp4",
                extension="mp4",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
