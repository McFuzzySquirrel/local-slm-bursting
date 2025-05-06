import os
from typing import List, Dict, Any
from markitdown import MarkItDown  # Import markidown
import hashlib

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor with chunk size and overlap parameters.
        
        Args:
            chunk_size: The target size of each text chunk in characters
            chunk_overlap: The overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a PDF file and return chunks of text with metadata.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of dictionaries with text chunks and metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_name = os.path.basename(file_path)
        
        # Convert PDF to Markdown using MarkItDown
        try:
            md = MarkItDown()  # Initialize MarkItDown
            result = md.convert(file_path)  # Convert the PDF to Markdown
            markdown_text = result.text_content  # Extract the Markdown content
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to Markdown: {e}")
        
        # Create chunks
        chunks = self._create_chunks(markdown_text)
        
        # Add metadata to chunks
        result = []
        for i, chunk in enumerate(chunks):
            # Create a unique ID for each chunk based on content
            chunk_id = hashlib.md5(f"{file_name}_{i}_{chunk[:50]}".encode()).hexdigest()
            
            result.append({
                "id": chunk_id,
                "text": chunk,
                "source": file_name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
            
        return result
    
    def _create_chunks(self, text: str) -> List[str]:
        """
        Split text into chunks of approximately chunk_size characters with overlap.
        
        Args:
            text: The text to be chunked
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Find the end of the chunk
            end = min(start + self.chunk_size, text_length)
            
            # If we're not at the end of the text, try to find a good breaking point
            if end < text_length:
                # Look for paragraph breaks, periods, or spaces to break at
                for separator in ["\n\n", ".", " "]:
                    last_separator = text.rfind(separator, start, end)
                    if last_separator != -1:
                        end = last_separator + len(separator)
                        break
            
            # Add chunk to the list
            chunks.append(text[start:end].strip())
            
            # Move to the next chunk with overlap
            start = max(start, end - self.chunk_overlap)
            
            # If we couldn't move forward, force move to avoid infinite loop
            if start == end - self.chunk_overlap:
                start = end
        
        return chunks
