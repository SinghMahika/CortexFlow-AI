from app.core.state import GraphState
from app.core.snowflake_client import execute_read_only_sql, generate_sql

def sql_node(state: GraphState):
    sql = generate_sql(state["user_query"])
    result = execute_read_only_sql(sql)
    state["sql_query"] = sql
    state["sql_result"] = result
    return state