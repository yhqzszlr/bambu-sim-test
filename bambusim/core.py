from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import copy

from .quality import calc_quality_score
from .faults import apply_fault

Number = int | float

##状态及参数设定
@dataclass
class Bambusim:
    nozzle_temp: float = 25.0
    bed_temp: float = 25.0
    progress: int = 0
    is_printing: bool = False
    is_paused: bool = False
    params: dict[str, Any] = field(default_factory=dict)
    quality_score: Optional[float] = None
    target_nozzle_temp: float = 25.0
    target_bed_temp: float = 25.0

    last_error: Optional[str] = None
    is_connected: bool = False
    history_error: list[str] = field(default_factory=list)

    def get_status(self) -> dict[str, Any]:
        return {
            "nozzle_temp": self.nozzle_temp,
            "bed_temp": self.bed_temp,
            "progress": self.progress,
            "is_printing": self.is_printing,
            "is_paused": self.is_paused,
            "quality_score": self.quality_score,
            "params": copy.deepcopy(self.params),
            "target_nozzle_temp": self.target_nozzle_temp,
            "target_bed_temp": self.target_bed_temp,
            "last_error": self.last_error,
            "is_connected": self.is_connected,
            "history_error": list(self.history_error),
        }

    def set_nozzle_temp(self, temp: Number) -> str:
        if not isinstance(temp, (int, float)):
            raise TypeError("temp must be a number(int or float)")
        if temp < 0 or temp > 350:
            raise ValueError("temp must be between 0 and 350")

        self.target_nozzle_temp = float(temp)
        self.nozzle_temp = float(temp)
        return f"nozzle temperature set to {self.nozzle_temp:.1f}℃"

    def set_param(self, name: str, value: Any) -> str:
        if not isinstance(name, str) or not name.strip():
            raise TypeError("name must be a non-empty string")
        self.params[name] = value
        return f"param {name} set to {value}"

    def start_print(self) -> str:
        if self.last_error:
            raise RuntimeError(f"cannot start print: {self.last_error}")

        if self.is_printing and not self.is_paused:
            return "already printing"

        if self.is_printing and self.is_paused:
            self.is_paused = False
            return "resumed printing"

        self.is_printing = True
        self.is_paused = False
        self.progress = 0
        self.quality_score = calc_quality_score(self.params, nozzle_temp=self.nozzle_temp)
        return f"started printing, quality_score={self.quality_score}"

    def pause_print(self) -> str:
        if not self.is_printing:
            return "can not pause:no printing"
        if self.is_paused:
            return "already paused"
        self.is_paused = True
        return "pause printing"

    def stop_print(self) -> str:
        if not self.is_printing:
            return "already stopped"
        self.is_printing = False
        self.is_paused = False
        self.progress = 0
        return "stopped printing"

    def simulate_error(self, error_type: str) -> str:
        return apply_fault(self, error_type)

    def clear_error(self) -> str:
        self.last_error = None
        return "error cleared"
