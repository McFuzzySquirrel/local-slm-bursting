#!/bin/bash

echo "===== Local SLM Bursting Application Launcher ====="
echo "This script will start both the backend API and the frontend UI."
echo

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found."
    echo "Creating .env from .env.example..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your configuration."
        echo "Press Enter to edit the .env file or Ctrl+C to exit."
        read
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo "No suitable editor found. Please edit .env file manually."
        fi
    else
        echo "ERROR: .env.example file not found."
        echo "Please create a .env file with required configuration."
        exit 1
    fi
fi

# Create directories if they don't exist
mkdir -p data/uploads
mkdir -p models
mkdir -p logs

# Check for GGUF model
if [ -z "$(ls -A models/*.gguf 2>/dev/null)" ]; then
    echo "WARNING: No GGUF model found in the models directory."
    echo "Please download a model from Hugging Face and place it in the models folder."
    echo "Example models: Phi-2, TinyLlama, Mistral-7B"
    echo
fi

# Start the backend API in a new terminal
echo "Starting backend API server..."

# Try different terminal emulators based on availability
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "python3 -m uvicorn app.main:app --reload --host localhost --port 8000; exec bash"
elif command -v xterm &> /dev/null; then
    xterm -e "python3 -m uvicorn app.main:app --reload --host localhost --port 8000; exec bash" &
elif command -v konsole &> /dev/null; then
    konsole --new-tab -e "python3 -m uvicorn app.main:app --reload --host localhost --port 8000; exec bash" &
elif command -v terminal &> /dev/null; then  # macOS
    terminal -e "python3 -m uvicorn app.main:app --reload --host localhost --port 8000" &
else
    echo "No suitable terminal emulator found. Starting backend in background..."
    python3 -m uvicorn app.main:app --reload --host localhost --port 8000 > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
fi

# Wait for the backend to initialize
echo "Waiting for backend to initialize (5 seconds)..."
sleep 5

# Start the frontend
echo "Starting Streamlit frontend..."
echo
echo "NOTE: When finished, close both terminal windows to shut down the application."
echo "If running in background mode, use 'kill $BACKEND_PID' to stop the backend."
echo

# Run the Streamlit app
streamlit run frontend/ui.py

# If we're running the backend in the background, clean up when the frontend exits
if [ -n "$BACKEND_PID" ]; then
    echo "Shutting down backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID
fi
