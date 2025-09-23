import uvicorn
from .agent_executor import HelloWorldAgentExecutor, HiThereAgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore  # For task state management
from a2a.types import AgentCapabilities, AgentCard, AgentSkill


def run_server1() -> None:
    # 1. Define the skill
    skill = AgentSkill(
        id="hello_world",
        name="Returns hello world",
        description="just returns hello world",
        tags=["hello world"],
        examples=["hi", "hello world"],
    )

    # 2. Define the agent card
    agent_card = AgentCard(
        name="Hello World Agent",
        description="Just a hello world agent",
        url="http://localhost:9999/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # 3. Define the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),  # For task state management
    )

    # 4. Build the server
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    # 5. Start the server with Uvicorn
    uvicorn.run(server.build(), host="0.0.0.0", port=9999)


def run_server2() -> None:
    # 1. Define the skill
    skill = AgentSkill(
        id="hi_there",
        name="Returns hi there",
        description="just returns hi there",
        tags=["hi there"],
        examples=["hi", "hi there"],
    )

    # 2. Define the agent card
    agent_card = AgentCard(
        name="Hi There Agent",
        description="Just a hi there agent",
        url="http://localhost:9998/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # 3. Define the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=HiThereAgentExecutor(),
        task_store=InMemoryTaskStore(),  # For task state management
    )

    # 4. Build the server
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    # 5. Start the server with Uvicorn
    uvicorn.run(server.build(), host="0.0.0.0", port=9998)


if __name__ == "__main__":
    import multiprocessing

    # Run both servers in separate processes
    p1 = multiprocessing.Process(target=run_server1)
    p2 = multiprocessing.Process(target=run_server2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
