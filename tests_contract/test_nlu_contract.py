from __future__ import annotations

from pathlib import Path

import pytest


FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.contract
@pytest.mark.integration
@pytest.mark.slow
def test_tiny_project_trains_loads_and_parses(tmp_path: Path) -> None:
    pytest.importorskip("sklearn")

    from adaos_rasa_nlu import load_model, train_nlu

    project_dir = FIXTURES / "tiny_nlu_project"
    train_result = train_nlu(
        project_dir=project_dir,
        output_dir=tmp_path / "models",
        fixed_model_name="contract_nlu",
    )

    assert train_result.model_path.exists()
    assert train_result.model_path.name == "contract_nlu.tar.gz"

    runtime = load_model(train_result.model_path)
    try:
        parsed = runtime.parse("hello")
    finally:
        runtime.close()

    assert parsed["text"] == "hello"
    assert parsed["intent"]["name"] in {"greet", "goodbye"}
    assert isinstance(parsed["intent"]["confidence"], float)
    assert isinstance(parsed["entities"], list)
