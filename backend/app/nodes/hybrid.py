from app.core.state import GraphState
from app.nodes.sql import sql_node
from app.nodes.rag import rag_node
from app.nodes.synthesizer import synthesizer_node


def hybrid_node(state: GraphState) -> GraphState:
    """
    Execute SQL and RAG, then synthesize the final answer.
    """

    state = sql_node(state)
    state = rag_node(state)
    state = synthesizer_node(state)

    return state