from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import briefing, notes, projects, services, settings as settings_api, tasks
from app.auth import install_auth
from app.config import get_settings
from app.database import init_db
from app.web import routes as web_routes


def create_app(*, seed_on_startup: bool = True, init_database: bool = True) -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if init_database:
            init_db(seed=seed_on_startup)
        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    install_auth(app, settings)

    static_dir = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    app.include_router(tasks.router)
    app.include_router(projects.router)
    app.include_router(notes.router)
    app.include_router(services.router)
    app.include_router(settings_api.router)
    app.include_router(briefing.router)
    app.include_router(web_routes.router)

    return app


app = create_app()
