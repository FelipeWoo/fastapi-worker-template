import os
import time
import secrets
import jwt
from dotenv import load_dotenv

load_dotenv(override=True)

secret = os.environ["INTERNAL_JWT_SECRET"]

now = int(time.time())
claims = {
    "iss": os.environ.get("INTERNAL_JWT_ISSUER", "go-main"),
    "aud": os.environ.get("INTERNAL_JWT_AUDIENCE", "fastapi-worker"),
    "iat": now,
    "exp": now + 120,
    "jti": secrets.token_hex(16),
    "sub": "service:go-main",
    "scope": "internal:billing",
}

alg = os.environ.get("INTERNAL_JWT_ALG", "HS256")
# Strip possible surrounding quotes from env var (e.g. "HS256" or 'HS256')
alg = alg.strip().strip('"').strip("'")
print(jwt.encode(claims, secret, algorithm=alg))
