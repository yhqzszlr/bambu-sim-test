from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any,Callable


def append_error(path: str | Path, error_type: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(error_type + "\n")

##错误格式
def log_op_error(errors_path: str | Path, *, action: str, params: str, e: Exception) -> None:
    """Write one structured error line to errors.log."""
    append_error(
        errors_path,
        f"{action} | {params} | {type(e).__name__}: {e}",
    )

##日志格式
def write_log_line(
    log_path: str | Path,
    *,
    action: str,
    params: str = "-",
    result: str = "-",
    ts: datetime | None = None,
) -> None:
    """Write one line: 时间 | 操作 | 参数 | 结果"""
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    ts = ts or datetime.now()
    ts_str = ts.strftime("%F,%T")

    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{ts_str} | {action} | {params} | {result}\n")

##写入日志和错误
def run_op(
    log_path: str | Path,
    *,
    action: str,
    params: str,
    func: Callable[..., Any],
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
    errors_path: str | Path | None = None,
) -> Any:
    """Run an operation, log OK/ERROR to log.txt, and optionally log exceptions to errors.log."""
    kwargs = kwargs or {}
    try:
        ret = func(*args, **kwargs)
        write_log_line(log_path, action=action, params=params, result=f"OK:{ret}")
        return ret
    except Exception as e:
        write_log_line(log_path, action=action, params=params, result=f"ERROR:{type(e).__name__}:{e}")
        if errors_path is not None:
            log_op_error(errors_path, action=action, params=params, e=e)
        return None