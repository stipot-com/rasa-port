from __future__ import annotations

import tempfile
import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator


@dataclass(frozen=True)
class TrainResult:
    """Result of an NLU-only training run."""

    model_path: Path


def train_nlu(
    project_dir: Path,
    output_dir: Path,
    *,
    fixed_model_name: str = "interpreter_latest",
) -> TrainResult:
    """Train an NLU-only model from a Rasa-style project directory."""
    project_dir = Path(project_dir)
    output_dir = Path(output_dir)
    config_path = project_dir / "config.yml"
    data_path = project_dir / "data"
    domain_path = project_dir / "domain.yml"

    if not config_path.exists():
        raise FileNotFoundError(f"Missing Rasa config: {config_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"Missing Rasa NLU data directory: {data_path}")

    from rasa.model_training import train_nlu as rasa_train_nlu

    with _default_training_cache(output_dir):
        model_path = rasa_train_nlu(
            config=str(config_path),
            nlu_data=str(data_path),
            output=str(output_dir),
            fixed_model_name=fixed_model_name,
            domain=str(domain_path) if domain_path.exists() else None,
        )
    if not model_path:
        raise RuntimeError("Rasa NLU training did not produce a model artifact")

    return TrainResult(model_path=Path(model_path))


@contextmanager
def _default_training_cache(output_dir: Path) -> Iterator[None]:
    cache_env = "RASA_CACHE_DIRECTORY"
    previous = os.environ.get(cache_env)
    if previous is None:
        os.environ[cache_env] = str(Path(output_dir) / ".rasa-cache")
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(cache_env, None)
        else:
            os.environ[cache_env] = previous


def load_model(model_path: Path) -> "NluRuntime":
    """Load an NLU model artifact for parsing."""
    return NluRuntime(model_path)


class NluRuntime:
    """Pure NLU model runtime that avoids the full Rasa Agent surface."""

    def __init__(self, model_path: Path) -> None:
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Missing Rasa model artifact: {self.model_path}")

        self._temp_dir = tempfile.TemporaryDirectory(prefix="adaos-rasa-nlu-")
        self._metadata, self._runner = self._load_runner(self.model_path)

    def close(self) -> None:
        """Release extracted model files."""
        self._temp_dir.cleanup()

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse a single user message."""
        from rasa.core.channels.channel import UserMessage
        from rasa.engine.constants import PLACEHOLDER_MESSAGE, PLACEHOLDER_TRACKER
        from rasa.shared.core.trackers import DialogueStateTracker
        from rasa.shared.nlu.constants import (
            ENTITIES,
            INTENT,
            INTENT_NAME_KEY,
            PREDICTED_CONFIDENCE_KEY,
            TEXT,
        )

        message = UserMessage(text)
        tracker = DialogueStateTracker.from_events(message.sender_id, [])
        results = self._runner.run(
            inputs={
                PLACEHOLDER_MESSAGE: [message],
                PLACEHOLDER_TRACKER: tracker,
            },
            targets=[self._metadata.nlu_target],
        )
        parsed_message = results[self._metadata.nlu_target][0]
        parse_data: Dict[str, Any] = {
            TEXT: "",
            INTENT: {INTENT_NAME_KEY: None, PREDICTED_CONFIDENCE_KEY: 0.0},
            ENTITIES: [],
        }
        parse_data.update(parsed_message.as_dict(only_output_properties=True))
        self._update_full_retrieval_intent(parse_data)
        return parse_data

    def _load_runner(self, model_path: Path) -> tuple[Any, Any]:
        from rasa.engine import loader
        from rasa.engine.runner.dask import DaskGraphRunner
        from rasa.engine.storage.local_model_storage import LocalModelStorage

        return loader.load_predict_graph_runner(
            Path(self._temp_dir.name),
            model_path,
            LocalModelStorage,
            DaskGraphRunner,
        )

    @staticmethod
    def _update_full_retrieval_intent(parse_data: Dict[str, Any]) -> None:
        from rasa.shared.nlu.constants import (
            FULL_RETRIEVAL_INTENT_NAME_KEY,
            INTENT,
            INTENT_NAME_KEY,
            INTENT_RESPONSE_KEY,
            RESPONSE,
            RESPONSE_SELECTOR,
        )

        intent_name = parse_data.get(INTENT, {}).get(INTENT_NAME_KEY)
        response_selector = parse_data.get(RESPONSE_SELECTOR, {})
        all_retrieval_intents = response_selector.get("all_retrieval_intents", [])
        if intent_name and intent_name in all_retrieval_intents:
            retrieval_intent = (
                response_selector.get(intent_name, {})
                .get(RESPONSE, {})
                .get(INTENT_RESPONSE_KEY)
            )
            parse_data[INTENT][FULL_RETRIEVAL_INTENT_NAME_KEY] = retrieval_intent
