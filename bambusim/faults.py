from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Bambusim


_MAPPING: dict[str, str] = {
    "断料": "filament_runout",
    "缺料": "filament_runout",
    "filament_runout": "filament_runout",
    "runout": "filament_runout",
    "过热": "overheat",
    "overheat": "overheat",
    "over_heat": "overheat",
    "断开": "disconnect",
    "断线": "disconnect",
    "disconnect": "disconnect",
}


def normalize_error_type(error_type: str) -> str:
    if not isinstance(error_type, str) or not error_type.strip():
        raise TypeError("error_type must be a non-empty string")
    et = error_type.strip().lower()
    if et not in _MAPPING:
        raise ValueError(
            "error_type must be one of: 断料/filament_runout, 过热/overheat, 断开/disconnect"
        )
    return _MAPPING[et]


def apply_fault(sim: "Bambusim", error_type: str) -> str:
    normalized = normalize_error_type(error_type)

    sim.last_error = normalized
    sim.history_error.append(normalized)

    if normalized == "filament_runout":
        if sim.is_printing:
            sim.is_paused = True
        return "simulated error: filament_runout"

    if normalized == "overheat":
        sim.nozzle_temp = min(350.0, max(sim.nozzle_temp, 260.0))
        if sim.is_printing:
            sim.is_paused = True
        return "simulated error: overheat"

    #不管什么原因，包括disconnect，直接合并
    sim.is_connected = False
    sim.is_printing = False
    sim.is_paused = False
    return "simulated error: disconnect"
