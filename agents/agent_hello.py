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


hello_skill = AgentSkill(
    id="hello_world",
    name="Returns hello world",
    description="just returns hello world",
    tags=["hello world"],
    examples=["hi", "hello world"],
)


hello_agent_card = AgentCard(
    name="Hello World Agent",
    description="Just a hello world agent",
    url="http://localhost:9999/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[hello_skill],
)


class HelloWorldAgent:
    """Simple agent that accepts either a str or a Message-like object."""

    async def invoke(self, input_value: Union[str, Message, None] = None) -> Message:
        """Return the provided input text or message payload with prefix, otherwise a default.

        Args:
            input_value: either a `str`, an `a2a.types.Message`, or `None`.
        """
        text = extract_text(input_value)
        if text:
            out_text = "HelloWorld Agent: " + text
        else:
            out_text = "Hello World~"

        # Build two TextParts, one for human and one for agent
        user_part = Part(root=TextPart(text=out_text, metadata={"receiver": "user"}))
        agent_part = Part(root=TextPart(text=out_text, metadata={"receiver": "agent"}))
        out_message = Message(
            message_id=uuid.uuid4().hex,
            parts=[user_part, agent_part],
            role=Role.agent,
        )
        return out_message
