from __future__ import annotations
from typing import Iterable, Tuple, Dict

def weighted_confidence(features: Iterable[Tuple[str, bool, float]]) -> Tuple[float, Dict[str, float] | None]:
    """Return confidence score and breakdown based on weighted features."""
    total = 0.0
    conf = 0.0
    breakdown: Dict[str, float] = {}
    for name, present, weight in features:
        total += weight
        if present:
            conf += weight
            breakdown[name] = weight
    if total == 0:
        return 0.0, None
    score = conf / total
    return round(score, 2), (breakdown or None)
