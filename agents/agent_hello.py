from a2a.types import AgentSkill, AgentCard, AgentCapabilities


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
    """Hello World Agent."""

    async def invoke(self, input_text: str | None = None) -> str:
        """Return the provided input_text if present, otherwise a default."""
        if input_text:
            if ":" in input_text:
                input_text = input_text.split(":", 1)[1].strip()
            return "HelloWorld Agent: " + input_text
        return "Hello World~"
