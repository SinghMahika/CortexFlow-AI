from backend.app.core.snowflake_client import complete

answer = complete(
    "Say hello in one sentence."
)

print(answer)