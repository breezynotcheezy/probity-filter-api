from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class WAVEngine(EngineBase):
    name = "wav"
    cost = 0.1
    _MAGIC = b"RIFF"
    _FMT = b"WAVE"

    def sniff(self, payload: bytes) -> Result:
        has_riff = len(payload) >= 12 and payload[:4] == self._MAGIC
        has_wave = len(payload) >= 12 and payload[8:12] == self._FMT
        conf, bd = weighted_confidence([
            ("riff", has_riff, 0.5),
            ("wave", has_wave, 0.5),
        ])
        if conf:
            cand = Candidate(
                media_type="audio/wav",
                extension="wav",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
