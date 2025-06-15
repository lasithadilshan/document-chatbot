import faiss
import numpy as np
import google.generativeai as genai
from typing import List, Tuple, Optional
import streamlit as st
import pickle
import os

class VectorStore:
    """Manages document embeddings using Gemini's embedding API and FAISS"""
    
    def __init__(self, api_key: str):
        """Initialize the vector store with Gemini API"""
        genai.configure(api_key=api_key)
        self.embedding_model = "models/text-embedding-004"
        self.dimension = 768  # Gemini text-embedding-004 dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []
        
    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings using Gemini's embedding API"""
        try:
            embeddings = []
            
            # Process in batches to avoid API limits
            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                # Get embeddings for the batch
                batch_embeddings = []
                for text in batch:
                    result = genai.embed_content(
                        model=self.embedding_model,
                        content=text,
                        task_type="retrieval_document"
                    )
                    batch_embeddings.append(result['embedding'])
                
                embeddings.extend(batch_embeddings)
            
            return np.array(embeddings, dtype=np.float32)
        
        except Exception as e:
            st.error(f"Error generating embeddings: {str(e)}")
            return np.array([])
    
    def add_documents(self, texts: List[str], metadata: Optional[List[dict]] = None) -> bool:
        """Add document chunks to the vector store"""
        if not texts:
            return False
        
        try:
            # Generate embeddings with progress bar
            with st.spinner("Creating embeddings with Gemini..."):
                embeddings = self._get_embeddings(texts)
            
            if embeddings.size == 0:
                st.error("Failed to generate embeddings")
                return False
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store texts and metadata
            self.texts.extend(texts)
            if metadata:
                self.metadata.extend(metadata)
            else:
                self.metadata.extend([{"chunk_id": i + len(self.metadata)} for i in range(len(texts))])
            
            st.success(f"Added {len(texts)} document chunks to vector store")
            return True
            
        except Exception as e:
            st.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float, dict]]:
        """Search for most relevant document chunks"""
        if self.index.ntotal == 0:
            return []
        
        try:
            # Generate query embedding
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = np.array([result['embedding']], dtype=np.float32)
            
            # Search in FAISS index
            distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
            
            # Convert results
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if 0 <= idx < len(self.texts):
                    # Convert L2 distance to similarity score
                    similarity = 1 / (1 + distance)
                    results.append((
                        self.texts[idx], 
                        similarity, 
                        self.metadata[idx] if idx < len(self.metadata) else {}
                    ))
            
            return results
            
        except Exception as e:
            st.error(f"Error searching vector store: {str(e)}")
            return []
    
    def save(self, filepath: str) -> bool:
        """Save the vector store to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, f"{filepath}.faiss")
            
            # Save texts and metadata
            with open(f"{filepath}.pkl", 'wb') as f:
                pickle.dump({
                    'texts': self.texts,
                    'metadata': self.metadata,
                    'dimension': self.dimension
                }, f)
            
            return True
        except Exception as e:
            st.error(f"Error saving vector store: {str(e)}")
            return False
    
    def load(self, filepath: str) -> bool:
        """Load the vector store from disk"""
        try:
            if not os.path.exists(f"{filepath}.faiss") or not os.path.exists(f"{filepath}.pkl"):
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            # Load texts and metadata
            with open(f"{filepath}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.metadata = data['metadata']
                self.dimension = data['dimension']
            
            return True
        except Exception as e:
            st.error(f"Error loading vector store: {str(e)}")
            return False
    
    def clear(self) -> None:
        """Clear the vector store"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store"""
        return {
            "total_chunks": len(self.texts),
            "index_size": self.index.ntotal,
            "dimension": self.dimension
        }