# Exploring Ideas Through Code: One Experiment at a Time

## About These Projects

All of my projects exist for one main reason: **learning through experimentation**.  
Each repository is a result of me asking questions like:  
> “Is this possible?”  
> “I wonder if…?”  

Sometimes they’re attempts to solve real problems I’ve come across, other times they’re just me following curiosity down a rabbit hole.  
This is my **learning playground**, a space where I test ideas, try new things, and learn by doing.  

I share them here in case they help or inspire someone else.  
So expect some projects to be **messy**, others **well-structured** — all of them are honest reflections of learning in progress.  

Feel free to **use**, **modify**, or **build on** anything here. 

So here we go:

# Local SLM Bursting

A hybrid AI assistant that efficiently routes queries between a locally-running small language model (SLM) and Azure OpenAI, optimizing for performance, cost, and user experience.

## 🌟 Overview

This project demonstrates an intelligent approach to AI deployment by using a local-first strategy with cloud bursting. Simple queries are processed directly on your device using lightweight SLMs via llama.cpp, while complex questions are automatically routed to more powerful Azure OpenAI models.

## ✨ Key Features

- **Hybrid Inference Pipeline**: Smart routing between local and cloud models
- **Local-First Processing**: Reduce latency and API costs with on-device inference
- **Intelligent Bursting**: Seamlessly scale to Azure OpenAI for complex queries
- **Document Intelligence**: Upload, process and query PDF documents
- **Vector Search**: Use semantic search to find relevant information
- **Interactive UI**: Clean Streamlit web interface

## 🏗️ Architecture

The system uses a layered architecture with multiple components working together to provide efficient and intelligent query processing:

### Core Components

1. **Frontend Layer**: 
   - Streamlit web application that provides an intuitive user interface
   - Handles document uploads and displays interactive query responses
   - Offers manual controls for routing decisions when needed
   - Communicates with the backend API using HTTP requests

2. **API Layer**:
   - FastAPI backend providing RESTful endpoints for all operations
   - Coordinates the flow between components (document processing, vector search, model selection)
   - Implements efficient request handling with asynchronous processing
   - Manages error cases and provides consistent response formats

3. **Inference Layer**:
   - **Local Inference Engine**:
     - Uses llama.cpp to run small language models directly on the device
     - Optimized for efficiency with minimal resource requirements
     - Handles simple queries without requiring cloud connectivity
     - Provides fast response times for straightforward questions
   
   - **Cloud Inference Engine**:
     - Integrates with Azure OpenAI service for powerful reasoning capabilities
     - Follows Azure best practices for secure and reliable API communication
     - Delivers high-quality responses for complex questions
     - Scales to handle sophisticated reasoning tasks

4. **Document Intelligence Layer**:
   - Processes uploaded PDF documents into manageable text chunks
   - Generates vector embeddings using Sentence Transformers
   - Stores embeddings in a FAISS vector database for efficient similarity search
   - Retrieves relevant context based on semantic similarity to queries
   
5. **Query Router**:
   - Analyzes incoming queries to determine appropriate processing path
   - Uses heuristic rules based on query length, complexity keywords, and structure
   - Makes intelligent routing decisions to optimize for both performance and quality
   - Can be manually overridden when specific routing is desired

6. **Storage Layer**:
   - Maintains uploaded documents in an organized file structure
   - Persists vector indices for fast retrieval during query processing
   - Manages configuration settings through environment variables

### Data Flow

The system processes queries through the following steps:

1. User submits a question through the Streamlit UI
2. The API receives the query and passes it to the Query Router
3. Query Router analyzes complexity and determines the appropriate model
4. Vector Store searches for relevant document chunks based on semantic similarity
5. Selected model (local or Azure) processes the query with retrieved context
6. Response is formatted with metadata about the source and returned to the user
7. UI displays the answer along with information about which model generated it

