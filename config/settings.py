import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import validator  # Import validator

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    api_host: str = "localhost"
    api_port: int = 8000
    
    # Upload settings
    upload_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
    
    # Document processing settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Vector store settings
    vector_store_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faiss_index")
    
    # Chroma DB settings
    chroma_db_impl: str = "duckdb+parquet"  # Default value
    chroma_db_dir: str = "data/chroma_db"  # Default value
    persist_directory: str = "data/chroma_db"  # Default value
    
    # Local LLM settings
    local_model_path: str = os.getenv("LOCAL_MODEL_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.gguf"))
    context_size: int = 2048
    max_tokens: int = 512
    temperature: float = 0.7
    
    # Azure LLM settings
    azure_api_key: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    azure_endpoint: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    azure_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-06")
    azure_max_tokens: int = 1024
    azure_temperature: float = 0.7
    
    # Additional OpenAI compatible settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_api_base: Optional[str] = os.getenv("OPENAI_API_BASE")
    openai_deployment_name: Optional[str] = os.getenv("OPENAI_DEPLOYMENT_NAME")
    openai_api_version: Optional[str] = os.getenv("OPENAI_API_VERSION")
    openai_api_type: Optional[str] = os.getenv("OPENAI_API_TYPE")
    
    # Query router settings
    word_limit: int = 20
    complexity_keywords: List[str] = [
        "compare", "contrast", "relate", "analyze", "evaluate", 
        "synthesize", "elaborate", "explain why", "versus", 
        "difference between", "similarities", "hypothesis"
    ]
    
    # General settings
    verbose: bool = False  # Default value

    @validator("verbose", pre=True)
    def parse_verbose(cls, value):
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields
