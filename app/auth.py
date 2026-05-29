from __future__ import annotations

import secrets

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.config import Settings


PUBLIC_PATH_PREFIXES = ("/static",)
PUBLIC_PATHS = {"/health", "/login"}


def verify_password(candidate: str, configured_password: str) -> bool:
    if not configured_password:
        return True
    return secrets.compare_digest(candidate, configured_password)


def install_auth(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie="command_center_session",
        same_site="lax",
        max_age=60 * 60 * 24 * 30,
    )

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        if not settings.auth_enabled:
            return await call_next(request)

        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith(PUBLIC_PATH_PREFIXES):
            return await call_next(request)

        if request.session.get("authenticated") is True:
            return await call_next(request)

        if path.startswith("/api") or request.headers.get("accept") == "application/json":
            return JSONResponse({"detail": "Authentication required"}, status_code=401)

        return RedirectResponse(url="/login", status_code=303)

