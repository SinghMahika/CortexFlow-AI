from backend.app.core.snowflake_client import search_policies

docs = search_policies(
    "What is the leave policy?"
)

print(docs)