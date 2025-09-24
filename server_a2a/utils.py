from typing import Any, Optional

from a2a.server.agent_execution import RequestContext


def get_input_value_from_context(context: RequestContext) -> Optional[Any]:
    """Extract message object or user text from RequestContext.

    Prefer returning the full Message-like object (if present on context.message);
    otherwise return a trimmed user text string or None.
    """
    try:
        message_obj = getattr(context, "message", None)
    except Exception:
        message_obj = None

    if message_obj is not None:
        return message_obj

    try:
        user_text = context.get_user_input()
    except Exception:
        user_text = None

    if isinstance(user_text, str):
        user_text = user_text.strip()
        return user_text or None

    return user_text
