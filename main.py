# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import asyncio
import os
import aiofiles
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import docx
import mammoth
from fastapi.responses import FileResponse

app = FastAPI()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="db_persist")

# Initialize the embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')

# Get or create a collection
collection = chroma_client.get_or_create_collection(name="documents")

# Helper functions
async def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

async def parse_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

async def parse_doc(file_path):
    with open(file_path, "rb") as doc_file:
        result = await asyncio.to_thread(mammoth.convert_to_plain_text, doc_file)
    text = result.value
    return text

async def parse_txt(file_path):
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        text = await f.read()
    return text

async def get_embeddings(texts):
    embeddings = await asyncio.to_thread(
        embedding_model.encode, texts, show_progress_bar=False
    )
    return embeddings

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI RAG Server!"}

# Favicon endpoint (optional)
@app.get("/favicon.png", include_in_schema=False)
async def favicon():
    return FileResponse("D:\professionalProjects\rag_project\icon\favicon.png")

# API Endpoints
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    # Ensure temp_files directory exists
    os.makedirs("temp_files", exist_ok=True)
    file_location = f"temp_files/{file.filename}"
    
    # Save the uploaded file asynchronously
    async with aiofiles.open(file_location, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Parse the document based on file type
    if file.filename.endswith('.pdf'):
        text = await parse_pdf(file_location)
    elif file.filename.endswith('.docx'):
        text = await parse_docx(file_location)
    elif file.filename.endswith('.doc'):
        text = await parse_doc(file_location)
    elif file.filename.endswith('.txt'):
        text = await parse_txt(file_location)
    else:
        os.remove(file_location)
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Generate embeddings
    embeddings = await get_embeddings([text])
    
    # Ingest into ChromaDB
    collection.add(
        documents=[text],
        embeddings=embeddings,
        ids=[file.filename]  # Use unique IDs in production
    )
    
    # Clean up the temporary file
    os.remove(file_location)
    
    return {"status": "Document ingested successfully"}

@app.get("/query")
async def query_document(query: str = Query(...), top_k: int = 5):
    # Generate embedding for the query
    query_embedding = await get_embeddings([query])
    
    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=['documents', 'distances']
    )
    
    return {"results": results}
