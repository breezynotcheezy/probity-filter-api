from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
import csv, io

@register
class CSVEngine(EngineBase):
    name = "csv"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="replace")
            sample = text.splitlines()
            if not sample:
                return Result(candidates=[])

            sample_text = "\n".join(sample[:10])  # try up to 10 lines
            dialect = csv.Sniffer().sniff(sample_text)
            has_header = csv.Sniffer().has_header(sample_text)
            reader = csv.reader(io.StringIO(sample_text), dialect)
            row_lengths = {len(row) for row in reader if row}
            if len(row_lengths) == 1 and list(row_lengths)[0] > 1:
                confidence = 0.95 if has_header else 0.90
                return Result(candidates=[
                    Candidate(media_type="text/csv", extension="csv", confidence=confidence)
                ])
        except Exception:
            pass
        return Result(candidates=[])
