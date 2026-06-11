# AI Document Upload Chatbot Q&A

This project is an AI document question-answering chatbot. It allows users to upload a PDF document and ask questions about its content.

The backend reads the uploaded PDF, extracts text, splits it into chunks, stores the chunks in a ChromaDB vector store, and then uses a Groq LLM with LangChain RAG to answer questions from the uploaded document. The frontend provides a simple browser interface for uploading PDFs and asking questions.

## Features

- Upload PDF documents
- Extract and clean PDF text
- Split document text into smaller chunks
- Generate embeddings using HuggingFace sentence transformers
- Store document embeddings in ChromaDB
- Ask questions about uploaded documents
- Generate answers using Groq LLM
- Show source chunks with document name and page number
- FastAPI backend
- HTML, CSS, and JavaScript frontend
- Docker support for backend deployment

## Project Structure

```text
ai-document-upload-chatboat-QA/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py               # Environment settings and paths
│   │   ├── document_processor.py   # PDF loading, cleaning, and chunking
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── rag_service.py          # RAG chain and LLM response logic
│   │   ├── routes.py               # API routes for upload and Q&A
│   │   ├── schemas.py              # Request and response models
│   │   └── vector_store.py         # ChromaDB and embedding setup
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html                  # Upload and Q&A interface
│   ├── script.js                   # Frontend API calls
│   └── style.css                   # UI styling
│
├── .gitignore
└── README.md
```

## Requirements

Make sure you have the following installed:

- Python 3.10 or later
- pip
- A Groq API key
- A browser

The first run may take some time because the embedding model needs to be downloaded.

## Backend Setup

Go to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

For Windows:

```bash
venv\Scripts\activate
```

For macOS or Linux:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:

```env
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000
```

Do not upload your real `.env` file to GitHub. Use `.env.example` for public repositories.

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI docs will be available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open a second terminal and go to the frontend folder:

```bash
cd frontend
```

Start a local frontend server:

```bash
python -m http.server 5500
```

Open this URL in your browser:

```text
http://localhost:5500
```

## How to Use

1. Start the backend server.
2. Start the frontend server.
3. Open the frontend in your browser.
4. Upload a PDF file.
5. Wait until the document is uploaded and indexed.
6. Ask questions about the uploaded document.

Example questions:

```text
What is the main topic of this document?
```

```text
Summarize this document.
```

```text
What are the key points mentioned in the PDF?
```

```text
Which page talks about the conclusion?
```

## API Endpoints

### Root

```http
GET /
```

Returns a welcome message with available API paths.

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok",
  "message": "Document Q/A RAG API is running"
}
```

### Upload Document

```http
POST /api/documents/upload
```

This endpoint accepts a PDF file using form data.

Form field name:

```text
file
```

Example response:

```json
{
  "message": "Document uploaded and indexed successfully.",
  "filename": "generated_filename.pdf",
  "chunks_created": 12
}
```

### Ask a Question

```http
POST /api/documents/ask
```

Request body:

```json
{
  "question": "What is this document about?"
}
```

Example response:

```json
{
  "answer": "The document is about ...",
  "sources": [
    {
      "content": "Source chunk text...",
      "source": "uploaded_file.pdf",
      "page": 1
    }
  ]
}
```

## How It Works

When a PDF is uploaded, the backend saves it in the `uploads` folder. The document is loaded with PyPDF, cleaned, and split into smaller text chunks.

Each chunk is converted into embeddings using a HuggingFace sentence transformer model. These embeddings are stored in ChromaDB.

When the user asks a question, the system searches the vector store for the most relevant chunks. The retrieved chunks are passed to the Groq LLM, and the answer is generated only from the document context.

## Generated Folders

The backend creates these folders automatically:

```text
backend/uploads/
backend/chroma_db/
```

`uploads/` stores uploaded PDF files.

`chroma_db/` stores the local ChromaDB vector database.

These folders should not be pushed to GitHub because they contain generated data.

## Resetting the Document Store

If you want to clear uploaded documents and indexed data, stop the backend and delete these folders:

```text
backend/uploads/
backend/chroma_db/
```

They will be created again when the backend starts.

## Docker Setup

You can also run the backend with Docker.

Go to the backend folder:

```bash
cd backend
```

Build the image:

```bash
docker build -t document-qa-chatbot .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 document-qa-chatbot
```

The backend will be available at:

```text
http://localhost:8000
```

## Important Files

### `document_processor.py`

Loads PDF files, cleans the extracted text, and splits the document into chunks.

### `vector_store.py`

Creates embeddings and stores document chunks in ChromaDB.

### `rag_service.py`

Builds the retrieval chain and generates answers using Groq LLM.

### `routes.py`

Defines the upload, health, and question-answering API endpoints.

### `script.js`

Connects the frontend upload form and question form to the backend API.

## Common Issues

### Backend is not starting

Make sure you are inside the `backend` folder and the virtual environment is activated.

Then install dependencies again:

```bash
pip install -r requirements.txt
```

### Groq API key error

Check that your `.env` file exists inside the `backend` folder and contains a valid `GROQ_API_KEY`.

### PDF upload fails

Make sure the selected file is a PDF. The backend only accepts files ending with `.pdf`.

### First request is slow

The embedding model may be downloading for the first time. Wait for the download to complete and try again.

### Frontend cannot connect to backend

Make sure the backend is running at:

```text
http://127.0.0.1:8000
```

Also check these URLs in `frontend/script.js`:

```javascript
const UPLOAD_URL = "http://127.0.0.1:8000/api/documents/upload";
const ASK_URL = "http://127.0.0.1:8000/api/documents/ask";
```

### CORS error in browser console

Make sure the frontend URL is included in `ALLOWED_ORIGINS` inside `.env`.

Example:

```env
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000
```

### Answer is not found in the document

The assistant is designed to answer from uploaded document context only. If the information is not present in the PDF, it should say that the information was not found.

## Notes

- This project only supports PDF uploads.
- Uploaded files and vector database files are generated locally.
- The system uses local ChromaDB storage.
- Keep your `.env` file private.
- For production use, add authentication, file size limits, persistent storage, and better document management.
