import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import UPLOAD_DIR
from app.document_processor import process_pdf
from app.rag_service import answer_question
from app.schemas import QuestionRequest, QuestionResponse, UploadResponse
from app.vector_store import add_documents_to_vector_store


router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Document Q/A RAG API is running",
    }


@router.post("/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # Unique filename (avoid overwrite)
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # Save file (safe write)
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                f.write(chunk)

        # Process and index
        chunks = process_pdf(file_path)
        chunks_count = add_documents_to_vector_store(chunks)

        return UploadResponse(
            message="Document uploaded and indexed successfully.",
            filename=unique_filename,
            chunks_created=chunks_count,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(exc)}",
        )


@router.post("/documents/ask", response_model=QuestionResponse)
async def ask_document_question(request: QuestionRequest):
    try:
        result = await answer_question(request.question)

        return QuestionResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {str(exc)}",
        )