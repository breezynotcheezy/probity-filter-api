from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_ID3_MAGIC = b"ID3"

@register
class MP3Engine(EngineBase):
    name = "mp3"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        has_id3 = payload.startswith(_ID3_MAGIC)
        has_frame = payload[:2] == b"\xff\xfb"
        conf, bd = weighted_confidence([
            ("id3", has_id3, 0.8),
            ("frame", has_frame, 0.2),
        ])
        if conf:
            cand = Candidate(
                media_type="audio/mpeg",
                extension="mp3",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
