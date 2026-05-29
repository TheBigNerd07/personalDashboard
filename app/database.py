from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

from sqlmodel import Session, SQLModel, create_engine, select

from app.config import Settings, get_settings
from app.models import Note, Project, ServiceCard, Setting, Task, utcnow


def _sqlite_path_from_url(database_url: str) -> Optional[Path]:
    if database_url == "sqlite:///:memory:":
        return None
    if database_url.startswith("sqlite:///"):
        return Path(database_url.replace("sqlite:///", "", 1))
    return None


def _create_engine(settings: Settings):
    db_path = _sqlite_path_from_url(settings.database_url)
    if db_path is not None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, connect_args=connect_args)


settings = get_settings()
engine = _create_engine(settings)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_setting(session: Session, key: str, default: str = "") -> str:
    setting = session.get(Setting, key)
    return setting.value if setting else default


def set_setting(session: Session, key: str, value: str) -> Setting:
    setting = session.get(Setting, key)
    if setting is None:
        setting = Setting(key=key, value=value)
        session.add(setting)
    else:
        setting.value = value
        setting.updated_at = utcnow()
    session.commit()
    session.refresh(setting)
    return setting


def seed_database() -> None:
    with Session(engine) as session:
        existing = any(
            [
                session.exec(select(Task)).first(),
                session.exec(select(Project)).first(),
                session.exec(select(ServiceCard)).first(),
            ]
        )
        if existing:
            return

        services = [
            ServiceCard(name="Portainer", url="http://pione.local:9000", description="Docker management", category="PiOne", sort_order=10),
            ServiceCard(name="Nginx Proxy Manager", url="http://pione.local:81", description="Reverse proxy and certificates", category="PiOne", sort_order=20),
            ServiceCard(name="Navidrome", url="http://musicpi.local:4533", description="Local music library", category="MusicPi", sort_order=30),
            ServiceCard(name="Tailscale Admin", url="https://login.tailscale.com/admin", description="Tailnet device and ACL management", category="Network", sort_order=40),
            ServiceCard(name="PiOne", url="http://pione.local", description="General infrastructure and experiments", category="Homelab", sort_order=50),
            ServiceCard(name="MusicPi", url="http://musicpi.local", description="Media and music services", category="Homelab", sort_order=60),
            ServiceCard(name="BusinessPi", url="http://businesspi.local", description="Business tools and automation", category="Homelab", sort_order=70),
        ]
        projects = [
            Project(name="Stride Shots Workflow", description="Improve capture, culling, delivery, and client follow-up.", category="Stride Shots", next_action="Add the next event workflow step."),
            Project(name="Homelab Improvements", description="Keep PiOne, MusicPi, and BusinessPi reliable and documented.", category="Homelab", next_action="Customize service URLs and health checks."),
            Project(name="School Planning", description="Track school deadlines and weekly priorities.", category="School", next_action="Add current deadlines."),
            Project(name="Command Center", description="Self-hosted dashboard for daily focus.", category="Software", next_action="Deploy with Docker Compose."),
        ]
        tasks = [
            Task(title="Customize service links", category="homelab", priority="high", status="active"),
            Task(title="Configure LM Studio", category="homelab", priority="normal", status="inbox"),
            Task(title="Add current school deadlines", category="school", priority="high", status="active"),
            Task(title="Add Stride Shots next actions", category="stride_shots", priority="high", status="active"),
        ]

        session.add_all(services + projects + tasks)
        session.add(Setting(key="todays_focus", value="Review priorities and move one important project forward."))
        session.commit()


def init_db(seed: bool = True) -> None:
    create_db_and_tables()
    if seed:
        seed_database()
