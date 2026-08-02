from app.core.state import GraphState
from app.core.snowflake_client import complete
from app.prompts.router_prompt import ROUTER_PROMPT


def intent_router_node(state: GraphState) -> GraphState:
    """
    Classifies the user's query into one of:
    CHAT, SQL, RAG, or HYBRID.
    """

    prompt = ROUTER_PROMPT.format(
        question=state["user_query"]
    )

    response = complete(prompt)

    intent = response.strip().upper()

    valid = {
        "RAG",
        "SQL",
        "HYBRID",
        "CHAT"
    }

    if intent not in valid:
        intent = "CHAT"

    state["intent"] = intent

    return state