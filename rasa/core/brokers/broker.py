from __future__ import annotations
import logging
from asyncio import AbstractEventLoop
from typing import Any, Dict, Text, Optional, Union, TypeVar, Type

import rasa.shared.utils.common
from rasa.utils.endpoints import EndpointConfig

logger = logging.getLogger(__name__)


EB = TypeVar("EB", bound="EventBroker")


class EventBroker:
    """Base class for any event broker implementation."""

    @staticmethod
    async def create(
        obj: Union[EventBroker, EndpointConfig, None],
        loop: Optional[AbstractEventLoop] = None,
    ) -> Optional[EventBroker]:
        """Factory to create an event broker."""
        if isinstance(obj, EventBroker):
            return obj

        if obj is None:
            return None

        logger.warning(
            "Event brokers are not included in the AdaOS Rasa NLU slice. "
            "Ignoring configured event broker."
        )
        return None

    @classmethod
    async def from_endpoint_config(
        cls: Type[EB],
        broker_config: EndpointConfig,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> Optional[EB]:
        """Creates an `EventBroker` from the endpoint configuration.

        Args:
            broker_config: The configuration for the broker.
            event_loop: The current event loop or `None`.

        Returns:
            An `EventBroker` object.
        """
        raise NotImplementedError(
            "Event broker must implement the `from_endpoint_config` method."
        )

    def publish(self, event: Dict[Text, Any]) -> None:
        """Publishes a json-formatted Rasa Core event into an event queue."""
        raise NotImplementedError("Event broker must implement the `publish` method.")

    def is_ready(self) -> bool:
        """Determine whether or not the event broker is ready.

        Returns:
            `True` by default, but this may be overridden by subclasses.
        """
        return True

    async def close(self) -> None:
        """Close the connection to an event broker."""
        # default implementation does nothing
        pass


async def _create_from_endpoint_config(
    endpoint_config: Optional[EndpointConfig], event_loop: Optional[AbstractEventLoop]
) -> Optional[EventBroker]:
    """Instantiate an event broker based on its configuration."""
    if endpoint_config is not None:
        logger.warning(
            "Event brokers are not included in the AdaOS Rasa NLU slice. "
            "Ignoring configured event broker."
        )
    return None


async def _load_from_module_name_in_endpoint_config(
    broker_config: EndpointConfig,
) -> Optional[EventBroker]:
    """Instantiate an event broker based on its class name."""
    try:
        event_broker_class = rasa.shared.utils.common.class_from_module_path(
            broker_config.type
        )
        return await event_broker_class.from_endpoint_config(broker_config)
    except (AttributeError, ImportError) as e:
        logger.warning(
            f"The `EventBroker` type '{broker_config.type}' could not be found. "
            f"Not using any event broker. Error: {e}"
        )
        return None
