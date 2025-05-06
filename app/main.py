from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import shutil
from typing import List, Optional, Dict, Any
import time
from pydantic import BaseModel
from pathlib import Path

from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from .local_llm import LocalLLM
from .azure_llm import AzureLLM
from .query_router import QueryRouter

# Load config
from config.settings import Settings

# Initialize app
app = FastAPI(title="Hybrid AI Assistant")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for requests and responses
class QueryRequest(BaseModel):
    query: str
    force_route: Optional[str] = None  # 'local' or 'azure' if we want to force route

class QueryResponse(BaseModel):
    response: str
    source: str  # 'local' or 'azure'
    query_time: float
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks: int

# Initialize components
settings = Settings()

document_processor = DocumentProcessor(
    chunk_size=settings.chunk_size, 
    chunk_overlap=settings.chunk_overlap
)

vector_store = VectorStore(
    persist_directory=settings.vector_store_path
)

local_llm = LocalLLM(
    model_path=settings.local_model_path,
    context_size=settings.context_size,
    max_tokens=settings.max_tokens,
    temperature=settings.temperature,
    verbose=settings.verbose
)

azure_llm = AzureLLM(
    api_key=settings.azure_api_key,
    endpoint=settings.azure_endpoint,
    deployment_name=settings.azure_deployment,
    max_tokens=settings.azure_max_tokens,
    temperature=settings.azure_temperature,
    verbose=settings.verbose
)

query_router = QueryRouter(
    word_limit=settings.word_limit,
    complexity_keywords=settings.complexity_keywords,
    verbose=settings.verbose
)

# Create upload directory if it doesn't exist
os.makedirs(settings.upload_dir, exist_ok=True)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Hybrid AI Assistant API is running"}


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    start_time = time.time()
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save the uploaded file temporarily
    temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)
    with open(temp_file_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
    
    try:
        # Process the document
        document_chunks = document_processor.process_pdf(temp_file_path)
        
        # Store the document chunks in vector store
        vector_store.add_documents(document_chunks)
        
        # Move file to upload directory for persistence
        upload_path = os.path.join(settings.upload_dir, file.filename)
        shutil.move(temp_file_path, upload_path)
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            chunks=len(document_chunks)
        )
    
    except Exception as e:
        # Clean up temp file in case of error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a query using appropriate model"""
    start_time = time.time()
    
    # Search for relevant context
    context_docs = vector_store.similarity_search(request.query, top_k=3)
    
    # Route the query or use forced route
    if request.force_route:
        route_target = request.force_route
        is_simple = (route_target == "local")
        reason = f"Forced route to {route_target}"
    else:
        routing_decision = query_router.route_query(request.query, context_docs)
        route_target = routing_decision["route_to"]
        is_simple = routing_decision["is_simple"]
        reason = routing_decision["reason"]
        confidence = routing_decision["confidence"]
    
    # Process with appropriate model
    if route_target == "local":
        result = local_llm.generate_with_context(request.query, context_docs)
    else:  # azure
        result = azure_llm.generate_with_context(request.query, context_docs)
    
    # Add metadata
    result["query_time"] = time.time() - start_time
    result["metadata"] = {
        "is_simple_query": is_simple,
        "routing_reason": reason,
        "context_docs": len(context_docs),
    }
    
    if "confidence" not in result and "confidence" in locals():
        result["confidence"] = confidence
    
    return QueryResponse(**result)


@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents"""
    documents = []
    for filename in os.listdir(settings.upload_dir):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(settings.upload_dir, filename)
            documents.append({
                "filename": filename,
                "size_kb": round(os.path.getsize(file_path) / 1024, 1),
                "upload_time": os.path.getctime(file_path)
            })
    
    return {"documents": documents}


@app.delete("/api/documents/{filename}")
async def delete_document(filename: str, background_tasks: BackgroundTasks):
    """Delete a document and its embeddings"""
    file_path = os.path.join(settings.upload_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete file
        os.remove(file_path)
        
        # Note: In a real implementation, we would also remove
        # the associated embeddings from the vector store.
        # This would require tracking document-chunk relationships.
        
        return {"status": "success", "message": f"Document {filename} deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
