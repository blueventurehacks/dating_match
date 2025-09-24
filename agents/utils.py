from typing import Optional, Union
from a2a.types import Message, TextPart


def extract_text(input_value: Union[str, Message, None]) -> Optional[str]:
    """Normalize input that may be a str or a Message-like object to a trimmed str or None.

    Tries common attribute names (text, content, parts). Falls back to str().
    """
    if input_value is None:
        return None

    if isinstance(input_value, str):
        s = input_value.strip()
        return s or None

    for part in input_value.parts:
        if isinstance(part.root, TextPart):
            if part.root.text:
                return part.root.text.strip()

    # As a last resort try the object's string representation
    try:
        s = str(input_value).strip()
        return s or None
    except Exception:
        return None
