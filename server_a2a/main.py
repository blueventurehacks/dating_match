import uvicorn
from .agent_executor import HelloWorldAgentExecutor, HiThereAgentExecutor, SelfDiscoveryAgentExecutor, DatingCoachAgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore  # For task state management
from agents.agent_hello import hello_agent_card
from agents.agent_hi import hi_agent_card
from agents.dating_coach import dating_coach_agent_card
from agents.self_discovery import self_discovery_agent_card



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

def run_self_discovery_server() -> None:
    request_handler = DefaultRequestHandler(
        agent_executor=SelfDiscoveryAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    server = A2AStarletteApplication(
        agent_card=self_discovery_agent_card,
        http_handler=request_handler
    )
    
    uvicorn.run(server.build(), host="0.0.0.0", port=9997)

def run_dating_coach_server() -> None:
    request_handler = DefaultRequestHandler(
        agent_executor=DatingCoachAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    server = A2AStarletteApplication(
        agent_card=dating_coach_agent_card,
        http_handler=request_handler
    )
    
    uvicorn.run(server.build(), host="0.0.0.0", port=9996)


if __name__ == "__main__":
    import multiprocessing

    p1 = multiprocessing.Process(target=run_self_discovery_server)
    p2 = multiprocessing.Process(target=run_dating_coach_server)
    p3 = multiprocessing.Process(target=run_server1)
    p4 = multiprocessing.Process(target=run_server2)
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p3.join()
    p4.join()
