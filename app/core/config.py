from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from app.core.paths import find_project_root


class InternalJWTConfig(BaseModel):
    secret: str = Field(default="")
    issuer: str = Field(default="go-main")
    audience: str = Field(default="fastapi-worker")
    alg: Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"] = Field(default="HS256")
    leeway_seconds: int = Field(default=10)


class AppConfig(BaseModel):
    name: str = Field(default="default")
    env: str = Field(default="production")
    log_level: str = Field(default="INFO")
    root: Path
    internal_jwt: InternalJWTConfig


def load_config() -> AppConfig:
    root = find_project_root(marker="Makefile")

    return AppConfig(
        name=os.getenv("APP_NAME", "default"),
        env=os.getenv("APP_ENV", "production"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        root=root,
        internal_jwt=InternalJWTConfig(
            secret=os.getenv("INTERNAL_JWT_SECRET", ""),
            issuer=os.getenv("INTERNAL_JWT_ISSUER", "go-main"),
            audience=os.getenv("INTERNAL_JWT_AUDIENCE", "fastapi-worker"),
            alg=os.getenv("INTERNAL_JWT_ALG", "HS256"),
            leeway_seconds=int(os.getenv("INTERNAL_JWT_LEEWAY", "10")),
        ),
    )
