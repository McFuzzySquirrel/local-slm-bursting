# GitHub Copilot Agent Mode Tutorial - Building Local SLM Bursting Application

This tutorial shows how to use GitHub Copilot in agent mode to build the Local SLM Bursting application from scratch using the provided PRD and instructions files.

## Setting Up Copilot Agent Mode

1. In VS Code, ensure you have the latest GitHub Copilot extension installed
2. Open the command palette (Ctrl+Shift+P or Cmd+Shift+P)
3. Type and select "GitHub Copilot: Start Agent Chat"
4. When the chat panel opens, you're ready to begin

## Example Interactions

Here are step-by-step examples of how to interact with Copilot agent to build this project:

### Step 1: Project Initialization

**You:**
```
I want to build a Local SLM Bursting application using the requirements in the product_requirements_document.md and following the guidelines in copilot_instructions.md. Let's start by setting up the project structure.
```

**Copilot:**
*Copilot will analyze the PRD and instructions, then suggest creating the project structure:*
```
Based on the PRD and instructions, I'll help you set up the project structure for the Local SLM Bursting application. Let's start by creating the main directories and files:

1. First, let's create the main project folder structure:
   - backend/ (for FastAPI backend)
   - frontend/ (for Streamlit frontend)
   - models/ (for storing GGUF models)
   - data/uploads/ (for user uploads)
   - logs/ (for application logs)

2. Then we'll create key configuration files:
   - requirements.txt
   - .env.example
   
3. Finally, we'll create the batch scripts:
   - run_app.bat
   - run_local_api.bat
   - run_streamlit.bat
   - quick_start.bat

Would you like me to generate these directories and initial files for you?
```

**You:**
```
Yes, please generate the directory structure and initial files.
```

### Step 2: Creating the Backend

**You:**
```
Now let's implement the FastAPI backend. It should be able to load local GGUF models, provide inference endpoints, and have the burst capability as described in the PRD.
```

**Copilot:**
*Copilot will analyze requirements and generate backend code:*
```
I'll create the FastAPI backend components based on the requirements. Here's what we'll implement:

1. First, let's create the main FastAPI application structure:
   - backend/main.py - Main application entry point
   - backend/api/routes.py - API endpoints
   - backend/models/model_manager.py - Model loading and management
   - backend/utils/config.py - Configuration handling

2. We'll implement these key features:
   - Local model loading using llama.cpp
   - Text generation endpoint
   - Model selection and configuration
   - Burst capability to cloud models

Let me generate these files for you. I'll start with backend/main.py...
```

### Step 3: Developing the Frontend

**You:**
```
Great! Now let's create the Streamlit frontend that will connect to our backend API. It should have all the UI components described in section 3.2 of the PRD.
```

**Copilot:**
*Copilot will generate the Streamlit frontend code:*
```
I'll create the Streamlit frontend with all the UI components described in the PRD. Here's what we'll implement:

1. Main Streamlit application (frontend/app.py) with:
   - Model selection dropdown
   - Text input area with parameters
   - Output display with formatting
   - Settings panel for configuration
   - Monitoring panel showing current model status

2. API connection utilities (frontend/utils/api.py) to communicate with the backend

Let me generate these files for you...
```

### Step 4: Creating Batch Scripts

**You:**
```
Let's create the batch scripts for running the application on Windows. We need run_app.bat as the main entry point, plus the individual scripts for the API and Streamlit.
```

**Copilot:**
*Copilot will generate batch scripts:*
```
I'll create the batch scripts for running the application on Windows. According to the requirements, we need:

1. run_app.bat - Main script that:
   - Checks for Python installation
   - Creates/activates virtual environment
   - Installs dependencies
   - Sets up configuration
   - Creates necessary directories
   - Starts backend and frontend

2. run_local_api.bat - Script to start just the backend API
3. run_streamlit.bat - Script to start just the Streamlit frontend
4. quick_start.bat - Script for quick startup of existing installation

Let me generate these scripts for you...
```

### Step 5: Creating Environment Files

**You:**
```
Let's create the requirements.txt file with all necessary dependencies, and a .env.example file with configuration parameters.
```

**Copilot:**
*Copilot will generate the dependency and configuration files:*
```
I'll create the requirements.txt file with all necessary dependencies for the application and a .env.example file with all required configuration parameters.

For requirements.txt, we'll include:
- fastapi - For the backend API
- uvicorn - For serving the API
- streamlit - For the frontend
- python-dotenv - For environment configuration
- llama-cpp-python - For running local GGUF models
- requests - For API communication
- pydantic - For data validation
- etc.

For .env.example, we'll include:
- API configuration (port, host)
- Model settings (default model, parameters)
- Cloud API keys (for bursting capability)
- Logging configuration

Let me generate these files for you...
```

## Testing and Debugging

**You:**
```
The application loads but I'm getting an error when trying to load a model. The error says "Failed to load model: No such file or directory". How can I fix this?
```

**Copilot:**
*Copilot will help debug issues:*
```
This error occurs because the application is trying to load a model that doesn't exist in the models/ directory. Here are steps to fix this:

1. First, check if you have any GGUF models in the models/ directory.
2. If not, you need to download a compatible model. You can download models from Hugging Face.
3. For example, download TinyLlama, Phi-2, or Mistral-7B GGUF model.
4. Place the downloaded .gguf file in the models/ directory.
5. Make sure the model path in the .env file matches the exact filename of your downloaded model.

Would you like me to modify the code to provide a better error message or add a fallback model option?
```

## Common Commands for Building This Project

Here are useful commands to give to Copilot agent while building this project:

1. **Project structure creation:**
   ```
   Create the directory structure according to the PRD section 5.1
   ```

2. **Backend implementation:**
   ```
   Create the FastAPI backend with model loading, inference endpoints, and configuration management
   ```

3. **Frontend implementation:**
   ```
   Create the Streamlit frontend with all UI components from section 3.2 of the PRD
   ```

4. **Batch script creation:**
   ```
   Create Windows batch scripts for application startup as described in section 5.2
   ```

5. **Adding burst functionality:**
   ```
   Implement the burst controller that switches between local and cloud models based on configurable criteria
   ```

6. **Testing and debugging:**
   ```
   Generate test cases for the backend API endpoints
   ```

7. **Documentation:**
   ```
   Create user documentation explaining how to set up and use the application
   ```

Remember that you can always refer Copilot back to specific sections of the PRD by mentioning them in your prompts.

## Best Practices

1. **Start with project structure**: Have Copilot set up directories and basic files first
2. **Build incrementally**: Focus on one component at a time (backend, then frontend)
3. **Test frequently**: Ask Copilot to generate test code or debug issues
4. **Reference the PRD**: Point to specific sections when making requests
5. **Iterate on code**: Ask Copilot to improve or refactor code as needed

By following this approach, you can efficiently collaborate with GitHub Copilot to build the complete Local SLM Bursting application as specified in the requirements document.
