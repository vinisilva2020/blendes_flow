#!/usr/bin/env python3
"""Create the single root .env while preserving legacy local values."""

from __future__ import annotations

import os
import re
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / ".env"
TEMPLATE = ROOT / ".env.example"
LEGACY_ENV = ROOT / "backend" / ".env"
LEGACY_SECRETS = ROOT / "infrastructure" / "secrets"
ASSIGNMENT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")


def parse(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        match = ASSIGNMENT.match(raw_line.strip())
        if match:
            values[match.group(1)] = match.group(2)
    return values


def read_legacy_secret(values: dict[str, str], name: str, filename: str) -> str:
    direct = values.get(name, "")
    if direct:
        return direct

    referenced = values.get(f"{name}_FILE", "")
    candidates = []
    if referenced:
        path = Path(referenced)
        candidates.append(path if path.is_absolute() else LEGACY_ENV.parent / path)
    candidates.append(LEGACY_SECRETS / filename)
    for candidate in candidates:
        try:
            value = candidate.resolve().read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if value:
            return value
    return ""


def main() -> int:
    if TARGET.exists():
        print(f"kept: {TARGET}")
        return 0

    legacy = parse(LEGACY_ENV)
    values = {
        **legacy,
        "DJANGO_SETTINGS_MODULE": "configuration.settings.docker",
        "DJANGO_SECRET_KEY": read_legacy_secret(
            legacy, "DJANGO_SECRET_KEY", "django_secret_key.txt"
        )
        or secrets.token_urlsafe(64),
        "JWT_SIGNING_KEY": read_legacy_secret(
            legacy, "JWT_SIGNING_KEY", "jwt_signing_key.txt"
        )
        or secrets.token_urlsafe(64),
        "POSTGRES_PASSWORD": read_legacy_secret(
            legacy, "POSTGRES_PASSWORD", "postgres_password.txt"
        )
        or secrets.token_urlsafe(48),
    }

    output = []
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        match = ASSIGNMENT.match(line)
        if match and match.group(1) in values:
            line = f"{match.group(1)}={values[match.group(1)]}"
        output.append(line)

    temporary = TARGET.with_suffix(".env.tmp")
    temporary.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    os.replace(temporary, TARGET)
    try:
        TARGET.chmod(0o600)
    except OSError:
        pass
    print(f"generated: {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
