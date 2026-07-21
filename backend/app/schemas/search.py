from pydantic import BaseModel


class SearchRequest(BaseModel):
    question: str

class SourceResponse(BaseModel):
    document: str
    chunk_index: int
    distance: float
    preview: str


class RAGResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]