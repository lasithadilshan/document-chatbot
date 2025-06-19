import streamlit as st
import os
from document_processor import DocumentProcessor
from vector_store import VectorStore
from chat_handler import ChatHandler
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Modern Document Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'suggested_questions' not in st.session_state:
        st.session_state.suggested_questions = []

def main():
    """Main application function"""
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    st.title("🤖 Modern Document Chat Assistant")
    st.markdown("**Powered by Gemini Flash 2.0 & FAISS Vector Search**")
    st.markdown("Upload documents and have intelligent conversations about their content!")
    st.markdown("</div>", unsafe_allow_html=True)

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("🔑 Google API Key not found. Please set GOOGLE_API_KEY in your .env file.")
        st.info("Get your API key from: https://aistudio.google.com/app/apikey")
        st.stop()

    # Initialize session state
    initialize_session_state()

    # Initialize components
    if st.session_state.vector_store is None:
        st.session_state.vector_store = VectorStore(api_key)
    
    chat_handler = ChatHandler(api_key)

    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        st.success("✅ API Key loaded successfully")
        
        # Document upload section
        st.header("📄 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files (max 200MB each)"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Process Documents", type="primary", use_container_width=True):
                if uploaded_files:
                    process_documents(uploaded_files, chat_handler)
                else:
                    st.warning("Please select files to upload first.")
        
        with col2:
            if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
                clear_all_data()
        
        # Document status
        st.header("📋 Document Status")
        display_document_status()
        
        # Quick actions
        if st.session_state.documents_processed:
            st.header("🚀 Quick Actions")
            if st.button("💡 Suggest Questions", use_container_width=True):
                generate_suggested_questions(chat_handler)

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("💬 Chat with Your Documents")
        
        if st.session_state.documents_processed:
            display_chat_interface(chat_handler)
        else:
            st.info("👆 Please upload and process documents using the sidebar to start chatting!")
            st.markdown("""
            ### How to use:
            1. **Upload documents** using the sidebar
            2. **Click "Process Documents"** to analyze them
            3. **Start asking questions** about your documents
            4. **View sources** for each response
            """)

    with col2:
        st.header("📊 Analytics")
        display_analytics()
        
        if st.session_state.suggested_questions:
            st.header("💡 Suggested Questions")
            display_suggested_questions()

def process_documents(uploaded_files, chat_handler):
    """Process uploaded documents with enhanced progress tracking"""
    processor = DocumentProcessor()
    
    all_chunks = []
    processed_files = []
    processing_info = []
    
    # Create progress containers
    progress_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing: {uploaded_file.name}")
            
            # Extract text
            text = processor.process_uploaded_file(uploaded_file)
            
            if text:
                # Chunk the text
                chunks = processor.chunk_text(text)
                
                # Add metadata to chunks
                chunk_metadata = []
                for j, chunk in enumerate(chunks):
                    metadata = {
                        'source': uploaded_file.name,
                        'chunk_id': j,
                        'file_type': uploaded_file.name.split('.')[-1].lower(),
                        'processed_at': datetime.now().isoformat()
                    }
                    chunk_metadata.append(metadata)
                
                all_chunks.extend(chunks)
                processed_files.append(uploaded_file.name)
                processing_info.append({
                    'file': uploaded_file.name,
                    'chunks': len(chunks),
                    'characters': len(text)
                })
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text("Finalizing...")
    
    if all_chunks:
        # Clear existing data and add new documents
        st.session_state.vector_store.clear()
        
        # Add documents to vector store
        success = st.session_state.vector_store.add_documents(
            all_chunks, 
            [{'source': info['file'], 'chunk_id': i} for info in processing_info for i in range(info['chunks'])]
        )
        
        if success:
            st.session_state.documents_processed = True
            st.session_state.processed_files = processed_files
            st.session_state.processing_info = processing_info
            st.session_state.chat_history = []  # Clear chat history
            
            # Display processing summary
            st.success(f"✅ Successfully processed {len(processed_files)} files!")
            
            with st.expander("📊 Processing Details"):
                for info in processing_info:
                    st.write(f"**{info['file']}**: {info['chunks']} chunks, {info['characters']:,} characters")
        else:
            st.error("❌ Failed to process documents. Please try again.")
    else:
        st.error("❌ No content could be extracted from the uploaded files.")

def display_chat_interface(chat_handler):
    """Display the enhanced chat interface"""
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📖 Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.write(f"**Source {i+1}:** {source}")

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                # Search for relevant context
                context_chunks = st.session_state.vector_store.search(prompt, k=5)
                
                # Generate response
                response = chat_handler.generate_response(prompt, context_chunks)
                
                st.write(response)
                
                # Show sources
                if context_chunks:
                    sources = []
                    with st.expander("📖 Sources Used", expanded=False):
                        for i, (chunk, score, metadata) in enumerate(context_chunks[:3]):
                            source_info = f"**Source {i+1}** (Relevance: {score:.2f})"
                            if metadata.get('source'):
                                source_info += f" - File: {metadata['source']}"
                            
                            st.write(source_info)
                            st.write(chunk[:300] + "..." if len(chunk) > 300 else chunk)
                            sources.append(f"{metadata.get('source', 'Unknown')} - Relevance: {score:.2f}")
                            st.divider()
                    
                    # Add sources to message
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response
                    })

