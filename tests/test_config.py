import json
from pathlib import Path

from backend.config import load_config, save_config


def test_save_and_load_config_roundtrip(tmp_path: Path):
    cfg = {
        "global_refresh_rate": 1.2,
        "history_size": 7,
        "providers": {"weather": {"enabled": True}},
    }
    target = tmp_path / "config.json"

    save_config(cfg, target)
    loaded = load_config(target)

    assert loaded == cfg
    text = target.read_text(encoding="utf-8")
    assert json.loads(text) == cfg
