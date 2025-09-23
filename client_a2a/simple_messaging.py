import asyncio
from typing import List, Optional

import httpx

from a2a.client import ClientFactory
from a2a.client.client import ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Message

SERVER_PORTS: List[int] = [9999, 9998]


async def fetch_agent_card(
    port: int, httpx_client: httpx.AsyncClient
) -> Optional[AgentCard]:
    url = f"http://localhost:{port}/.well-known/agent-card.json"
    try:
        resp = await httpx_client.get(url, timeout=5.0)
        resp.raise_for_status()
        return AgentCard.model_validate(resp.json())
    except Exception as exc:
        print(f"Failed to fetch agent-card from {url}: {exc}")
        return None


async def send_and_collect(
    client_factory: ClientFactory, card: AgentCard, content: str
) -> Optional[str]:
    """Send `content` to the agent described by `card` and return the first text reply (if any)."""
    client = client_factory.create(card)
    message: Message = create_text_message_object(content=content)

    first_text = None
    try:
        async for event in client.send_message(message):
            # print raw event for debugging
            print(f"[to {card.url}] EVENT: {event}")
            # attempt to extract a text payload from the event
            parts = getattr(event, "parts", None)
            if parts:
                p = parts[0]
                root = getattr(p, "root", None)
                if root is not None:
                    text = getattr(root, "text", None)
                elif isinstance(p, dict):
                    inner = p.get("root") or p
                    text = inner.get("text") if isinstance(inner, dict) else None
                else:
                    text = None

                if text:
                    if first_text is None:
                        first_text = text
    except Exception as exc:
        print(f"Error while sending message to {card.url}: {exc}")

    return first_text


async def simple_messaging_via_client():
    async with httpx.AsyncClient() as httpx_client:
        config = ClientConfig(
            httpx_client=httpx_client, supported_transports=["JSONRPC"]
        )
        factory = ClientFactory(config)

        # Fetch both agent cards
        card1 = await fetch_agent_card(SERVER_PORTS[0], httpx_client)
        card2 = await fetch_agent_card(SERVER_PORTS[1], httpx_client)
        if not card1 or not card2:
            print("Failed to fetch both agent cards; aborting.")
            return

        # client1 -> agent1
        print("\n--- client1 -> agent1 ---")
        client1_message = "hello!"
        agent1_reply = await send_and_collect(factory, card1, client1_message)
        print(f"agent1_reply (collected by client1): {agent1_reply}")

        # client1 -> client2 (simulate transfer of agent1's reply as a client message)
        print("\n--- client1 forwards agent1 reply to client2 (simulated) ---")
        if agent1_reply is None:
            print("No reply from agent1 to forward; sending default payload to client2")
            agent1_reply = "(no reply from agent1)"
        client2_message = agent1_reply

        # client2 -> agent2
        print("\n--- client2 -> agent2 ---")
        agent2_reply = await send_and_collect(factory, card2, client2_message)
        print(f"agent2_reply (collected by client2): {agent2_reply}")


if __name__ == "__main__":
    asyncio.run(simple_messaging_via_client())
