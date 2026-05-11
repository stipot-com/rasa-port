from __future__ import annotations

import json
import subprocess
import sys

import pytest

from tests_contract.conftest import REPO_ROOT, subprocess_env


@pytest.mark.contract
def test_adaos_nlu_api_import_is_lightweight() -> None:
    script = """
import json
import sys

import adaos_rasa_nlu

blocked = {
    "aiohttp",
    "boto3",
    "jwt",
    "pymongo",
    "rasa_sdk",
    "redis",
    "sanic",
    "twilio",
    "webexteamssdk",
}
loaded = sorted(name for name in blocked if name in sys.modules)
print(json.dumps({"loaded": loaded, "api": sorted(adaos_rasa_nlu.__all__)}))
raise SystemExit(1 if loaded else 0)
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        env=subprocess_env(),
        text=True,
        capture_output=True,
        check=False,
    )

    payload = json.loads(result.stdout.strip())
    assert result.returncode == 0, result.stderr
    assert payload["loaded"] == []
    assert payload["api"] == ["NluRuntime", "TrainResult", "load_model", "train_nlu"]


@pytest.mark.contract
def test_rasa_package_import_keeps_version_available() -> None:
    script = """
import json

import rasa

print(json.dumps({"version": rasa.__version__}))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        env=subprocess_env(),
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout.strip())["version"]

