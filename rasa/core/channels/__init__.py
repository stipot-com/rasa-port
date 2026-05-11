from typing import Dict, List, Text, Type

from rasa.core.channels.channel import (  # noqa: F401
    CollectingOutputChannel,
    InputChannel,
    OutputChannel,
    UserMessage,
)

# AdaOS uses Rasa here as an embedded NLU runtime, not as a full channel server.
input_channel_classes: List[Type[InputChannel]] = []
BUILTIN_CHANNELS: Dict[Text, Type[InputChannel]] = {}
