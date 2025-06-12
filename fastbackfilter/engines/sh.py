from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_SHEBANGS = [b"#!/bin/sh", b"#!/bin/bash", b"#!/usr/bin/env bash", b"#!/usr/bin/env sh"]

@register
class SHEngine(EngineBase):
    name = "sh"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        has_magic = any(payload.startswith(magic) for magic in _SHEBANGS)
        conf, bd = weighted_confidence([
            ("shebang", has_magic, 1.0),
        ])
        if conf:
            cand = Candidate(
                media_type="application/x-sh",
                extension="sh",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
