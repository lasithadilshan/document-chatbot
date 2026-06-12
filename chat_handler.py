import os
import streamlit as st
from typing import List, Tuple
from huggingface_hub import InferenceClient


class ChatHandler:
    """Handles interaction with the Hugging Face inference API."""

    # Primary model and fallback in case the primary is unavailable / gated.
    PRIMARY_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
    FALLBACK_MODEL = "HuggingFaceH4/zephyr-7b-beta"

    def __init__(self, api_key: str):
        """Initialize the chat handler with a Hugging Face token."""
        resolved_key = str(api_key).strip() if api_key else os.getenv("HUGGINGFACE_API_KEY", "").strip()

        if not resolved_key:
            raise ValueError(
                "HUGGINGFACE_API_KEY is missing. Please set the HUGGINGFACE_API_KEY "
                "environment variable or add it to your .env file before starting the app."
            )

        self.api_key = resolved_key
        self.model_name = self.PRIMARY_MODEL
        self.client = InferenceClient(token=resolved_key)
        self._model_verified = False

    def _ensure_model(self):
        """Verify the primary model is accessible; fall back if not."""
        if self._model_verified:
            return
        try:
            # Quick probe with the primary model
            self.client.chat_completion(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=4,
            )
            self._model_verified = True
        except Exception:
            st.warning(
                f"⚠️ Primary model `{self.PRIMARY_MODEL}` is not accessible "
                f"(it may be gated). Falling back to `{self.FALLBACK_MODEL}`."
            )
            self.model_name = self.FALLBACK_MODEL
            self._model_verified = True

    def generate_response(self, query: str, context_chunks: List[Tuple[str, float, dict]]) -> str:
        """Generate a response using the configured Hugging Face model."""
        try:
            self._ensure_model()
            context = self._prepare_context(context_chunks)
            system_msg, user_msg = self._create_messages(query, context)

            response = self.client.chat_completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=1024,
                temperature=0.1,
                top_p=0.8,
            )

            text = response.choices[0].message.content
            if text:
                return text.strip()

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

    def _create_messages(self, query: str, context: str) -> tuple[str, str]:
        """Create system and user messages for the chat completion API."""

        if context:
            system_msg = (
                "You are an expert document analysis assistant. "
                "Answer questions based on the provided document excerpts. "
                "Be specific, cite relevant information, use a clear professional tone, "
                "and provide direct quotes when they support your answer. "
                "If the context doesn't fully address the question, clearly state what information is missing."
            )
            user_msg = (
                f"**DOCUMENT CONTEXT:**\n{context}\n\n"
                f"**USER QUESTION:** {query}"
            )
        else:
            system_msg = (
                "You are a helpful assistant. No relevant document context was found "
                "in the uploaded files. Provide a helpful response while clearly explaining "
                "that you don't have specific document context to reference."
            )
            user_msg = query

        return system_msg, user_msg

    def generate_summary(self, text: str) -> str:
        """Generate a summary of the document"""
        try:
            self._ensure_model()
            response = self.client.chat_completion(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a document summarisation assistant. Provide concise summaries focusing on main points, key findings, and important information.",
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a concise summary of the following document:\n\n{text[:8000]}",
                    },
                ],
                max_tokens=256,
                temperature=0.1,
                top_p=0.8,
            )
            result = response.choices[0].message.content
            return result.strip() if result else "Could not generate summary."

        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def suggest_questions(self, context_chunks: List[Tuple[str, float, dict]]) -> List[str]:
        """Suggest relevant questions based on document content"""
        if not context_chunks:
            return []

        try:
            self._ensure_model()
            # Use the first chunk for question generation
            sample_text = context_chunks[0][0][:2000]

            response = self.client.chat_completion(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You generate relevant questions about document content. Provide 3-5 questions in a simple list, each on its own line prefixed with a dash (-).",
                    },
                    {
                        "role": "user",
                        "content": f"Based on this document excerpt, suggest 3-5 relevant questions:\n\n{sample_text}",
                    },
                ],
                max_tokens=256,
                temperature=0.3,
                top_p=0.8,
            )

            text = response.choices[0].message.content
            if text:
                # Extract questions from the response
                questions = []
                for line in text.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                        question = line.lstrip('-•* ').strip()
                        if question:
                            questions.append(question)
                    elif line.endswith('?'):
                        questions.append(line)

                return questions[:5]  # Return max 5 questions

        except Exception as e:
            st.error(f"Error generating question suggestions: {str(e)}")

        return []