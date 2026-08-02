from app.core.state import GraphState
from app.core.snowflake_client import complete


def chat_node(state: GraphState) -> GraphState:
    """
    General conversational node.
    """

    prompt = f"""
You are CortexFlow AI, an enterprise AI assistant.

Responsibilities:
- Answer greetings naturally.
- Answer general knowledge questions briefly.
- Be professional and concise.
- If the question requires company data or policy information,
  answer only using the appropriate workflow (already handled by LangGraph).

User Question:
{state["user_query"]}

Answer:
"""

    state["final_response"] = complete(prompt)

    return state