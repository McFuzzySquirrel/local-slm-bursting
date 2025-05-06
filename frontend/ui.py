import streamlit as st
import requests
import os
import json
import time
from datetime import datetime

# Load config
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import Settings

# Configuration
settings = Settings()
API_URL = f"http://{settings.api_host}:{settings.api_port}"

# Page configuration
st.set_page_config(
    page_title="Hybrid AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# App title and description
st.title("Hybrid AI Assistant")
st.markdown("**On-Device SLM with Azure LLM Fallback**")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This assistant uses:
        - 🖥️ **Local Model**: For simple queries
        - ☁️ **Azure GPT-4**: For complex queries
        - 📑 **Vector Search**: For document context
        """
    )
    
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            # Save the uploaded file temporarily
            file_path = os.path.join("temp", uploaded_file.name)
            os.makedirs("temp", exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Send the file to the API
            try:
                with open(file_path, "rb") as f:
                    response = requests.post(
                        f"{API_URL}/api/upload",
                        files={"file": (uploaded_file.name, f, "application/pdf")}
                    )
                    
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Document processed into {result['chunks']} chunks!")
                else:
                    st.error(f"Error: {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
            
            finally:
                # Clean up
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    st.header("Documents")
    if st.button("Refresh Document List"):
        with st.spinner("Loading documents..."):
            try:
                response = requests.get(f"{API_URL}/api/documents")
                if response.status_code == 200:
                    docs = response.json()["documents"]
                    if docs:
                        for doc in docs:
                            doc_name = doc["filename"]
                            doc_size = doc["size_kb"]
                            st.text(f"📄 {doc_name} ({doc_size} KB)")
                    else:
                        st.info("No documents uploaded yet")
                else:
                    st.error("Failed to load documents")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.header("Settings")
    force_route = st.radio(
        "Force routing to:",
        options=["Auto", "Local Model", "Azure GPT"],
        index=0
    )

# Main content area
query = st.text_area("Ask a question about your documents:", height=100)

col1, col2 = st.columns([1, 5])
with col1:
    submit_button = st.button("Submit", use_container_width=True)
with col2:
    # Empty space for alignment
    pass

# Process query when button is clicked
if submit_button and query:
    # Prepare request data
    request_data = {"query": query}
    
    # Add force routing if selected
    if force_route == "Local Model":
        request_data["force_route"] = "local"
    elif force_route == "Azure GPT":
        request_data["force_route"] = "azure"
    
    # Send request to API
    with st.spinner("Generating answer..."):
        try:
            response = requests.post(
                f"{API_URL}/api/query",
                json=request_data
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display source info
                source = result.get("source", "unknown")
                source_icon = "🖥️" if source == "local" else "☁️" if source == "azure" else "❓"
                source_name = "Local Model" if source == "local" else "Azure GPT" if source == "azure" else "Unknown"
                
                st.info(f"Answer generated using {source_icon} **{source_name}** in {result.get('query_time', 0):.2f} seconds")
                
                # Display the response
                st.markdown("### Answer")
                st.markdown(result.get("response", "No response generated"))
                
                # Display metadata in expander
                with st.expander("Response Details"):
                    st.json(result)
                    
            else:
                st.error(f"Error: {response.text}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Bottom disclaimer
st.markdown("---")
st.caption("© 2023 Hybrid AI Assistant | This is a demo application running a hybrid AI system")
