from typing import List
import math


class EmbeddingService:
    """Simple mock embedding service for basic functionality"""
    
    def __init__(self):
        pass
    
    def embed_text(self, text: str) -> List[float]:
        """Generate a simple hash-based embedding"""
        # Simple hash-based embedding (not real embeddings)
        hash_val = hash(text.lower())
        # Convert to a simple vector
        embedding = []
        for i in range(384):  # Standard embedding size
            embedding.append(float((hash_val + i) % 1000) / 1000.0)
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts"""
        return [self.embed_text(text) for text in texts]
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# Singleton instance
embedding_service = EmbeddingService()