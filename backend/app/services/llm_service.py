from langchain_groq import ChatGroq

from app.core.config import settings


def get_llm():

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    return llm