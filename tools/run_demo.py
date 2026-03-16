from __future__ import annotations
from bambusim.core import Bambusim
from bambusim.logging_utils import write_log_line, append_error,log_op_error
from bambusim.logging_utils import write_log_line, run_op

LOG_PATH = "log.txt"
ERRORS_PATH = "errors.log"


def main() -> None:
    sim = Bambusim()

    print("1) status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    print(run_op(LOG_PATH, action="SET_NOZZLE_TEMP", params="temp=210", func=sim.set_nozzle_temp, args=(210,)))
    print(run_op(LOG_PATH, action="SET_PARAM", params="name=speed,value=140", func=sim.set_param, args=("speed", 140)))
    print(run_op(LOG_PATH, action="SET_PARAM", params="name=layer_height,value=0.28", func=sim.set_param, args=("layer_height", 0.28)))
    print(run_op(LOG_PATH, action="SET_PARAM", params="name=cooling,value=60", func=sim.set_param, args=("cooling", 60)))

    print("set_params_status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    print(run_op(LOG_PATH, action="START_PRINT", params="-", func=sim.start_print))
    print("start_status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    print(run_op(LOG_PATH, action="PAUSE_PRINT", params="-", func=sim.pause_print))
    print("pause_status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    print(run_op(LOG_PATH, action="START_PRINT", params="-", func=sim.start_print))
    print(run_op(LOG_PATH, action="STOP_PRINT", params="-", func=sim.stop_print))
    print("stop_status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    run_op(LOG_PATH, action="START_PRINT", params="-", func=sim.start_print)
    print(run_op(LOG_PATH, action="SIMULATE_ERROR", params="error_type=runout", func=sim.simulate_error, args=("runout",)))
    print("simulate_error_status:", sim.get_status())
    write_log_line(LOG_PATH, action="GET_STATUS", params="-", result="OK:printed_status")

    # 故意触发错误，验证日志
    run_op(LOG_PATH, action="SET_NOZZLE_TEMP", params="temp=999",
            func=sim.set_nozzle_temp, args=(999,), errors_path=ERRORS_PATH)

if __name__ == "__main__":
    main()
