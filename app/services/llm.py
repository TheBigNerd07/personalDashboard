from __future__ import annotations

import json
import logging
from typing import Any
from typing import Optional

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are Logan's local productivity assistant. You create concise, practical "
    "daily briefings from structured dashboard data. Do not invent facts. If data "
    "is missing, say so briefly."
)


class LLMUnavailable(RuntimeError):
    """Raised when the optional local LLM cannot produce a usable response."""


class LMStudioClient:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()

    async def generate_daily_briefing(self, dashboard_context: dict[str, Any]) -> str:
        if not self.settings.llm_enabled:
            raise LLMUnavailable("LLM integration is disabled")

        url = f"{self.settings.llm_base_url.rstrip('/')}/chat/completions"
        user_prompt = (
            "Create a daily briefing from this JSON:\n"
            f"{json.dumps(dashboard_context, indent=2, default=str)}\n\n"
            "Return markdown with these sections:\n"
            "- Focus\n"
            "- Top Tasks\n"
            "- Deadlines\n"
            "- Projects\n"
            "- Homelab\n"
            "- Stride Shots\n"
            "- Suggested Next Action"
        )
        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 700,
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            logger.warning("LM Studio request failed: %s", exc)
            raise LLMUnavailable("LM Studio request failed") from exc

        try:
            content = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            logger.warning("LM Studio returned an invalid response shape")
            raise LLMUnavailable("LM Studio returned invalid output") from exc

        if not content:
            raise LLMUnavailable("LM Studio returned an empty briefing")

        return content
