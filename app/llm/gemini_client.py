from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings


def get_gemini_client():

    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.2
    )

    return llm