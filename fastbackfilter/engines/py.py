from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_SHEBANGS = [b"#!/usr/bin/env python", b"#!/usr/bin/python", b"#!/bin/python"]
_KEYWORDS = [b"def ", b"import ", b"class "]

@register
class PyEngine(EngineBase):
    name = "py"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        lines = payload.splitlines()[:2]
        for line in lines:
            if line.startswith(b"#!") and b"python" in line.lower():
                cand = Candidate(media_type="text/x-python", extension="py", confidence=0.95)
                return Result(candidates=[cand])
        text = payload[:256]
        if any(k in text for k in _KEYWORDS):
            cand = Candidate(media_type="text/x-python", extension="py", confidence=0.8)
            return Result(candidates=[cand])
        return Result(candidates=[])
