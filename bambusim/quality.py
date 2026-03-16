from __future__ import annotations

from typing import Any


def calc_quality_score(params: dict[str, Any], *, nozzle_temp: float) -> float:
    score = 100.0

    speed = float(params.get("speed", 100))
    layer = float(params.get("layer_height", 0.2))
    cooling = float(params.get("cooling", 50))

    if speed > 100:
        score -= min(30.0, (speed - 100) * 0.2)
    else:
        score += min(5.0, (100 - score) * 0.02)

    if layer > 0.2:
        score -= min(25.0, (layer - 0.2) * 100)
    else:
        score += min(5.0, (0.2 - layer) * 50)

    score -= abs(cooling - 50) * 0.2
    score -= min(20.0, abs(nozzle_temp - 210) * 0.2)

    score = max(0.0, min(100.0, score))
    return round(score, 2)
