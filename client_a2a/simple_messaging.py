import asyncio
from typing import List, Optional, Tuple

from urllib.parse import urljoin
import httpx

from a2a.client import ClientFactory
from a2a.client.client import ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Message, TextPart

SERVER_PORTS: List[int] = [9999, 9998, 9997, 9996]

async def fetch_agent_card(
    base_url: str, httpx_client: httpx.AsyncClient
) -> Optional[AgentCard]:
    url = urljoin(base_url, "/.well-known/agent-card.json")
    try:
        resp = await httpx_client.get(url, timeout=5.0)
        resp.raise_for_status()
        card = AgentCard.model_validate(resp.json())
        # Replace the placeholder URL in the card with the actual base URL used to fetch it.
        # This ensures the client uses the correct, reachable address.
        card.url = base_url + "/"
        return card
    except Exception as exc:
        print(f"Failed to fetch agent-card from {url}: {exc}")
        return None


# async def send_and_collect(
#     client_factory: ClientFactory, card: AgentCard, content: str | Message
# ) -> Tuple[Optional[str], Optional[Message]]: # This is the original function signature

async def send_and_collect( # This is the original function signature
    client_factory: ClientFactory, card: AgentCard, content: str | Message) -> Tuple[Optional[str], Optional[Message]]:
    """Send `content` to the agent described by `card` and return the first text reply (if any)."""
    client = client_factory.create(card)
    message: Message = (
        content
        if isinstance(content, Message)
        else create_text_message_object(content=content)
    )

    text_to_user, message_to_agent = None, None
    try:
        print(f"Sending to agent: {card.url} | Content: {content}")
        async for event in client.send_message(message):
            if not isinstance(event, Message):
                continue
            # print raw event for debugging
            # print(f"[to {card.url}] EVENT: {event}")
            parts = event.parts
            if isinstance(parts, list) and parts:
                # attempt to extract a text payload from 1st part for user
                text_part = parts[0].root
                if isinstance(text_part, TextPart) and text_to_user is None:
                    text_to_user = text_part.text
            if isinstance(parts, list) and len(parts) >= 2:
                # assume 2nd part is for agent
                if message_to_agent is None:
                    message_to_agent = Message(
                        message_id=event.message_id,
                        parts=[parts[1]],
                        role=event.role,
                    )
        print(f"Received from agent: {text_to_user}")
    except Exception as exc:
        print(f"Error while sending message to {card.url}: {exc}")

    return text_to_user, message_to_agent


async def simple_messaging_via_client():
    async with httpx.AsyncClient() as httpx_client:
        config = ClientConfig(
            httpx_client=httpx_client, supported_transports=["JSONRPC"]
        )
        factory = ClientFactory(config)

        # Fetch both agent cards
        card1 = await fetch_agent_card(f"http://localhost:{SERVER_PORTS[0]}", httpx_client)
        card2 = await fetch_agent_card(f"http://localhost:{SERVER_PORTS[1]}", httpx_client)
        if not card1 or not card2:
            print("Failed to fetch both agent cards; aborting.")
            return

        # client1 -> agent1
        print("\n--- client1 -> agent1 ---")
        client1_message = "hello!"
        agent1_to_user, agent1_to_agent = await send_and_collect(
            factory, card1, client1_message
        )
        print(f"agent1_reply (collected by client1): {agent1_to_user}")

        # client1 -> client2 (simulate transfer of agent1's reply as a client message)
        print("\n--- client1 forwards agent1 reply to client2 (simulated) ---")
        client2_message = (
            agent1_to_agent if agent1_to_agent is not None else "(no reply from agent1)"
        )

        # client2 -> agent2
        print("\n--- client2 -> agent2 ---")
        agent2_to_user, agent2_to_agent = await send_and_collect(
            factory, card2, client2_message
        )
        print(f"agent2_reply (collected by client2): {agent2_to_user}")


if __name__ == "__main__":
    asyncio.run(simple_messaging_via_client())
