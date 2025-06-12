from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_SHEBANGS = [b"#!/usr/bin/env node", b"#!/usr/bin/node"]
_KEYWORDS = [b"function", b"var ", b"let ", b"const "]

@register
class JSEngine(EngineBase):
    name = "js"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        lines = payload.splitlines()[:2]
        for line in lines:
            if line.startswith(b"#!") and b"node" in line.lower():
                cand = Candidate(media_type="application/javascript", extension="js", confidence=0.95)
                return Result(candidates=[cand])
        text = payload[:512]
        if any(k in text for k in _KEYWORDS):
            cand = Candidate(media_type="application/javascript", extension="js", confidence=0.8)
            return Result(candidates=[cand])
        return Result(candidates=[])
