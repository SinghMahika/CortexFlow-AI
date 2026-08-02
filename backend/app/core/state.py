from typing import TypedDict, List, Dict


class GraphState(TypedDict):
    user_query: str
    intent: str

    retrieved_documents: list
    sql_query: str
    sql_result: list

    final_response: str
    sources: list