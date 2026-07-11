#!/usr/bin/env python3
"""Cross-platform development commands for BlendES Flow."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"


def executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required command not found: {name}")
    return path


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"+ {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


def docker_command() -> str:
    """Return Docker only when the CLI and engine are both available."""
    docker = executable("docker")
    engine = subprocess.run(
        [docker, "info"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if engine.returncode != 0:
        raise SystemExit(
            "Docker Engine is not available. Start Docker Desktop, wait until "
            "it reports that the engine is running, and retry "
            "`python scripts/project.py dev-docker`."
        )
    return docker


def setup() -> None:
    run([sys.executable, str(ROOT / "scripts" / "bootstrap_env.py")])
    run([executable("poetry"), "install"], cwd=BACKEND)
    run([executable("npm"), "ci"], cwd=FRONTEND)
    run([executable("poetry"), "run", "python", "manage.py", "migrate"], cwd=BACKEND)


def dev() -> None:
    poetry = executable("poetry")
    npm = executable("npm")
    processes = [
        subprocess.Popen(
            [poetry, "run", "python", "manage.py", "runserver"], cwd=BACKEND
        ),
        subprocess.Popen([npm, "run", "dev"], cwd=FRONTEND),
    ]
    try:
        exit_code = processes[0].wait()
        raise SystemExit(exit_code)
    except KeyboardInterrupt:
        pass
    finally:
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()


def dev_docker() -> None:
    docker = docker_command()
    run([sys.executable, str(ROOT / "scripts" / "bootstrap_env.py")])
    run([docker, "compose", "up", "--build"])


def test() -> None:
    run(
        [
            executable("poetry"),
            "run",
            "python",
            "manage.py",
            "test",
            "--settings=configuration.settings.test",
        ],
        cwd=BACKEND,
    )


def check() -> None:
    run([executable("poetry"), "run", "python", "manage.py", "check"], cwd=BACKEND)
    run([executable("npm"), "run", "type-check"], cwd=FRONTEND)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("setup", "dev", "dev-docker", "test", "check"),
    )
    command = parser.parse_args().command.replace("-", "_")
    try:
        globals()[command]()
    except subprocess.CalledProcessError as exc:
        rendered_command = " ".join(str(part) for part in exc.cmd)
        raise SystemExit(
            f"Command failed with exit code {exc.returncode}: {rendered_command}"
        ) from None


if __name__ == "__main__":
    main()
