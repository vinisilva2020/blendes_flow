#!/usr/bin/env python3
"""Gera os arquivos locais de segredo consumidos pelo Docker Compose."""

from __future__ import annotations

import argparse
import os
import secrets
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "infrastructure" / "secrets"


def write_secret(path: Path, value: str, force: bool) -> bool:
    if path.exists() and not force:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(value, encoding="utf-8", newline="\n")
    os.replace(temporary_path, path)

    try:
        path.chmod(0o600)
    except OSError:
        pass

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Django, JWT, and PostgreSQL secret files for Docker Compose."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Secrets directory (default: infrastructure/secrets).",
    )
    parser.add_argument(
        "--rotate-django",
        action="store_true",
        help="Replace only the existing Django secret key.",
    )
    parser.add_argument(
        "--rotate-jwt",
        action="store_true",
        help=(
            "Replace only the JWT signing key. Existing access tokens become "
            "invalid immediately."
        ),
    )
    parser.add_argument(
        "--rotate-postgres",
        action="store_true",
        help=(
            "Replace the PostgreSQL password file. Existing databases also "
            "require their role password to be changed."
        ),
    )
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    generated = (
        (
            output_dir / "django_secret_key.txt",
            secrets.token_urlsafe(64),
            args.rotate_django,
        ),
        (
            output_dir / "jwt_signing_key.txt",
            secrets.token_urlsafe(64),
            args.rotate_jwt,
        ),
        (
            output_dir / "postgres_password.txt",
            secrets.token_urlsafe(48),
            args.rotate_postgres,
        ),
    )

    for path, value, force in generated:
        action = "generated" if write_secret(path, value, force) else "kept"
        print(f"{action}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
