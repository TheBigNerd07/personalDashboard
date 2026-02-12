from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional


SourceStatus = Literal["ok", "stale", "error"]


@dataclass
class NormalizedSnapshot:
    """Standardized payload produced by every provider."""

    source: str
    status: SourceStatus
    data: Dict[str, Any]
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "status": self.status,
            "data": self.data,
            "fetched_at": self.fetched_at.isoformat(),
            "error": self.error,
        }
