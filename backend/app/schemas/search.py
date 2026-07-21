from pydantic import BaseModel


class SearchRequest(BaseModel):
    question: str

class SourceResponse(BaseModel):
    document: str
    relevance: int
    preview: str


class RAGResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]