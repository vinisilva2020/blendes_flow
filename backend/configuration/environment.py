"""Load the single project environment file."""

from functools import lru_cache
from pathlib import Path

import environ

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


@lru_cache(maxsize=1)
def load_environment() -> None:
    """Load root .env without overriding variables supplied by the process."""
    if ENV_FILE.is_file():
        environ.Env.read_env(ENV_FILE, overwrite=False)
