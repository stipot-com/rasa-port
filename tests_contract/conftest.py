from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(REPO_ROOT) if not existing else os.pathsep.join([str(REPO_ROOT), existing])
    )
    return env

