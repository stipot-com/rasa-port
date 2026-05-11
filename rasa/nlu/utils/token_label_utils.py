from __future__ import annotations

from typing import Any, Dict, List, Optional, Text

from rasa.nlu.tokenizers.tokenizer import Token
from rasa.shared.nlu.constants import ENTITY_ATTRIBUTE_TYPE, NO_ENTITY_TAG


def determine_token_labels(
    token: Token,
    entities: Optional[List[Dict[Text, Any]]],
    attribute_key: Text = ENTITY_ATTRIBUTE_TYPE,
) -> Text:
    """Determine the training label for a token without importing test helpers."""
    entity = _determine_entity_for_token(token, entities)
    if entity is None:
        return NO_ENTITY_TAG

    label = entity.get(attribute_key)
    return label if label else NO_ENTITY_TAG


def _determine_entity_for_token(
    token: Token,
    entities: Optional[List[Dict[Text, Any]]],
) -> Optional[Dict[Text, Any]]:
    if not entities:
        return None

    candidates = [
        entity
        for entity in entities
        if _is_token_within_entity(token, entity)
        or _does_token_cross_borders(token, entity)
    ]
    if not candidates:
        return None

    return max(candidates, key=lambda entity: _determine_intersection(token, entity))


def _is_token_within_entity(token: Token, entity: Dict[Text, Any]) -> bool:
    return _determine_intersection(token, entity) == len(token.text)


def _does_token_cross_borders(token: Token, entity: Dict[Text, Any]) -> bool:
    num_intersect = _determine_intersection(token, entity)
    return 0 < num_intersect < len(token.text)


def _determine_intersection(token: Token, entity: Dict[Text, Any]) -> int:
    pos_token = set(range(token.start, token.end))
    pos_entity = set(range(entity["start"], entity["end"]))
    return len(pos_token.intersection(pos_entity))

