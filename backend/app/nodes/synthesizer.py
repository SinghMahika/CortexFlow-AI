from app.core.state import GraphState
from app.core.snowflake_client import complete

def synthesizer_node(state: GraphState):

    prompt = f"""
    You are an enterprise AI assistant.

    User Question:
    {state['user_query']}

    Intent:
    {state['intent']}

    Retrieved Documents:
    {state['retrieved_documents']}

    SQL Result:
    {state['sql_result']}

    Provide a helpful answer using the available information.
    """
    answer = complete(prompt)
    state["final_response"] = answer

    return state