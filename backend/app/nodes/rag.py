from app.core.state import GraphState
from app.core.snowflake_client import search_policies

def rag_node(state: GraphState):
    docs = search_policies(state["user_query"])
    state["retrieved_documents"] = docs
    state["sources"] = list(
    {
        doc["document_name"]
        for doc in docs
    }
)
    return state