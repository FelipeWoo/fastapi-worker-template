from __future__ import annotations

from fastapi import Request
from app.core.config import AppConfig


def get_config(request: Request) -> AppConfig:
    cfg = getattr(request.app.state, "config", None)
    if cfg is None:
        raise RuntimeError("AppConfig not initialized. Ensure lifespan sets app.state.config.")
    return cfg
