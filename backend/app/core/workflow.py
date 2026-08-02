from langgraph.graph import END, START, StateGraph
from app.core.state import GraphState
from app.nodes.chat import chat_node
from app.nodes.hybrid import hybrid_node
from app.nodes.intent_router_node import intent_router_node
from app.nodes.rag import rag_node
from app.nodes.sql import sql_node
from app.nodes.synthesizer import synthesizer_node


def route(state: GraphState) -> str:
    return state["intent"]


workflow = StateGraph(GraphState)
workflow.add_node("intent_router", intent_router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("sql", sql_node)
workflow.add_node("hybrid", hybrid_node)
workflow.add_node("chat", chat_node)
workflow.add_node("synthesizer", synthesizer_node)
workflow.add_edge(START, "intent_router")
workflow.add_conditional_edges(
    "intent_router",
    route,
    {
        "RAG": "rag",
        "SQL": "sql",
        "HYBRID": "hybrid",
        "CHAT": "chat",
        "UNKNOWN": "chat",
    },
)
workflow.add_edge("rag", "synthesizer")
workflow.add_edge("sql", "synthesizer")
workflow.add_edge("hybrid", "synthesizer")
workflow.add_edge("synthesizer", END)
workflow.add_edge("chat", END)
graph = workflow.compile()


def run_workflow(user_query: str) -> dict[str, object]:
    result = graph.invoke(
        {
            "user_query": user_query,
            "intent": "",
            "retrieved_documents": [],
            "sql_query": "",
            "sql_result": [],
            "final_response": "",
            "sources": [],
        }
    )
    return {
    "response": result["final_response"],
    "sources": result.get("sources", []),
    "intent": result.get("intent"),
    "generated_sql": result.get("sql_query"),
}