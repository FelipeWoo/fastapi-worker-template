from __future__ import annotations

from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import AppConfig
from app.core.deps import get_config


bearer = HTTPBearer(auto_error=False)

REQUIRED_CLAIMS = ["exp", "iat", "iss", "aud"]


def require_internal_jwt(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    cfg: AppConfig = Depends(get_config),
) -> dict[str, Any]:
    jwt_cfg = cfg.internal_jwt

    if not jwt_cfg.secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing INTERNAL_JWT_SECRET",
        )

    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = creds.credentials

    try:
        claims = jwt.decode(
            token,
            jwt_cfg.secret,
            algorithms=[jwt_cfg.alg],
            issuer=jwt_cfg.issuer,
            audience=jwt_cfg.audience,
            options={"require": REQUIRED_CLAIMS},
            leeway=jwt_cfg.leeway_seconds,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return claims


def require_scope(required: str):
    def checker(
        claims: dict[str, Any] = Depends(require_internal_jwt),
    ) -> dict[str, Any]:
        scope = claims.get("scope", "")
        scopes = set(str(scope).split())
        if required not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing scope: {required}",
            )
        return claims

    return checker
