import os
from typing import Dict, Any, Optional, List
from llama_cpp import Llama
import time

class LocalLLM:
    def __init__(
        self, 
        model_path: str, 
        context_size: int = 2048,
        max_tokens: int = 512,
        temperature: float = 0.7,
        verbose: bool = False
    ):
        """
        Initialize the local LLM using llama.cpp.
        
        Args:
            model_path: Path to the GGUF model file
            context_size: Maximum context size for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            verbose: Whether to print verbose output
        """
        self.model_path = model_path
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        self.context_size = context_size
        
        # Initialize model
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Lazy loading - we'll load the model when it's first used
        self.model = None
    
    def _load_model(self):
        """Load the model if not already loaded"""
        if self.model is None:
            if self.verbose:
                print(f"Loading model from {self.model_path}...")
            start_time = time.time()
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=self.context_size,
                n_gpu_layers=-1  # Auto-detect number of layers to offload to GPU
            )
            if self.verbose:
                print(f"Model loaded in {time.time() - start_time:.2f}s")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            
        Returns:
            Response containing generated text and metadata
        """
        self._load_model()
        
        start_time = time.time()
        
        # Combine system prompt and user prompt if needed
        if system_prompt:
            full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>"
        else:
            full_prompt = prompt
            
        if self.verbose:
            print(f"Generating response with local LLM for prompt: {prompt[:50]}...")
            
        # Generate completion
        response = self.model.create_completion(
            prompt=full_prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stop=["<|user|>", "<|system|>"]  # Stop tokens
        )
        
        generation_time = time.time() - start_time
        
        # Extract the generated text
        generated_text = response.get("choices", [{}])[0].get("text", "").strip()
        
        return {
            "response": generated_text,
            "source": "local",
            "model": os.path.basename(self.model_path),
            "generation_time": generation_time,
            "completion_tokens": len(response.get("choices", [{}])[0].get("text", "").split())
        }
    
    def generate_with_context(self, prompt: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a completion with document context.
        
        Args:
            prompt: The user query
            context_docs: List of context documents from vector store
            
        Returns:
            Response with generated text and metadata
        """
        # Format the context documents
        context_text = "\n\n".join([f"Document [{i+1}] (from {doc.get('source', 'unknown')}): {doc['text']}" 
                                  for i, doc in enumerate(context_docs)])
        
        # Create the context-aware prompt
        system_prompt = """You are a helpful assistant. Answer the user's question based on the provided context. 
If the context doesn't contain the information needed, say you don't know and avoid making up information.
Use the provided documents to give accurate answers."""
        
        full_prompt = f"""Context information:
{context_text}

Question: {prompt}

Answer:"""

        return self.generate(full_prompt, system_prompt)
