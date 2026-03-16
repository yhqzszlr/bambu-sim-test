from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class SetTempReq(BaseModel):
    temp: float = Field(..., description="Nozzle temperature target")


class SetParamReq(BaseModel):
    name: str = Field(..., min_length=1)
    value: Any


class SetErrorReq(BaseModel):
    error_type: str = Field(..., min_length=1)
