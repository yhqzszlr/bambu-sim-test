from __future__ import annotations

from fastapi import FastAPI, HTTPException

from bambusim.core import Bambusim
from web.schemas import SetTempReq, SetParamReq, SetErrorReq

app = FastAPI(title="Bambusim API")

sim = Bambusim()


@app.get("/status")
def status():
    return sim.get_status()


@app.post("/nozzle_temp")
def nozzle_temp(req: SetTempReq):
    try:
        msg = sim.set_nozzle_temp(req.temp)
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/param")
def set_param(req: SetParamReq):
    try:
        msg = sim.set_param(req.name, req.value)
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/start")
def start_print():
    try:
        msg = sim.start_print()
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pause")
def pause_print():
    try:
        msg = sim.pause_print()
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/stop")
def stop_print():
    try:
        msg = sim.stop_print()
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/error")
def simulate_error(req: SetErrorReq):
    try:
        msg = sim.simulate_error(req.error_type)
        return {"ok": True, "message": msg, "status": sim.get_status()}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/error/clear")
def clear_error():
    msg = sim.clear_error()
    return {"ok": True, "message": msg, "status": sim.get_status()}
