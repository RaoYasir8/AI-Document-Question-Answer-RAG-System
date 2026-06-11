from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# Text splitter configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""],
)


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = " ".join(text.split())
    return text.strip()


def load_pdf(file_path: Path) -> list[Document]:
    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    cleaned_documents = []

    for doc in documents:
        cleaned_content = clean_text(doc.page_content)

        if cleaned_content:
            cleaned_documents.append(
                Document(
                    page_content=cleaned_content,
                    metadata={
                        "source": file_path.name,
                        "page": doc.metadata.get("page", 0) + 1,
                    },
                )
            )

    return cleaned_documents


def process_pdf(file_path: Path) -> list[Document]:
    documents = load_pdf(file_path)
    chunks = text_splitter.split_documents(documents)
    return chunks