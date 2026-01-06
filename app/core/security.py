from __future__ import annotations

from typing import Any

import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer = HTTPBearer(auto_error=False)

REQUIRED_CLAIMS = ["exp", "iat", "iss", "aud"]


def require_internal_jwt(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict[str, Any]:
    # Read env at call time so values set by boot() or tests are respected
    JWT_SECRET = os.getenv("INTERNAL_JWT_SECRET", "")
    JWT_ISSUER = os.getenv("INTERNAL_JWT_ISSUER", "go-main")
    JWT_AUDIENCE = os.getenv("INTERNAL_JWT_AUDIENCE", "fastapi-worker")
    JWT_ALG = os.getenv("INTERNAL_JWT_ALG", "HS256")

    if not JWT_SECRET:
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
            JWT_SECRET,
            algorithms=[JWT_ALG],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={"require": REQUIRED_CLAIMS},
            leeway=10,
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
    def checker(claims: dict[str, Any] = Depends(require_internal_jwt)) -> dict[str, Any]:
        scope = claims.get("scope", "")
        scopes = set(str(scope).split())
        if required not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing scope: {required}",
            )
        return claims
    return checker
