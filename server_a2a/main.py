import uvicorn
from .agent_executor import HelloWorldAgentExecutor, HiThereAgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore  # For task state management
from agents.agent_hello import hello_agent_card
from agents.agent_hi import hi_agent_card


def run_server1() -> None:
    # 1. Define the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),  # For task state management
    )

    # 2. Build the server using imported agent card
    server = A2AStarletteApplication(
        agent_card=hello_agent_card, http_handler=request_handler
    )

    # 3. Start the server with Uvicorn
    uvicorn.run(server.build(), host="0.0.0.0", port=9999)


def run_server2() -> None:
    # 1. Define the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=HiThereAgentExecutor(),
        task_store=InMemoryTaskStore(),  # For task state management
    )

    # 2. Build the server using imported agent card
    server = A2AStarletteApplication(
        agent_card=hi_agent_card, http_handler=request_handler
    )

    # 3. Start the server with Uvicorn
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