This architecture balances efficiency and capability by processing simple queries locally while seamlessly bursting to cloud resources when needed for more complex questions.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure OpenAI service access
- GGUF format language model file

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/local-slm-bursting.git
   cd local-slm-bursting
   ```

2. **Set up a Python virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

5. **Update the .env file with your settings**
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
   - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
   - `AZURE_OPENAI_DEPLOYMENT`: Your model deployment name (default: "gpt-4o")
   - `LOCAL_MODEL_PATH`: Path to your downloaded GGUF model file

6. **Download a GGUF model**
   - Get models from [Hugging Face](https://huggingface.co/models?search=gguf)
   - Recommended options:
     - [Phi-2](https://huggingface.co/microsoft/phi-2)
     - [TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
     - [Mistral-7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)

## 🏁 Running the Application

### Option 1: Quick Start (Recommended)

Use the all-in-one launcher script to start both backend and frontend:

```bash
# Windows
run_app.bat

# Linux/Mac
chmod +x run_app.sh  # Make executable (first time only)
./run_app.sh
```

This script will:
- Check your environment setup
- Create necessary directories
- Verify model files
- Launch the backend API server
- Start the Streamlit frontend
- Open your browser automatically

### Option 2: Manual Start

If you prefer to start components individually:

1. **Start the API server**
   ```bash
   # Windows
   run_local_api.bat
   
   # Linux/Mac
   python -m uvicorn app.main:app --reload --host localhost --port 8000
   ```

2. **Launch the web interface** (in a separate terminal)
   ```bash
   # Windows
   run_streamlit.bat
   
   # Linux/Mac
   streamlit run frontend/ui.py
   ```

3. **Access the application** at [http://localhost:8501](http://localhost:8501)

## 💡 Usage Guide

### Document Processing
1. Upload PDF documents via the sidebar
2. Documents are automatically parsed and indexed using vector embeddings
3. Content becomes available for context-aware responses

### Question Answering
1. Type your question in the input box
2. The system determines query complexity using the QueryRouter:
   - Simple queries → Local SLM
   - Complex queries → Azure OpenAI
3. View responses with source attribution and processing details

### Manual Routing Control
Use the "Force routing" radio buttons in the sidebar to manually direct queries to either:
- Auto (default): Let the system decide
- Local Model: Force using local SLM
- Azure GPT: Force using Azure OpenAI

## 📦 Dependencies

The project uses the following key libraries:
- FastAPI and Uvicorn for the backend API
- llama-cpp-python for local inference
- Sentence Transformers and FAISS for vector search
- Streamlit for the web interface
- MarkItDown for PDF processing
- Azure libraries for Azure OpenAI integration

## 📂 Project Structure

```
local-slm-bursting/
│
├── app/                  # Backend API code
│   ├── main.py           # FastAPI entry point
│   ├── local_llm.py      # Local model interface
│   ├── azure_llm.py      # Azure OpenAI interface
│   ├── query_router.py   # Query complexity analyzer
│   ├── document_processor.py # PDF processing
│   └── vector_store.py   # Vector database interface
│
├── frontend/            # User interface
│   └── ui.py            # Streamlit web app
│
├── config/              # Configuration
│   └── settings.py      # Application settings
│
├── models/              # Local model storage
│   └── [model_file.gguf] # Your downloaded model
│
├── data/                # Data storage
│   ├── uploads/         # Uploaded documents
│   ├── faiss_index/     # Vector store index
│   └── chroma_db/       # ChromaDB storage
│
├── requirements.txt     # Python dependencies
├── run_local_api.bat    # Windows API startup script
├── run_streamlit.bat    # Windows UI startup script
├── run_app.bat          # Windows all-in-one launcher
├── run_app.sh           # Linux/Mac all-in-one launcher
└── README.md            # This documentation
```

## 🔧 Configuration Options

The application's behavior can be configured through the `settings.py` file:

- **API Settings**: Host and port configuration
- **Document Processing**: Chunk size and overlap for document splitting
- **Local LLM Settings**: Model path, context size, and generation parameters
- **Azure LLM Settings**: API keys, endpoints, and model configuration
- **Query Router Settings**: Word limits and complexity keywords for routing

## 🚨 Limitations

- Local model performance depends on your hardware capabilities
- PDF processing may struggle with complex document layouts
- Query routing is based on heuristics and may not always be optimal

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) for local inference
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/) for cloud AI
- [Sentence Transformers](https://www.sbert.net/) for text embeddings
- [FastAPI](https://fastapi.tiangolo.com/) for API development
- [Streamlit](https://streamlit.io/) for the web interface
