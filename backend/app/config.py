from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Directories
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Create directories if not exist
UPLOAD_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    ALLOWED_ORIGINS: str = (
        "http://localhost:5500,"
        "http://127.0.0.1:5500,"
        "http://localhost:8000"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()


def get_allowed_origins() -> list[str]:
    return [
        origin.strip()
        for origin in settings.ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ]