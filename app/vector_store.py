import os
import faiss
from config.settings import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import numpy as np
import pickle

class VectorStore:
    def __init__(self, persist_directory=None):
        """Initialize the vector store."""
        settings = Settings()
        
        # Use settings from config, with environment variables as fallback
        self.persist_directory = persist_directory or settings.vector_store_path
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Path to save FAISS index and metadata
        self.index_path = os.path.join(self.persist_directory, "faiss_index")
        self.metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
        
        # Initialize FAISS index and metadata
        self.embedding_dim = 384  # Dimension of embeddings (e.g., for 'all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.metadata = {}  # Store metadata for each vector
        
        # Load existing index and metadata if available
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        
        if settings.verbose:
            print(f"Vector store initialized with FAISS at '{self.persist_directory}'")

        # Initialize the embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document chunks with text and metadata
        """
        if not documents:
            return
        
        # Extract text for embedding
        texts = [doc["text"] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts)
        
        # Add embeddings to FAISS index
        self.index.add(np.array(embeddings, dtype=np.float32))
        
        # Store metadata
        for i, doc in enumerate(documents):
            self.metadata[len(self.metadata)] = {
                "text": doc["text"],
                "source": doc.get("source", "Unknown"),
                "chunk_index": doc.get("chunk_index", 0),
                "total_chunks": doc.get("total_chunks", 1),
            }
        
        # Persist the index and metadata
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)
    
    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: The search query
            top_k: Number of results to return
            
        Returns:
            List of documents with similarity scores
        """
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode([query])
        
        # Search in the FAISS index
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)
        
        # Format the results
        formatted_results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:  # No more results
                continue
            metadata = self.metadata.get(idx, {})
            formatted_results.append({
                "text": metadata.get("text", ""),
                "source": metadata.get("source", "Unknown"),
                "chunk_index": metadata.get("chunk_index", 0),
                "similarity_score": 1.0 - distances[0][i],  # Convert distance to similarity
            })
        
        return formatted_results
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Embed a single text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        return self.embedding_model.encode(text)
