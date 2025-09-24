from typing_extensions import override
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from agents.agent_hello import HelloWorldAgent
from agents.agent_hi import HiThereAgent
from .utils import get_input_value_from_context


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
        # Prefer passing the full Message object when available
        # to allow the agent to inspect parts
        # fall back to a plain string input.
        input_value = get_input_value_from_context(context)

        message_result = await self.agent.invoke(input_value)
        # Respond to the original caller
        await event_queue.enqueue_event(message_result)

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
        # Prefer passing the full Message object when available
        # to allow the agent to inspect parts
        # fall back to a plain string input.
        input_value = get_input_value_from_context(context)

        message_result = await self.agent.invoke(input_value)
        # Respond to the original caller
        await event_queue.enqueue_event(message_result)

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")
