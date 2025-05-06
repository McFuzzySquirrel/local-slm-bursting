# Hybrid AI Assistant – Project Requirements

## Project Title
**Hybrid AI Assistant** – On-Device SLM with Azure LLM Fallback

## Goal
Build a hybrid AI assistant that runs a lightweight language model (SLM) on-device to handle simple questions and bursts to Azure-hosted GPT-4-Turbo for complex queries. This assistant should allow document upload, local indexing, and interactive querying via a web interface.

---

## High-Level Architecture

### Local Components
- Python backend using FastAPI.
- Local small language model (Phi-2 or TinyLlama via llama.cpp).
- Vector database (ChromaDB or FAISS) for local document embedding and retrieval.
- SentenceTransformer for lightweight embeddings.
- Document ingestion from PDF using PyPDF2.
- Streamlit frontend interface served locally.

### Cloud Components
- Azure AI Studio or Azure OpenAI deployment (GPT-4-Turbo).
- Secure API key authentication.
- Optional Azure Blob Storage for file archival.

---

## Core Functional Requirements

### 1. Document Upload & Processing
- Accept PDF uploads via frontend.
- Extract and chunk text content from PDFs.
- Embed chunks using a sentence transformer.
- Store embeddings in a local vector store.

### 2. Query Interface
- Text input field for user questions.
- Process query by:
  - Determining if it's "simple" (e.g., short or fact-based).
  - Using the local model if simple.
  - Escalating to Azure GPT-4 if complex.

### 3. Routing Logic
- A Python function `is_simple(query: str)` determines complexity:
  - Short (≤20 words)
  - No logical operators or comparison keywords like "compare", "contrast", "relate"
- Route to `query_local()` or `query_azure()` based on outcome.

### 4. Answer Rendering
- Display:
  - Final response
  - Source (local or Azure)
  - Optional confidence or explanation tag

### 5. Local LLM Inference
- Load GGUF model (4-bit or 5-bit) using `llama-cpp-python`.
- Process prompt text and return simple completions.

### 6. Azure LLM Inference
- Secure API call to Azure OpenAI deployment.
- Handle error fallback gracefully.
- Use OpenAI `chat/completions` endpoint format.

---

## Non-Functional Requirements
- Runs on Windows (Surface device).
- Should function offline (local mode).
- Modular and maintainable Python code structure.
- Easily extendable to support audio/voice in the future.

---

## File/Folder Structure

```
hybrid_ai_assistant/
│
├── app/
│   ├── main.py
│   ├── local_llm.py
│   ├── azure_llm.py
│   ├── query_router.py
│   ├── document_processor.py
│   └── vector_store.py
│
├── frontend/
│   └── ui.py
├── config/
│   └── settings.py
├── models/
│   └── [downloaded_gguf_model]
├── data/
│   └── sample.pdf
├── requirements.txt
├── run_local_api.bat
├── README.md
```

---

## Suggested Tasks for GitHub Copilot Agent

### Task 1: Set up virtual environment and dependencies
- Create `requirements.txt`
- Install FastAPI, uvicorn, llama-cpp-python, sentence-transformers, chromadb, PyPDF2, streamlit, requests

### Task 2: Scaffold application structure
- Generate directory tree above with `__init__.py` files where necessary

### Task 3: Implement document ingestion
- `document_processor.py` reads PDF and returns chunks of text.

### Task 4: Implement vector indexing
- `vector_store.py` stores document chunks and supports similarity search.

### Task 5: Implement local model wrapper
- `local_llm.py` loads GGUF model and generates completions.

### Task 6: Implement Azure GPT wrapper
- `azure_llm.py` sends chat prompt to Azure and returns structured response.

### Task 7: Implement query router
- `query_router.py` decides where to send the query.

### Task 8: Build FastAPI endpoint
- `main.py` serves a `/query` endpoint that receives user input.

### Task 9: Build Streamlit frontend
- `ui.py` provides a basic interface for input and displays source and result.

### Task 10: Document and test
- Add example PDF and demo prompts.
- Ensure clear README instructions.
