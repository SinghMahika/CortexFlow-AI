from langchain_openai import ChatOpenAI
from app.core.settings import settings

llm = ChatOpenAI(
    model=settings.MODEL_NAME,      # or whichever model you're using
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)