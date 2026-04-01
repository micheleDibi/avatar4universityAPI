import json
import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


def _parse_api_keys() -> Dict[str, int]:
    raw = os.getenv("API_KEYS", "")
    if raw:
        return {k: int(v) for k, v in json.loads(raw).items()}
    return {}


class Settings:
    API_KEY: str = os.getenv("API_KEY", "")
    API_KEYS: Dict[str, int] = _parse_api_keys()
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")


settings = Settings()
