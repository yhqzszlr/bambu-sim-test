def append_error(path: str | Path, error_type: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(error_type + "\n")

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

##写入日志
def run_op(
    log_path: str | Path,
    *,
    action: str,
    params: str,
    func: Callable[..., Any],
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
) -> Any:
    """Run an operation, log OK/ERROR, and return func result (or None on exception)."""
    kwargs = kwargs or {}
    try:
        ret = func(*args, **kwargs)
        write_log_line(log_path, action=action, params=params, result=f"OK:{ret}")
        return ret
    except Exception as e:
        write_log_line(log_path, action=action, params=params, result=f"ERROR:{type(e).__name__}:{e}")
        return None