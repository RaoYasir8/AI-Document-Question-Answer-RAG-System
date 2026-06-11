from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.config import CHROMA_DIR, settings


# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
)

# Initialize vector store
vector_store = Chroma(
    collection_name="document_qa_collection",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)


def add_documents_to_vector_store(documents: list[Document]) -> int:
    if not documents:
        return 0

    vector_store.add_documents(documents)
    return len(documents)


def get_retriever(k: int = 4):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )