import os
import json
import google.generativeai as genai
from google.generativeai import types
from flask import Blueprint, request, jsonify
from models import db, User

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

# --- Define the Functions for Gemini ---

def save_user_hobbies(user_id: int, hobbies: str):
    """
    Saves the user's hobbies to their profile.

    Args:
        user_id (int): The ID of the user to update.
        hobbies (str): A summary of the user's hobbies.
    """
    try:
        user = db.session.get(User, user_id)
        if not user:
            return f"Cannot find user with ID {user_id}."

        user.hobbies = hobbies
        db.session.commit()
        return f"Successfully updated hobbies  for {user.first_name}."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def save_user_mbti(user_id: int, mbti_type: str):
    """
    Saves the user's MBTI personality type to their profile.

    Args:
        user_id (int): The ID of the user.
        mbti_type (str): The user's MBTI type (e.g., INFP, ESTJ).
    """
    valid_mbti_types = {
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    }

    mbti_type = mbti_type.upper()

    if mbti_type not in valid_mbti_types:
        return f"'{mbti_type}' is not a valid MBTI type."

    try:
        user = db.session.get(User, user_id)
        if not user:
            return f"Cannot find user with ID {user_id}."

        user.mbti = mbti_type
        db.session.commit()
        return f"Saved {mbti_type} as {user.first_name}'s MBTI type."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def save_user_attachment_style(user_id: int, attachment_style: str):
    """Saves the user's attachment style."""
    valid_styles = {
        "Secure", "Anxious", "Avoidant", "Fearful-Avoidant"
    }

    attachment_style = attachment_style.title()
    if attachment_style not in valid_styles:
        return f"'{attachment_style}' is not a valid attachment style."

    try:
        user = db.session.get(User, user_id)
        if not user:
            return f"Cannot find user with ID {user_id}."
        user.attachment_style = attachment_style
        db.session.commit()
        return f"Saved {attachment_style} as {user.first_name}'s attachment style."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}" 

def save_user_relationship_goal(user_id: int, relationship_goal: str):
    """Saves the user's relationship goal."""
    try:
        user = db.session.get(User, user_id)
        if not user:
            return f"Cannot find user with ID {user_id}."
        user.relationship_goal = relationship_goal
        db.session.commit()
        return f"Saved relationship goal for {user.first_name}."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

# --- Configure the Gemini Model ---

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-001',
    tools=[
        save_user_hobbies,
        save_user_mbti,
        save_user_attachment_style,
        save_user_relationship_goal
    ],
    system_instruction="""
            You are a friendly self-discovery assistant. Your job is to help users reflect on themselves and save the following information:

                1. MBTI personality type (must be one of the 16 official MBTI types like INFP, ESTJ, etc.)
                2. Attachment style (must be one of: Secure, Anxious, Avoidant, Fearful-Avoidant)
                3. Relationship goal (e.g., casual dating, long-term relationship, friendship, etc.)
                4. Hobbies and interests (a brief summary of the user's hobbies)
            
            Guidelines:
                1. If a user provides even one piece of information, save it immediately by calling the appropriate function.
                2. For MBTI, users may give partial answers like "I and/or N" -- ask follow-up questions to complete it.
                3. Normalize fuzzy answers. For example:
                    - "I think I'm clingy" -> Anxious
                    - "I need space" -> Avoidant
                    - "I'm independent but still want connection" -> Fearful-Avoidant
                4. Keep the conversation casual, helpful, and informative -- like a supportive coach or therapist.
                5. Consistently prompt the user with targeted questions designed to elicit specific details that help you gather the required information, 
                   but limit the number of questions in each response to 2 or 3, depending on the flow of the conversation. The user should not feel overwhelmed.
                6. If the user only answers part of the previous response, try to ask the missing pieces in a reworded question.
        """
)

@chat_bp.route('/message', methods=['POST'])
def handle_chat():
    payload = request.get_json()
    user_message = payload.get("message")
    user_id = payload.get("userId")

    if not all([user_message, user_id]):
        return jsonify({"message": "Missing message or userId"}), 400

    # Start chat session with function calling enabled
    chat_session = model.start_chat(enable_automatic_function_calling=True)

    # Send user message. The library will automatically handle the function calling loop.
    # By providing context about the user, the model can infer the user_id for the function call.
    response = chat_session.send_message(
        f"The user with ID {user_id} says: {user_message}"
    )

    # The final response text will be the model's textual reply to the user.
    bot_response = response.text

    return jsonify({"reply": bot_response}), 200
