from typing_extensions import override
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import Message
from agents.agent_hello import HelloWorldAgent
from agents.agent_hi import HiThereAgent
from agents.self_discovery import SelfDiscoveryAgent
from agents.dating_coach import DatingCoachAgent
from agents.utils import extract_text
from .utils import get_input_value_from_context
from typing import AsyncGenerator


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

class SelfDiscoveryAgentExecutor(AgentExecutor):
    """Self Discovery Agent Executor Implementation."""

    def __init__(self):
        self.agent = SelfDiscoveryAgent()

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Get input from context
        input_value = get_input_value_from_context(context)

        print(f"[SelfDiscoveryAgentExecutor] Received: {extract_text(input_value)}")

        # Process through the agent
        message_result = await self.agent.invoke(input_value)
        
        # Send response back
        print(f"[SelfDiscoveryAgentExecutor] Sending back: {extract_text(message_result)}")
        await event_queue.enqueue_event(message_result)

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")

class DatingCoachAgentExecutor:
    def __init__(self):
        self.agent = DatingCoachAgent(self_discovery_client=None)

    async def execute(self, message: Message) -> AsyncGenerator[Message, None]:
        response = await self.agent.invoke(message)
        yield response
