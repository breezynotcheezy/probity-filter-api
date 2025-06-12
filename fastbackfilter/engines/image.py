from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

@register
class ImageEngine(EngineBase):
    name = "image"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        jpeg = payload.startswith(b"\xff\xd8\xff")
        gif = payload.startswith(b"GIF87a") or payload.startswith(b"GIF89a")
        if jpeg:
            conf, bd = weighted_confidence([("jpeg", True, 1.0)])
            cand = Candidate(
                media_type="image/jpeg",
                extension="jpg",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        if gif:
            conf, bd = weighted_confidence([("gif", True, 1.0)])
            cand = Candidate(
                media_type="image/gif",
                extension="gif",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
