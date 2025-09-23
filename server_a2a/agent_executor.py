from typing_extensions import override
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class HelloWorldAgent:
    """Hello World Agent."""

    async def invoke(self, input_text: str | None = None) -> str:
        """Return the provided input_text if present, otherwise a default."""
        if input_text:
            if ":" in input_text:
                input_text = input_text.split(":", 1)[1].strip()
            return "HelloWorld Agent: " + input_text
        return "Hello World~"


class HiThereAgent:
    """Hi There Agent."""

    async def invoke(self, input_text: str | None = None) -> str:
        """Return the provided input_text if present, otherwise a default."""
        if input_text:
            if ":" in input_text:
                input_text = input_text.split(":", 1)[1].strip()
            return "HiThere Agent: " + input_text
        return "Hi there!"


class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = HelloWorldAgent()

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Extract incoming text from the request context (if any)
        try:
            user_text = context.get_user_input().strip()
        except Exception:
            user_text = ""

        result = await self.agent.invoke(user_text or None)
        # Respond to the original caller
        await event_queue.enqueue_event(new_agent_text_message(result))

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")


class HiThereAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = HiThereAgent()

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Extract incoming text from the request context (if any)
        try:
            user_text = context.get_user_input().strip()
        except Exception:
            user_text = ""

        result = await self.agent.invoke(user_text or None)
        # Respond to the original caller
        await event_queue.enqueue_event(new_agent_text_message(result))

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")
