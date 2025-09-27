from typing import Union
from a2a.types import (
    AgentSkill, AgentCard, AgentCapabilities,
    Message, Role, Part, TextPart
)
from .utils import extract_text
import uuid

# Define Dating Coach Skills
dating_advice_skill = AgentSkill(
    id="dating_advice",
    name="Provide Dating Advice",
    description="Provides personalized dating advice based on personality type, attachment style, and relationship goals",
    tags=["dating", "advice", "relationships"],
    examples=[
        "How should an INFP approach dating?",
        "Dating tips for anxious attachment",
    ],
)

dating_coach_agent_card = AgentCard(
    name="Dating Coach Agent",
    description="A supportive dating coach that provides personalized advice based on user's personality and preferences",
    url="http://localhost:9996/",  # Different port from self-discovery agent
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[dating_advice_skill],
)

class DatingCoachAgent:
    """Dating coach agent that consults with self-discovery agent."""
    
    def __init__(self, self_discovery_client):
        self.self_discovery_client = self_discovery_client

    async def invoke(self, input_value: Union[str, Message, None] = None) -> Message:
        # Extract user's query
        user_text = extract_text(input_value)
        
        # Consult self-discovery agent for user's profile
        profile_response = await self.self_discovery_client.send_message(
            f"What do you know about this user's personality and preferences? Context: {user_text}"
        )
        profile_info = extract_text(profile_response)
        
        # Generate personalized advice based on both inputs
        advice = f"Based on your {profile_info}, here's my dating advice: {user_text}"
        
        # Create message parts for both user and agent
        user_part = Part(root=TextPart(text=advice, metadata={"receiver": "user"}))
        agent_part = Part(root=TextPart(text=advice, metadata={"receiver": "agent"}))
        
        return Message(
            message_id=uuid.uuid4().hex,
            parts=[user_part, agent_part],
            role=Role.agent,
        )