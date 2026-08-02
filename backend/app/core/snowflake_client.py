import json
import re
from typing import Any
import snowflake.connector
from snowflake.core import Root
from app.core.settings import settings

def connect() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=settings.SNOWFLAKE_ACCOUNT,
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_TOKEN,
        warehouse=settings.SNOWFLAKE_WAREHOUSE,
        database=settings.SNOWFLAKE_DATABASE,
        schema=settings.SNOWFLAKE_SCHEMA,
        role=settings.SNOWFLAKE_ROLE,
    )

def complete(prompt: str) -> str:
    """Use Snowflake Cortex rather than an external OpenAI API key."""
    with connect() as connection:
        with connection.cursor() as cursor:
            # COMPLETE is widely available today. Keep the model configurable in .env.
            cursor.execute(
                "SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s)",
                (settings.SNOWFLAKE_CORTEX_MODEL, prompt),
            )
            row = cursor.fetchone()
    return str(row[0]) if row else ""


def search_policies(query: str, category: str | None = None, limit: int = 4) -> list[dict[str, Any]]:
    """Retrieve policy chunks from the existing Cortex Search service."""
    with connect() as connection:
        root = Root(connection)
        service = (
            root.databases[settings.SNOWFLAKE_DATABASE]
            .schemas[settings.SNOWFLAKE_SEARCH_SCHEMA]
            .cortex_search_services[settings.SNOWFLAKE_SEARCH_SERVICE]
        )
        filter_value = {"@eq": {"category": category}} if category else None
        response = service.search(
            query=query,
            columns=["chunk_text", "document_name", "category", "section_title"],
            filter=filter_value,
            limit=limit,
        )
    return json.loads(response.to_json()).get("results", [])


def hr_schema() -> str:
    """Read the table definitions so text-to-SQL is tied to the actual Snowflake tables."""
    descriptions: list[str] = []
    with connect() as connection:
        with connection.cursor() as cursor:
            for table in ("EMPLOYEES", "LEAVE_BALANCES"):
                cursor.execute(f"DESC TABLE {settings.SNOWFLAKE_DATABASE}.CURATED.{table}")
                columns = cursor.fetchall()
                descriptions.append(
                    f"{settings.SNOWFLAKE_DATABASE}.CURATED.{table}: "
                    + ", ".join(f"{column[0]} {column[1]}" for column in columns)
                )
    return "\n".join(descriptions)


def execute_read_only_sql(sql: str) -> list[dict[str, Any]]:
    """Allow only a single read-only query from the SQL-generation node."""
    statement = sql.strip().rstrip(";")
    if not re.match(r"^(SELECT|WITH)\b", statement, flags=re.IGNORECASE):
        raise ValueError("Only SELECT or WITH queries are allowed.")
    if ";" in statement or re.search(
        r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|GRANT|REVOKE|CALL|COPY|PUT|GET)\b",
        statement,
        flags=re.IGNORECASE,
    ):
        raise ValueError("The generated query is not read-only.")
    if not re.search(r"\bLIMIT\b", statement, flags=re.IGNORECASE):
        statement = f"{statement} LIMIT 50"

    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            column_names = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
    return [dict(zip(column_names, row)) for row in rows]

def generate_sql(question: str) -> str:
    """
    Convert a natural language question into a read-only SQL query.
    """

    schema = hr_schema()

    prompt = f"""
You are an expert Snowflake SQL generator.

You ONLY answer questions that require structured data.

Available tables:

{schema}

Important Rules:
- ONLY use the tables listed above.
- NEVER invent tables or columns.
- NEVER reference policy documents.
- NEVER reference leave policies, HR handbook, expense policy, company handbook, or PDFs.
- If the question contains both structured-data and policy questions, generate SQL ONLY for the structured-data portion.
- Ignore policy/document-related parts completely.
- Return ONLY valid Snowflake SQL.
- Do NOT use markdown.
- Do NOT explain anything.
- Use SELECT statements only.
- Use fully qualified table names.
- Add LIMIT 50 unless using an aggregate.

Question:
{question}

SQL:
"""

    sql = complete(prompt)

    # Remove markdown if the model returns ```sql
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql