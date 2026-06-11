from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)


class SourceChunk(BaseModel):
    content: str
    source: str | None = None
    page: int | None = None


class QuestionResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int