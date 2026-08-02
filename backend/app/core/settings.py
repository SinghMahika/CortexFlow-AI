from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    SNOWFLAKE_CORTEX_MODEL: str = "gpt-4o"
    SNOWFLAKE_ACCOUNT: str
    SNOWFLAKE_USER: str
    SNOWFLAKE_TOKEN: str
    SNOWFLAKE_DATABASE: str
    SNOWFLAKE_SCHEMA: str
    SNOWFLAKE_WAREHOUSE: str
    SNOWFLAKE_ROLE: str
    SNOWFLAKE_SEARCH_SCHEMA: str
    SNOWFLAKE_SEARCH_SERVICE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
