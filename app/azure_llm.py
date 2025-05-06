import os
import time
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# AzureLLM class: Responsible for communication with Azure OpenAI services.
# This class follows Azure best practices for API interaction, error handling,
# and secure credential management.
class AzureLLM:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        deployment_name: Optional[str] = None,
        api_version: str = "2023-05-15",  # Default to a stable API version
        max_tokens: int = 1024,           # Default response limit that balances detail and cost
        temperature: float = 0.7,         # Default temperature for balanced creativity/determinism
        verbose: bool = False             # Toggles logging for debugging
    ):
        """
        Initialize Azure OpenAI API client.
        
        Design decisions:
        - Uses environment variables as fallbacks for sensitive credentials
        - Supports multiple API versions for compatibility
        - Configurable generation parameters for different use cases
        - Verbose mode for development/debugging environments
        
        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            deployment_name: Azure OpenAI model deployment name
            api_version: Azure OpenAI API version
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            verbose: Whether to print verbose output
        """
        # Load environment variables if not provided
        # This follows Azure security best practice of not hardcoding credentials
        load_dotenv()
        
        # Priority: 1. Explicitly passed parameters, 2. Environment variables
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = api_version
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        
        # Validation: Ensure required credentials are available
        # Early validation prevents runtime errors during API calls
        if not self.api_key:
            raise ValueError("Azure OpenAI API key not provided and not found in environment variables")
        if not self.endpoint:
            raise ValueError("Azure OpenAI endpoint not provided and not found in environment variables")
        if not self.deployment_name:
            raise ValueError("Azure OpenAI deployment name not provided and not found in environment variables")
        
        # Ensure endpoint doesn't end with a slash
        # This prevents URL formatting issues when building request paths
        self.endpoint = self.endpoint.rstrip('/')
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a completion for a prompt using Azure OpenAI.
        
        Design decisions:
        - Supports system prompts for better control over model behavior
        - Measures generation time for monitoring/optimization
        - Robust error handling with informative messages
        - Returns structured response with metadata for downstream processing
        
        Args:
            prompt: User prompt
            system_prompt: Optional system message
            
        Returns:
            Response with generated text and metadata
        """
        # Track performance for monitoring and optimization
        start_time = time.time()
        
        # Set up request headers following Azure best practices
        # Content-Type ensures proper request parsing
        # api-key header is the recommended auth method for Azure OpenAI
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        # Construct messages array in OpenAI chat format
        # System message provides instructions to guide the model's behavior
        # User message contains the actual query content
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Construct Azure OpenAI API URL
        # Format: {endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        # Set up request parameters
        # max_tokens limits response size for cost control
        # temperature affects randomness/creativity (0=deterministic, 1=creative)
        request_data = {
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        
        # Optional debug logging
        if self.verbose:
            print(f"Calling Azure OpenAI API for prompt: {prompt[:50]}...")
        
        try:
            # Send request to Azure OpenAI with timeout for reliability
            # Using POST for chat completions API as per Azure docs
            response = requests.post(url, headers=headers, json=request_data, timeout=60)
            
            # Raise exception for HTTP errors (4xx, 5xx)
            response.raise_for_status()
            
            # Parse JSON response
            response_data = response.json()
            
            # Extract generated text from the response
            # The structure follows OpenAI's standard response format
            if "choices" in response_data and response_data["choices"]:
                generated_text = response_data["choices"][0]["message"]["content"].strip()
            else:
                generated_text = "No response generated."
                
            # Calculate total processing time
            generation_time = time.time() - start_time
            
            # Extract usage statistics for monitoring and cost management
            usage = response_data.get("usage", {})
            
            # Return structured response with metadata
            return {
                "response": generated_text,
                "source": "azure",
                "model": self.deployment_name,
                "generation_time": generation_time,
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
            
        except requests.exceptions.RequestException as e:
            # Handle request errors gracefully
            # Provides detailed error information without crashing the application
            error_message = f"Azure OpenAI API error: {str(e)}"
            if self.verbose:
                print(error_message)
            return {
                "response": f"Error: Failed to generate response from Azure OpenAI. {error_message}",
                "source": "error",
                "error": str(e),
                "generation_time": time.time() - start_time
            }
    
    def generate_with_context(self, prompt: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a completion with document context using RAG (Retrieval-Augmented Generation) pattern.
        
        Design decisions:
        - Formats retrieved documents in a structured way for the model
        - Uses careful prompt engineering to ensure model uses provided context
        - Implements a RAG pattern for knowledge-grounded responses
        - Instructs model to cite sources for accountability
        
        Args:
            prompt: User query
            context_docs: List of context documents from vector store
            
        Returns:
            Response with generated text and metadata
        """
        # Format retrieved documents with source attribution
        # Numbered for easy reference in model responses
        context_text = "\n\n".join([f"Document [{i+1}] (from {doc.get('source', 'unknown')}): {doc['text']}" 
                                  for i, doc in enumerate(context_docs)])
        
        # System prompt provides instruction on how to use context
        # Constraints help ensure higher quality responses
        system_prompt = """You are a helpful assistant. Answer the user's question based only on the provided context. 
If the context doesn't contain the information needed to answer the question, say you don't know and don't make up information.
Be concise but thorough, and cite which document you used by referring to its number."""
        
        # Format the user message with context
        # Clear separation between context and query helps model understand the task
        user_prompt = f"""I need information from the following context:

{context_text}

Based on this context, please answer my question: {prompt}"""

        # Use the standard generate method with our specialized prompts
        return self.generate(user_prompt, system_prompt)
