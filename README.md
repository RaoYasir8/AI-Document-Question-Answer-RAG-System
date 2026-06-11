# AI Document Question-Answering System using LLMs and RAG

This project is a production-style AI document question-answering system. It uses **FastAPI, LangChain, embeddings, ChromaDB vector store, and Groq LLM** to answer questions from uploaded PDF documents.

---

## 🚀 Features

- Upload PDF documents
- Extract text from PDF files
- Clean and preprocess text
- Split text into chunks
- Generate embeddings
- Store embeddings in ChromaDB
- Perform semantic search
- RAG (Retrieval-Augmented Generation) architecture
- Context-aware answers using Groq LLM
- Return answers with source chunks
- Simple frontend using HTML, CSS, and JavaScript

---

## 🧠 Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- Groq LLM API
- ChromaDB
- HuggingFace Sentence Transformers
- PyPDF
- Pydantic

### Frontend
- HTML
- CSS
- JavaScript

---

## ⚙️ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env