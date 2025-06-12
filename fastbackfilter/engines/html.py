from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_HTML_MAGIC = b"<html"

@register
class HTMLEngine(EngineBase):
    name = "html"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        window = payload[:32].lower()
        has_tag = _HTML_MAGIC in window
        conf, bd = weighted_confidence([
            ("tag", has_tag, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="text/html",
                extension="html",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
