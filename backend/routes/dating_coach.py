import os
import httpx
from urllib.parse import urljoin
import google.generativeai as genai
from google.generativeai import types
from flask import Blueprint, request, jsonify
from client_a2a.simple_messaging import send_and_collect, fetch_agent_card
from a2a.client import ClientFactory
from a2a.client.client import ClientConfig

dating_coach_bp = Blueprint('dating_coach', __name__, url_prefix='/dating_coach')

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-001',
    tools=[],
    system_instruction="""
            You are a friendly, pragmatic, and empathetic dating coach chatbot for people. 
            Your job is to help any user improve dating outcomes (profiles, messaging, flirting, confidence, date planning, boundaries) 
            while preserving safety and privacy.

            Rules and Behaviors:
                1. Begin by welcoming the user and offering a quick, low-effort way to get help (choose a topic or answer a short intake question)
                2. Ask short, optional intake questions to gather relevant context only when necessary. Always offer a “skip” option.
                3. Keep tone adaptable: default to warm and encouraging; switch to direct/tough-love or playful if the user requests it.
                4. Provide very short, concrete, actionable suggestions (scripts, message examples, step-by-step plans) and explain why each suggestion works.
                5. Never give medical, legal, or mental-health clinical advice. If a user’s issue requires professional help (e.g., severe social anxiety, suicidal ideation, abuse), 
                provide a supportive refusal and recommend seeking a qualified professional and emergency resources.
                6. If user asks for manipulative, deceptive, illegal, or harassing tactics, refuse and explain why; instead provide ethical, consent-respecting alternatives.
                7. When the user asks for profile editing or message review, always include: (1) a direct example, (2) a shorter/concise variant, and (3) a one-sentence explanation of the change.
                8. If user is ambiguous, offer 2–3 common interpretations and proceed with the most helpful by default (no endless clarifying questions).
                9. End answers with an explicit next step prompt (e.g., “Want me to roleplay this message with you?”).
        """
)

def get_a2a_host() -> str:
    """
    Determines the correct host for A2A communication.
    - 'host.docker.internal' if backend is in Docker and A2A server is on the host.
    - 'localhost' for local development.
    """
    if os.getenv("A2A_ON_HOST") == "1":
        return "http://host.docker.internal"
    return "http://localhost"

@dating_coach_bp.route('/message', methods=['POST'])
async def handle_dating_coach_chat():
    payload = request.get_json()
    user_message = payload.get("message")
    user_id = payload.get("userId")

    if not user_message:
        return jsonify({"message": "Missing message"}), 400
    
    sd_reply = None
    # If a user is logged in, consult the self-discovery agent for context.
    if user_id:
        # 1. Use A2A protocol to get self-discovery agent's reply
        async with httpx.AsyncClient(timeout=30.0) as httpx_client:
            config = ClientConfig(httpx_client=httpx_client, supported_transports=["JSONRPC"])
            factory = ClientFactory(config)
    
            # Get self-discovery agent card
            host = get_a2a_host()
            self_discovery_card = await fetch_agent_card(f"{host}:9997", httpx_client)
            if not self_discovery_card:
                print("[DatingCoach] Warning: Could not connect to self-discovery agent. Proceeding without context.")
            else:
                # Use A2A to get self-discovery agent's reply
                sd_reply, _ = await send_and_collect(
                    factory,
                    self_discovery_card,
                    f"User {user_id} says: {user_message}"
                )
                print(f"[DatingCoach] Received from SelfDiscoveryAgent: {sd_reply}")
    
    # Compose a prompt for the dating coach Gemini bot
    if sd_reply:    
        prompt = (
            f"A user is asking for dating advice. Here is their message: '{user_message}'\n\n"
            f"The self-discovery assistant's reply to the user's message was: '{sd_reply}'\n\n"
            "Based on BOTH the user's direct message and the context from the self-discovery assistant, provide your best dating advice."
        )

    else:
        # If no context from self-discovery agent, use a simpler prompt
        prompt = user_message
    
    # Get response from Gemini dating coach model
    response = model.start_chat(enable_automatic_function_calling=True).send_message(prompt)
    coach_reply = response.text
    
    return jsonify({"reply": coach_reply}), 200
