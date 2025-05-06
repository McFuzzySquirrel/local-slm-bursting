from typing import Dict, Any, List, Tuple
import re

class QueryRouter:
    def __init__(self, 
                 word_limit: int = 20,
                 complexity_keywords: List[str] = None,
                 verbose: bool = False):
        """
        Initialize the query router.
        
        Args:
            word_limit: Maximum number of words for a query to be considered simple
            complexity_keywords: List of keywords that indicate complex queries
            verbose: Whether to print verbose output
        """
        self.word_limit = word_limit
        self.verbose = verbose
        
        # Default complexity keywords if none provided
        self.complexity_keywords = complexity_keywords or [
            "compare", "contrast", "relate", "analyze", "evaluate", 
            "synthesize", "elaborate", "explain why", "versus",
            "difference between", "similarities", "hypothesis", 
            "implications", "consequences", "versus", "pros and cons",
            "advantages and disadvantages", "complex", "complicated"
        ]
    
    def is_simple_query(self, query: str) -> Tuple[bool, str]:
        """
        Determine if a query is simple enough for the local model.
        
        Args:
            query: The user query
            
        Returns:
            Tuple of (is_simple, reason)
        """
        # Clean and normalize the query
        query = query.strip().lower()
        
        # Check word count
        words = query.split()
        if len(words) > self.word_limit:
            return False, f"Query exceeds {self.word_limit} words"
        
        # Check for logical operators
        logical_operators = ["and", "or", "not", "if", "then", "because", "therefore", "thus", "hence"]
        for op in logical_operators:
            if f" {op} " in f" {query} ":  # Add spaces to ensure we match whole words
                return False, f"Contains logical operator: {op}"
        
        # Check for complexity keywords
        for keyword in self.complexity_keywords:
            if keyword.lower() in query:
                return False, f"Contains complexity keyword: {keyword}"
        
        # Check for question complexity (multiple question marks or nested questions)
        if query.count("?") > 1:
            return False, "Contains multiple questions"
        
        # Check for comparative statements
        comparative_pattern = r'\b(more|less|better|worse|larger|smaller|higher|lower)\b.*\b(than)\b'
        if re.search(comparative_pattern, query):
            return False, "Contains comparative statement"
        
        return True, "Simple query"
    
    def route_query(self, query: str, context_docs: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Determine the routing decision for a query.
        
        Args:
            query: The user query
            context_docs: Optional context documents
            
        Returns:
            Dictionary with routing decision
        """
        is_simple, reason = self.is_simple_query(query)
        
        # Determine if we have enough context
        has_context = context_docs is not None and len(context_docs) > 0
        
        # Logic for routing decision
        if is_simple:
            target = "local"
            confidence = 0.8 if has_context else 0.6
        else:
            target = "azure"
            confidence = 0.9
        
        if self.verbose:
            print(f"Query: '{query}' routed to {target} (simple: {is_simple}, reason: {reason})")
        
        return {
            "query": query,
            "route_to": target,
            "is_simple": is_simple,
            "reason": reason,
            "confidence": confidence,
            "has_context": has_context
        }
