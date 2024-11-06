# FastAPI RAG Server with ChromaDB

## Overview

This project implements a lightweight FastAPI server for Retrieval-Augmented Generation (RAG). The server allows for the ingestion and querying of documents in various formats (PDF, DOC, DOCX, TXT) using ChromaDB's persistent client as the vector store. It leverages the `sentence-transformers/all-MiniLM-L6-v2` model from Hugging Face to generate text embeddings on the CPU.

## Features

- **Document Ingestion**: Upload and store documents in a vector database with embedded content for efficient querying.
- **Semantic Search**: Query documents using natural language and retrieve the most relevant results.
- **Asynchronous Operations**: Uses efficient non-blocking API endpoints for better performance.
- **Supported File Formats**: PDF, DOC, DOCX, and TXT.

## Installation

### Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)

### Steps to Set Up the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/fastapi-rag-server.git
   cd fastapi-rag-server
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- The `--reload` flag enables auto-reloading for code changes (useful during development).

## API Endpoints

### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Returns a welcome message.
- **Example Response**:
  ```json
  {
    "message": "Welcome to the FastAPI RAG Server!"
  }
  ```

### 2. Ingest Document
- **URL**: `POST /ingest`
- **Description**: Uploads and ingests a document into the vector store.
- **Request Body**: `form-data` with a key `file` containing the document (PDF, DOC, DOCX, TXT).
- **Example Request**:
  - **Using Postman**: 
    - Select `POST` method, set the URL to `http://localhost:8000/ingest`.
    - Go to the "Body" tab, choose `form-data`, add a key `file`, and select a file to upload.
- **Example Response**:
  ```json
  {
    "status": "Document ingested successfully"
  }
  ```

### 3. Query Documents
- **URL**: `GET /query`
- **Description**: Queries the ingested documents for the most relevant matches.
- **Query Parameters**:
  - `query` (string): The search term or question.
  - `top_k` (integer, optional): The number of top results to return (default is 5).
- **Example Request**:
  - **Using Postman**: 
    - Select `GET` method, set the URL to `http://localhost:8000/query`.
    - Add query parameters `query` and `top_k` in the "Params" section.
- **Example Response**:
  ```json
  {
    "results": [
      {
        "documents": ["Document text here"],
        "distances": [0.12345]
      }
    ]
  }
  ```

## Testing with Postman

### 1. Ingest a Document
- **Method**: POST
- **URL**: `http://localhost:8000/ingest`
- **Body**: 
  - Select `form-data`.
  - Key: `file`, Value: [Select the file you want to upload]
- Click **Send** to upload and ingest the document.

### 2. Query Documents
- **Method**: GET
- **URL**: `http://localhost:8000/query`
- **Params**:
  - `query`: Your search term (e.g., "machine learning").
  - `top_k`: The number of results to return (e.g., 5).
- Click **Send** to retrieve the results.

## Project Structure

```
fastapi-rag-server/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

- **main.py**: The main FastAPI application code.
- **requirements.txt**: List of dependencies needed to run the project.
- **README.md**: Documentation for setting up and using the project.
- **.gitignore**: Specifies files and directories to be ignored by Git.

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for running FastAPI.
- **ChromaDB**: Vector database for storing and querying document embeddings.
- **SentenceTransformers**: Library for embedding text using pre-trained models.
- **PyPDF2**: Utility for extracting text from PDF files.
- **python-docx**: Library for extracting text from DOCX files.
- **Mammoth**: Tool for converting DOC files to plain text.
- **Aiofiles**: Library for asynchronous file operations.

## Notes

- Ensure you have sufficient permissions to create and manage files in the `temp_files/` and `db_persist/` directories.
- The `--reload` flag in the Uvicorn command is only recommended for development. Use `uvicorn main:app` without `--reload` in production.

## Future Improvements

- Add authentication for API endpoints.
- Implement more robust error handling.
- Optimize the embedding generation for large documents by chunking text.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [SentenceTransformers](https://www.sbert.net/) for the embedding models.
- [ChromaDB](https://docs.trychroma.com/) for the vector database.
- Community and resources for supporting the development of this project.

### Thank You!

