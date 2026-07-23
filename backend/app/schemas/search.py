from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    question: str = Field(
        ...,
        description=(
            "Question to answer using information from uploaded documents."
        ),
        examples=[
            "What operating system is recommended?"
        ],
    )


class SourceResponse(BaseModel):
    document: str = Field(
        ...,
        description="Name of the source document.",
        examples=[
            "employee_handbook.pdf"
        ],
    )

    page: int | None = Field(
        None,
        description="Page number where the information was found.",
        examples=[
            4
        ],
    )

    relevance: int = Field(
        ...,
        description=(
            "Similarity score indicating how relevant the source is "
            "to the question."
        ),
        examples=[
            92
        ],
    )

    preview: str = Field(
        ...,
        description="Short preview of the retrieved document content.",
        examples=[
            "Employees should use Linux as the recommended development environment."
        ],
    )


class RAGResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Generated answer based only on retrieved document context.",
        examples=[
            "The recommended operating system is Linux."
        ],
    )

    sources: list[SourceResponse] = Field(
        ...,
        description="Documents used to generate the answer.",
    )