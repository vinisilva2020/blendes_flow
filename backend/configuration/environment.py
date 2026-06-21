"""Carrega o ambiente do backend a partir de um único arquivo .env."""

from functools import lru_cache
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


@lru_cache(maxsize=1)
def load_environment() -> None:
    """Carrega backend/.env sem sobrescrever variáveis do processo."""
    if ENV_FILE.is_file():
        environ.Env.read_env(ENV_FILE, overwrite=False)
