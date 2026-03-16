import pytest

from bambusim.core import Bambusim
from bambusim.faults import apply_fault
from bambusim.logging_utils import append_error

##测试类型、内容与逻辑

# A) core：骨架与基本设定

def test_heat_sets_temps_and_targets():
    sim = Bambusim()

    ret = sim.set_nozzle_temp(210)

    assert isinstance(ret, str)
    assert "nozzle temperature set to" in ret

    st = sim.get_status()
    assert st["nozzle_temp"] == 210.0
    assert st["target_nozzle_temp"] == 210.0


@pytest.mark.parametrize("bad", ["hot", None, object()])
def test_heat_invalid_temp_type(bad):
    sim = Bambusim()
    with pytest.raises(TypeError):
        sim.set_nozzle_temp(bad)


@pytest.mark.parametrize("bad", [-1, 351])
def test_heat_invalid_temp_range(bad):
    sim = Bambusim()
    with pytest.raises(ValueError):
        sim.set_nozzle_temp(bad)


def test_start_print_sets_flags_and_quality_score():
    sim = Bambusim()

    ret = sim.start_print()

    assert isinstance(ret, str)
    assert ret.startswith("started printing, quality_score=")

    st = sim.get_status()
    assert st["is_printing"] is True
    assert st["is_paused"] is False
    assert st["progress"] == 0
    assert st["quality_score"] is not None
    assert 0.0 <= st["quality_score"] <= 100.0


def test_parameter_impact_quality_score_changes():
    sim = Bambusim()
    sim.set_param("speed", 100)
    sim.set_param("layer_height", 0.2)
    sim.set_param("cooling", 50)
    sim.start_print()
    base = sim.get_status()["quality_score"]
    assert isinstance(base, (int, float))

    sim2 = Bambusim()
    sim2.set_param("speed", 200)
    sim2.set_param("layer_height", 0.3)
    sim2.set_param("cooling", 50)
    sim2.start_print()
    worse = sim2.get_status()["quality_score"]
    assert worse < base

    sim3 = Bambusim()
    sim3.set_param("speed", 60)
    sim3.set_param("layer_height", 0.12)
    sim3.set_param("cooling", 50)
    sim3.start_print()
    better = sim3.get_status()["quality_score"]
    assert better >= base


# B) faults：故障规则

@pytest.mark.parametrize("inp, normalized", [
    ("runout", "filament_runout"),
    ("filament_runout", "filament_runout"),
    ("断料", "filament_runout"),
    ("overheat", "overheat"),
    ("过热", "overheat"),
    ("disconnect", "disconnect"),
    ("断开", "disconnect"),
])
def test_apply_fault_normalizes_and_records_history(inp, normalized):
    sim = Bambusim()
    msg = apply_fault(sim, inp)

    assert isinstance(msg, str)
    assert sim.last_error == normalized
    assert normalized in sim.history_error


def test_fault_blocks_start_print_until_cleared():
    sim = Bambusim()

    apply_fault(sim, "overheat")
    with pytest.raises(RuntimeError):
        sim.start_print()

    sim.clear_error()
    ret = sim.start_print()
    assert isinstance(ret, str)


def test_disconnect_stops_printing():
    sim = Bambusim()
    sim.is_connected = True
    sim.start_print()
    assert sim.is_printing is True

    apply_fault(sim, "disconnect")
    assert sim.is_connected is False
    assert sim.is_printing is False
    assert sim.is_paused is False


# C) logging_utils：日志写入

def test_error_append_logging(tmp_path):
    log = tmp_path / "errors.log"

    append_error(log, "overheat")
    append_error(log, "motor_stall")
    append_error(log, "overheat")

    text = log.read_text(encoding="utf-8")
    assert "overheat" in text
    assert "motor_stall" in text
