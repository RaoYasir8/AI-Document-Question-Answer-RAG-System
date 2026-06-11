from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_allowed_origins
from app.routes import router


app = FastAPI(
    title="AI Document Question-Answering RAG System",
    description=(
        "A production-style document Q/A system using FastAPI, "
        "LangChain, embeddings, vector search, and Groq LLM."
    ),
    version="1.0.0",
)


# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Document Q/A RAG API",
        "docs": "/docs",
        "upload_endpoint": "/api/documents/upload",
        "ask_endpoint": "/api/documents/ask",
    }