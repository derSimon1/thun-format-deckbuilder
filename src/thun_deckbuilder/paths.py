from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]

CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"

DATABASE_FILE = DATA_DIR / "cards.db"
SCRYFALL_BULK_FILE = DATA_DIR / "default_cards.json"
THUN_CONFIG_FILE = CONFIG_DIR / "thun.toml"