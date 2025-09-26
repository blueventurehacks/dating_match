from a2a.types import (
    AgentSkill,
    AgentCard,
    AgentCapabilities,
)


# 1) MBTI personality type collection and validation
mbti_skill = AgentSkill(
    id="collect_mbti",
    name="Collect and validate MBTI type",
    description=(
        "Ask and record the user's MBTI personality type. Must be one of the 16 official types: "
        "INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP. "
        "Handle partial answers by asking follow-ups."
    ),
    tags=["personality", "MBTI", "validation", "follow-up"],
    examples=[
        "I'm INFP",
        "Probably I or N",
        "Between ENFP and INFP",
    ],
)

# 2) Attachment style normalization and saving
attachment_style_skill = AgentSkill(
    id="collect_attachment_style",
    name="Collect and normalize attachment style",
    description=(
        "Ask and record the user's attachment style. Must be one of: "
        "Secure, Anxious, Avoidant, Fearful-Avoidant. Normalize fuzzy language such as "
        "'I think I'm clingy' -> Anxious, 'I need space' -> Avoidant, "
        "'I'm independent but still want connection' -> Fearful-Avoidant."
    ),
    tags=["attachment", "relationship", "normalization"],
    examples=[
        "I think I'm clingy",
        "I often need space",
        "I'm pretty comfortable relying on people",
    ],
)

# 3) Relationship goal capture
relationship_goal_skill = AgentSkill(
    id="collect_relationship_goal",
    name="Collect relationship goal",
    description=(
        "Ask and record the user's relationship goal, e.g., casual dating, long-term relationship, friendship, etc."
    ),
    tags=["relationship", "goal", "dating"],
    examples=[
        "Looking for something casual",
        "I'm hoping for a long-term relationship",
        "Open to friendship for now",
    ],
)

# 4) Hobbies and interests summary
hobbies_skill = AgentSkill(
    id="collect_hobbies",
    name="Collect hobbies and interests",
    description=(
        "Ask and record a brief summary of the user's hobbies and interests. Save as a concise profile summary."
    ),
    tags=["hobbies", "interests", "profile"],
    examples=[
        "I love hiking and cooking",
        "Reading, yoga, and indie films",
    ],
)

# 5) Guided, supportive conversation flow
guided_conversation_skill = AgentSkill(
    id="guided_conversation",
    name="Guided and supportive conversation",
    description=(
        "Keep the conversation casual, helpful, and supportive. Ask targeted questions to elicit details, "
        "limit to 2-3 questions per response to avoid overwhelming the user, and if the user only answers part, "
        "follow up on missing pieces in a reworded form. Save any provided info immediately."
    ),
    tags=["conversation", "guidance", "supportive", "follow-up", "limits"],
    examples=[
        "Thanks for sharing! Two quick questions to help clarify...",
        "You mentioned you might be 'I'—could you share whether you also lean 'N, S, T, or F'?",
    ],
)


self_discovery_agent_card = AgentCard(
    name="Self Discovery Agent",
    description=(
        "A friendly self-discovery assistant that helps users reflect and records MBTI, attachment style, "
        "relationship goals, and hobbies while keeping a supportive, concise dialogue."
    ),
    url="http://localhost:9997/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[
        mbti_skill,
        attachment_style_skill,
        relationship_goal_skill,
        hobbies_skill,
        guided_conversation_skill,
    ],
)
