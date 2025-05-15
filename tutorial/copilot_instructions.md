# GitHub Copilot Instructions for Local SLM Bursting Application

## Project Overview
We're building a Local Small Language Model (SLM) Bursting application that allows users to run local language models and "burst" to cloud models when needed. The application consists of a FastAPI backend and a Streamlit frontend.

## Architecture Instructions
- Create a FastAPI backend for model inference and management
- Create a Streamlit frontend for user interaction
- Implement a virtual environment setup for Python dependencies
- Design batch scripts for easy startup on Windows systems
- Support local models (GGUF format) with configurable parameters
- Implement "bursting" capability to cloud models when local models can't handle requests

## File Structure Instructions
- Create a modular project structure with separate backend and frontend components
- Implement a `run_app.bat` for initial setup and running both components
- Create separate batch files for running individual components
- Use a `.env` file for configuration (with `.env.example` as a template)
- Create necessary directories for models, uploads, and logs

## Environment Setup Instructions
- Use Python 3.8+ with venv for environment isolation
- Create requirements.txt with all necessary dependencies
- Implement automatic checking and creation of required directories
- Add validation for Python installation and dependency installation

## Backend API Instructions
- Create a FastAPI application with proper error handling
- Implement endpoints for:
  - Text completion/generation
  - Model listing and selection
  - Configuration management
  - Health checks
- Use async patterns for efficient handling of requests
- Implement proper logging and error handling

## Frontend UI Instructions
- Create a Streamlit application with clean, intuitive UI
- Implement:
  - Model selection dropdown
  - Text input area with generation options
  - Settings configuration panel
  - Response display area
- Add proper error handling for API connectivity issues

## Deployment Instructions
- Create batch files for easy deployment on Windows
- Include proper waiting mechanisms between backend and frontend startup
- Add clear instructions for users to run the application
- Include validation checks before starting components

## Testing Instructions
- Test API endpoints with different model configurations
- Validate frontend UI behavior with various inputs
- Test error handling and recovery mechanisms
- Verify environment setup works correctly on fresh installations

## Note to Copilot
Focus on creating a robust, user-friendly application that can be easily set up and run on Windows machines using batch files. Ensure proper error handling and user guidance throughout the application.
