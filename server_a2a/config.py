import os
from urllib.parse import urlparse

def get_agent_url(port: int) -> str:
    """
    Get the appropriate URL for the agent based on whether we're running in Docker or locally.
    
    Args:
        port (int): The port number the agent runs on
        
    Returns:
        str: The full URL for the agent
    """
    # When running in Docker, services can refer to each other by service name
    if os.getenv("RUNNING_IN_DOCKER"):
        return f"http://agent-servers:{port}/"
    # For local development
    return f"http://localhost:{port}/"