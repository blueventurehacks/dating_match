import httpx
import asyncio

from a2a.client import ClientFactory
from a2a.client.client import ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Message


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        # Configure factory to prefer JSON-RPC transport explicitly
        config = ClientConfig(
            httpx_client=httpx_client, supported_transports=["JSONRPC"]
        )
        factory = ClientFactory(config)

        # Fetch the agent card from the server's well-known endpoint
        resp = await httpx_client.get(
            "http://localhost:9999/.well-known/agent-card.json"
        )
        resp.raise_for_status()
        card = AgentCard.model_validate(resp.json())

        # Create a client for this agent
        client = factory.create(card)

        # Build a Message object using helper (ensures valid shape)
        message: Message = create_text_message_object(
            content="how much is 10 USD in INR?"
        )

        # send_message returns an async iterator of events/messages
        async for event in client.send_message(message):
            print(event)


if __name__ == "__main__":
    asyncio.run(main())
