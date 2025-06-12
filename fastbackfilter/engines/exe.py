from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
from .utils import weighted_confidence

_MZ = b"MZ"

@register
class EXEEngine(EngineBase):
    name = "exe"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        has_mz = payload.startswith(_MZ)
        has_pe = False
        if len(payload) > 0x40 and has_mz:
            off = int.from_bytes(payload[0x3C:0x40], "little", signed=False)
            if len(payload) >= off + 2 and payload[off:off + 2] == b"PE":
                has_pe = True
        conf, bd = weighted_confidence([
            ("mz", has_mz, 0.6),
            ("pe", has_pe, 0.4),
        ])
        if conf:
            cand = Candidate(
                media_type="application/vnd.microsoft.portable-executable",
                extension="exe",
                confidence=conf,
                breakdown=bd,
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
