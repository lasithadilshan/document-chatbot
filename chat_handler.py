import google.generativeai as genai
import streamlit as st
from typing import List, Tuple, Dict, Any

class ChatHandler:
    """Handles interaction with Google Gemini Flash 2.0 API"""
    
    def __init__(self, api_key: str):
        """Initialize the chat handler with Gemini API"""
        genai.configure(api_key=api_key)
        
        # Configure the model with optimized settings
        self.generation_config = genai.GenerationConfig(
            temperature=0.1,  # Lower temperature for more focused responses
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
        )
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def generate_response(self, query: str, context_chunks: List[Tuple[str, float, dict]]) -> str:
        """Generate response using Gemini with document context"""
        try:
            # Prepare context from retrieved chunks
            context = self._prepare_context(context_chunks)
            
            # Create the prompt
            prompt = self._create_prompt(query, context)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I encountered an error while generating a response. Please try again."
    
    def _prepare_context(self, context_chunks: List[Tuple[str, float, dict]]) -> str:
        """Prepare context from retrieved chunks"""
        if not context_chunks:
            return ""
        
        context_parts = []
        for i, (text, score, metadata) in enumerate(context_chunks[:3]):  # Use top 3 chunks
            chunk_info = f"**Document Excerpt {i+1}** (Relevance: {score:.2f})"
            if metadata.get('source'):
                chunk_info += f" - Source: {metadata['source']}"
            
            context_parts.append(f"{chunk_info}\n{text}")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create an optimized prompt for Gemini Flash 2.0"""
        
        if context:
            return f"""You are an expert document analysis assistant. Your task is to answer questions based on the provided document excerpts.

**DOCUMENT CONTEXT:**
{context}

**USER QUESTION:** {query}

**INSTRUCTIONS:**
1. Answer based primarily on the provided document context
2. Be specific and cite relevant information from the excerpts
3. If the context doesn't fully address the question, clearly state what information is missing
4. Use a clear, professional tone
5. Provide direct quotes when they support your answer
6. If you need to make inferences, clearly indicate this

**RESPONSE:**"""
        else:
            return f"""You are a helpful assistant. The user has asked a question about documents, but no relevant document context was found in the uploaded files.

**USER QUESTION:** {query}

Please provide a helpful response while clearly explaining that you don't have specific document context to reference. You may provide general information about the topic if appropriate, but emphasize the limitation.

**RESPONSE:**"""
    
    def generate_summary(self, text: str) -> str:
        """Generate a summary of the document"""
        try:
            prompt = f"""Please provide a concise summary of the following document. Focus on the main points, key findings, and important information.

**DOCUMENT:**
{text[:8000]}  # Limit to avoid token limits

**SUMMARY:**"""
            
            response = self.model.generate_content(prompt)
            return response.text if response.text else "Could not generate summary."
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def suggest_questions(self, context_chunks: List[Tuple[str, float, dict]]) -> List[str]:
        """Suggest relevant questions based on document content"""
        if not context_chunks:
            return []
        
        try:
            # Use the first chunk for question generation
            sample_text = context_chunks[0][0][:2000]
            
            prompt = f"""Based on this document excerpt, suggest 3-5 relevant questions that a user might ask. Focus on the main topics and important information covered.

**DOCUMENT EXCERPT:**
{sample_text}

**SUGGESTED QUESTIONS:**
Please provide questions in a simple list format."""
            
            response = self.model.generate_content(prompt)
            if response.text:
                # Extract questions from the response
                questions = []
                for line in response.text.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                        question = line[1:].strip()
                        if question:
                            questions.append(question)
                    elif line.endswith('?'):
                        questions.append(line)
                
                return questions[:5]  # Return max 5 questions
            
        except Exception as e:
            st.error(f"Error generating question suggestions: {str(e)}")
        
        return []