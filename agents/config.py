import os

def get_agent_host():
    """
    Get the appropriate host for agent servers based on environment.
    - If running in Docker and A2A servers are on the host: use 'host.docker.internal'
    - If running in Docker and A2A servers are in Docker: use 'agent-servers'
    - Otherwise (local dev): use 'localhost'
    """
    if os.getenv("RUNNING_IN_DOCKER"):
        # Check if user wants to force host.docker.internal (set an env var if needed)
        if os.getenv("A2A_ON_HOST") == "1":
            return "host.docker.internal"
        return "agent-servers"
    return "localhost"

def get_agent_url(port: int) -> str:
    host = get_agent_host()
    return f"http://{host}:{port}/"

def get_backend_url() -> str:
    """
    Determines the correct host for the backend API.
    - 'http://localhost:5001' if running in Docker.
    - 'http://localhost:5001' for local development.
    """
    if os.getenv("RUNNING_IN_DOCKER"):
        return "http://localhost:5001"
    return "http://localhost:5001"