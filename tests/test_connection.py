from backend.app.core.snowflake_client import execute_read_only_sql

result = execute_read_only_sql("SELECT COUNT(*) FROM ENTERPRISE_AI_DB.CURATED.EMPLOYEES")

print(result)