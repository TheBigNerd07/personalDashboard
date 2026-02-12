from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG_PATH = Path("config.json")


def load_config(path: Path | None = None) -> Dict[str, Any]:
    config_path = path or DEFAULT_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: Dict[str, Any], path: Path | None = None) -> None:
    config_path = path or DEFAULT_CONFIG_PATH
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
