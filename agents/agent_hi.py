from typing import Union
import uuid

from a2a.types import (
    AgentSkill,
    AgentCard,
    AgentCapabilities,
    Message,
    Role,
    Part,
    TextPart,
)
from .utils import extract_text


hi_skill = AgentSkill(
    id="hi_there",
    name="Returns hi there",
    description="just returns hi there",
    tags=["hi there"],
    examples=["hi", "hi there"],
)


hi_agent_card = AgentCard(
    name="Hi There Agent",
    description="Just a hi there agent",
    url="http://localhost:9998/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[hi_skill],
)


class HiThereAgent:
    """Simple agent that accepts either a str or a Message-like object."""

    async def invoke(self, input_value: Union[str, Message, None] = None) -> Message:
        """Return the provided input text or message payload with prefix, otherwise a default.

        Args:
            input_value: either a `str`, an `a2a.types.Message`, or `None`.
        """
        text = extract_text(input_value)
        if text:
            out_text = "HiThere Agent: " + text
        else:
            out_text = "Hi there!"

        # Build two TextParts, one for human and one for agent
        user_part = Part(root=TextPart(text=out_text, metadata={"receiver": "user"}))
        agent_part = Part(root=TextPart(text=out_text, metadata={"receiver": "agent"}))
        out_message = Message(
            message_id=uuid.uuid4().hex,
            parts=[user_part, agent_part],
            role=Role.agent,
        )
        return out_message
