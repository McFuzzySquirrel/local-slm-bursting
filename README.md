# Local SLM Bursting Application

A hybrid solution that runs Small Language Models (SLMs) locally with the ability to "burst" to more powerful cloud models when necessary, providing cost-effective, private, and always-available language model capabilities.

## Features

- **Local Model Inference**: Run text generation/completion with locally-stored GGUF models
- **Burst Capability**: Seamlessly switch to cloud models when needed based on configurable criteria
- **Easy Setup**: Simple batch scripts for Windows environments
- **Streamlit UI**: Intuitive interface for interacting with models
- **FastAPI Backend**: Efficient API for model management and inference

## Getting Started

### Prerequisites

- Python 3.8+ installed and in PATH
- Windows operating system
- Internet connection for initial setup and cloud model bursting
- 4GB+ RAM (8GB+ recommended for larger models)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/local-slm-bursting.git
   cd local-slm-bursting
   ```

2. Run the setup script:
   ```
   run_app.bat
   ```
   
   This script will:
   - Create a virtual environment (.venv)
   - Install required dependencies
   - Create necessary directories
   - Set up configuration files
   - Start both backend and frontend

3. Download a GGUF model:
   - Visit [Hugging Face](https://huggingface.co/models?other=gguf)
   - Download models like TinyLlama, Phi-2, or Mistral-7B
   - Place the .gguf file in the `models/` directory

### Quick Start (After Initial Setup)

For subsequent runs, use:
```
quick_start.bat
```

This script uses the existing virtual environment to start the application.

## Usage

1. Select a model from the dropdown in the UI
2. Adjust generation parameters if needed
3. Enter your prompt text
4. Click "Generate" to get a response
5. The application will use the local model by default and burst to cloud models when needed

## Architecture

The Local SLM Bursting application follows a client-server architecture with two main components:

### Backend API (FastAPI)

- **Model Management**: Dynamically loads and manages local GGUF models using llama.cpp
- **Inference Engine**: Handles text generation requests with configurable parameters
- **Burst Controller**: Intelligently decides when to use local models vs. cloud models based on:
  - Request complexity
  - Local model capabilities
  - Response quality requirements
  - System resource availability
- **Configuration Service**: Manages application settings and model parameters
- **API Endpoints**: RESTful endpoints for model interaction and system management

### Frontend UI (Streamlit)

- **User Interface**: Intuitive web interface for interacting with models
- **Request Handler**: Formats and sends requests to the backend API
- **Response Renderer**: Displays generated text with proper formatting
- **Settings Manager**: UI controls for adjusting model and system parameters
- **Monitoring Panel**: Displays system status and current model information

### Data Flow

1. User inputs prompt and parameters through the Streamlit UI
2. Request is sent to the FastAPI backend
3. Backend determines whether to use local or cloud model
4. Request is processed by the chosen model
5. Response is returned to the frontend
6. Generated text is displayed to the user

### Bursting Mechanism

The application uses these criteria to decide when to "burst" to cloud models:

- **Token Threshold**: When input/output exceeds local model capacity
- **Complexity Detection**: When prompt requires capabilities beyond local model
- **Quality Requirements**: When higher quality is explicitly requested
- **Resource Monitoring**: When local system resources are constrained

This hybrid approach provides the benefits of both local processing (privacy, availability, lower cost) and cloud models (higher capability, better quality for complex tasks) in a seamless experience.

## Project Structure

```
local-slm-bursting/
├── backend/               # FastAPI backend
│   ├── api/               # API routes
│   ├── models/            # Model management 
│   └── utils/             # Utility functions
├── frontend/              # Streamlit frontend
├── models/                # GGUF model storage
├── data/                  # Data storage
│   └── uploads/           # User uploads
├── logs/                  # Application logs
├── .env.example           # Example configuration
├── requirements.txt       # Python dependencies
├── run_app.bat            # Main startup script
├── run_local_api.bat      # Backend starter
├── run_streamlit.bat      # Frontend starter
└── quick_start.bat        # Quickstart script
```

## Configuration

Edit the `.env` file to configure:
- API endpoint settings
- Default model and parameters
- Cloud model API keys (for bursting)
- Logging settings

## Development

This project is built using GitHub Copilot. Check out these resources:

- [Copilot Instructions](./copilot_instructions.md) - Guidelines for using Copilot with this project
- [Product Requirements Document](./product_requirements_document.md) - Detailed project specifications
- [Copilot Agent Tutorial](./copilot_agent_tutorial.md) - Tutorial for building the project with Copilot

### Running Individual Components

- Start only the backend: `run_local_api.bat`
- Start only the frontend: `run_streamlit.bat`

## Troubleshooting

### Common Issues

- **"Failed to load model"**: Ensure a GGUF model is placed in the models/ directory
- **Backend connection error**: Check if the backend API is running on the configured port
- **Memory errors**: Try a smaller model or adjust memory settings in the .env file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Llama.cpp](https://github.com/ggerganov/llama.cpp) for local model inference
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the frontend UI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
