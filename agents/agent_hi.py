from a2a.types import AgentSkill, AgentCard, AgentCapabilities


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
    """Hi There Agent."""

    async def invoke(self, input_text: str | None = None) -> str:
        """Return the provided input_text if present, otherwise a default."""
        if input_text:
            if ":" in input_text:
                input_text = input_text.split(":", 1)[1].strip()
            return "HiThere Agent: " + input_text
        return "Hi there!"
