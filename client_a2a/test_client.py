import httpx
import asyncio
from typing import List

from a2a.client import ClientFactory
from a2a.client.client import ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Message


SERVER_PORTS: List[int] = [9999, 9998]


async def query_agent(
    port: int, httpx_client: httpx.AsyncClient, factory: ClientFactory
) -> None:
    url = f"http://localhost:{port}/.well-known/agent-card.json"
    print(f"\n--- Connecting to server on port {port} ---")
    try:
        resp = await httpx_client.get(url, timeout=5.0)
        resp.raise_for_status()
    except Exception as exc:
        print(f"Failed to fetch agent-card from {url}: {exc}")
        return

    try:
        card = AgentCard.model_validate(resp.json())
    except Exception as exc:
        print(f"Failed to parse agent-card JSON from {url}: {exc}")
        return

    client = factory.create(card)

    message: Message = create_text_message_object(
        content=f"hello from test to port {port}"
    )

    try:
        async for event in client.send_message(message):
            print(f"[port {port}] {event}")
    except Exception as exc:
        print(f"Error while sending message to port {port}: {exc}")


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        config = ClientConfig(
            httpx_client=httpx_client, supported_transports=["JSONRPC"]
        )
        factory = ClientFactory(config)

        # Query each server sequentially
        for port in SERVER_PORTS:
            await query_agent(port, httpx_client, factory)


if __name__ == "__main__":
    asyncio.run(main())