def display_document_status():
    """Display enhanced document status information"""
    if st.session_state.documents_processed:
        st.success("✅ Documents Ready")
        
        # Display processed files
        if st.session_state.processed_files:
            st.write("**📁 Processed Files:**")
            for file in st.session_state.processed_files:
                st.write(f"• {file}")
        
        # Display statistics
        if hasattr(st.session_state, 'processing_info'):
            total_chunks = sum(info['chunks'] for info in st.session_state.processing_info)
            total_chars = sum(info['characters'] for info in st.session_state.processing_info)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📄 Total Chunks", total_chunks)
            with col2:
                st.metric("📝 Characters", f"{total_chars:,}")
    else:
        st.info("📄 No documents processed")

def display_analytics():
    """Display chat and document analytics"""
    if st.session_state.documents_processed:
        # Chat statistics
        total_messages = len(st.session_state.chat_history)
        user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        
        st.metric("💬 Total Messages", total_messages)
        st.metric("❓ Questions Asked", user_messages)
        
        # Vector store stats
        if st.session_state.vector_store:
            stats = st.session_state.vector_store.get_stats()
            st.metric("🔍 Searchable Chunks", stats["total_chunks"])
    else:
        st.info("Upload documents to see analytics")

def display_suggested_questions():
    """Display suggested questions as clickable buttons"""
    for i, question in enumerate(st.session_state.suggested_questions):
        if st.button(f"❓ {question}", key=f"suggested_{i}", use_container_width=True):
            # Add the question to chat
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.rerun()

def generate_suggested_questions(chat_handler):
    """Generate suggested questions based on document content"""
    if not st.session_state.documents_processed:
        return
    
    with st.spinner("🧠 Generating suggested questions..."):
        # Get sample content for question generation - use a non-empty query
        sample_chunks = st.session_state.vector_store.search("summary main topics", k=3)
        
        # If no results with the query, try getting chunks directly from stored texts
        if not sample_chunks and st.session_state.vector_store.texts:
            # Create mock chunks from the first few stored texts
            sample_chunks = []
            for i, text in enumerate(st.session_state.vector_store.texts[:3]):
                sample_chunks.append((text, 1.0, {'source': f'Document {i+1}'}))
        
        if sample_chunks:
            questions = chat_handler.suggest_questions(sample_chunks)
            st.session_state.suggested_questions = questions
            if questions:
                st.success(f"Generated {len(questions)} suggested questions!")
            else:
                st.warning("Could not generate questions. Try processing more documents.")
        else:
            st.warning("No document content available for question generation.")

def clear_all_data():
    """Clear all application data"""
    if st.session_state.vector_store:
        st.session_state.vector_store.clear()
    
    st.session_state.documents_processed = False
    st.session_state.processed_files = []
    st.session_state.chat_history = []
    st.session_state.suggested_questions = []
    
    if hasattr(st.session_state, 'processing_info'):
        delattr(st.session_state, 'processing_info')
    
    st.success("🗑️ All data cleared successfully!")
    st.rerun()

if __name__ == "__main__":
    main()
