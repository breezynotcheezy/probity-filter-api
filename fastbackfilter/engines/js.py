from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_SHEBANGS = [b"#!/usr/bin/env node", b"#!/usr/bin/node"]
_KEYWORDS = [b"function", b"var ", b"let ", b"const "]

@register
class JSEngine(EngineBase):
    name = "js"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        lines = payload.splitlines()[:2]
        has_shebang = any(line.startswith(b"#!") and b"node" in line.lower() for line in lines)
        text = payload[:512]
        has_kw = any(k in text for k in _KEYWORDS)
        conf, bd = weighted_confidence([
            ("shebang", has_shebang, 0.6),
            ("keyword", has_kw, 0.4),
        ])
        if conf:
            cand = Candidate(
                media_type="application/javascript",
                extension="js",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
