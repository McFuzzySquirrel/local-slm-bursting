# Hybrid AI Assistant

A hybrid AI assistant that runs a small language model (SLM) locally on your device for simple queries and bursts to Azure-hosted GPT-4-Turbo for complex questions.

## Features

- 🖥️ **Local Inference**: Process simple queries directly on your device
- ☁️ **Azure Fallback**: Route complex questions to Azure OpenAI
- 📄 **Document Processing**: Upload and index PDFs for context-aware answers
- 🔍 **Vector Search**: Retrieve relevant document segments for queries
- 🌐 **Web Interface**: Simple Streamlit UI for interaction

## Architecture

![Hybrid AI Architecture](https://mermaid.ink/img/pako:eNp1kU9PwzAMxb9K5DMIdeW2A5eJP1KlHYCJQ5rcxiVqkrhKUmCC774UNm1IwJf4vffsWH6DLEpBMeS6smVNVdUoQ28rcvdOtLQ13kkBXdglQsvS0WMRN6qgJzJlSy3BU8hMZd6pIVcfNYMP4ZbqnIr_fOxG8SyKHMrCdfkEvn7UOdt4OHLaDWCskiJUoMVRCz-tM2WkRtrjh260ZdUC9-TJF7QKv0CztARN7ftg_6GaAnm7Ic6Pz2PhYKTdB4ZrCJrRy7kPPjKtFlnz4WacvK7fpyGtxD2MSURkx97UW6PXkerImDu4rtzTw7_vdDXtNw9idlx_A5oBYjU?type=png)

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure OpenAI API access (for complex queries)
- A GGUF format language model file (Phi-2, TinyLlama, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hybrid-ai-assistant.git
   cd hybrid-ai-assistant
   ```

2. **Create and activate a virtual environment**
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

4. **Create environment file**
   ```bash
   copy .env.example .env
   ```

5. **Edit the `.env` file** to add your Azure OpenAI API key and model path

6. **Download a GGUF model file** and place it in the `models` directory
   - You can download models from [Hugging Face](https://huggingface.co/models?search=gguf)
   - Recommended: [Phi-2](https://huggingface.co/microsoft/phi-2) or [TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)

### Running the Application

1. **Start the backend API**
   ```bash
   run_local_api.bat
   # Or on Linux/Mac
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend in another terminal**
   ```bash
   run_streamlit.bat
   # Or on Linux/Mac
   streamlit run frontend/ui.py
   ```

3. **Open your browser** at http://localhost:8501

## Usage

1. **Upload Documents**
   - Use the sidebar to upload PDF documents
   - The system will process and index them automatically

2. **Ask Questions**
   - Type your question in the main text area
   - The system will automatically route to the appropriate model
   - Simple questions → Local model
   - Complex questions → Azure GPT

3. **View Results**
   - See which model answered your query
   - Review related document segments

## Project Structure

```
hybrid_ai_assistant/
│
├── app/                  # Backend API code
│   ├── main.py           # FastAPI entry point
│   ├── local_llm.py      # Local model wrapper
│   ├── azure_llm.py      # Azure OpenAI client
│   ├── query_router.py   # Query complexity analyzer
│   ├── document_processor.py # PDF processing
│   └── vector_store.py   # Vector database interface
│
├── frontend/            # Streamlit UI
│   └── ui.py            # Frontend interface
│
├── config/              # Configuration
│   └── settings.py      # App settings
│
├── models/              # Local model storage
│   └── [model_file.gguf] # Downloaded GGUF model
│
├── data/                # Data storage
│   └── uploads/         # Uploaded documents
│
├── requirements.txt     # Python dependencies
├── run_local_api.bat    # Windows batch to run API
├── run_streamlit.bat    # Windows batch to run UI
└── README.md            # This file
```

## Customization

- **Local Model**: Replace the model file in the `models` directory and update `.env`
- **Routing Logic**: Adjust the complexity detection in `query_router.py`
- **Document Processing**: Modify chunk size in `settings.py`

## License

MIT
