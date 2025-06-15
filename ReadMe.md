# Modern Generative AI Document Processing Chatbot

🤖 **Powered by Gemini Flash 2.0 & FAISS Vector Search**

A modern, production-ready document processing chatbot that allows users to upload documents and have intelligent conversations about their content using Google's Gemini Flash 2.0 model.

## ✨ Features

- **Multi-format Support**: PDF, DOCX, and TXT files
- **Intelligent Search**: FAISS vector database with Gemini embeddings
- **Context-aware Responses**: Powered by Gemini Flash 2.0
- **Real-time Chat**: Interactive web interface with source attribution
- **Smart Analytics**: Document processing statistics and chat metrics
- **Suggested Questions**: AI-generated relevant questions
- **Modern UI**: Clean, responsive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI Studio API Key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd document-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   
   Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
document-chatbot/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document parsing utilities
├── vector_store.py       # FAISS vector store with Gemini embeddings
├── chat_handler.py       # Gemini API interaction
├── requirements.txt      # Dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # ReadMe file
```

## 🛠️ Core Components

### Document Processor (`document_processor.py`)
- Extracts text from PDF, DOCX, and TXT files
- Smart text chunking with overlap
- Robust error handling and text cleaning

### Vector Store (`vector_store.py`)
- FAISS-based similarity search
- Gemini text-embedding-004 for embeddings
- Persistent storage and retrieval
- Batch processing for efficiency

### Chat Handler (`chat_handler.py`)
- Gemini Flash 2.0 integration
- Context-aware response generation
- Safety settings and content filtering
- Optimized prompt engineering

### Main Application (`app.py`)
- Streamlit web interface
- Session state management
- Real-time chat functionality
- Analytics and suggested questions

## 📋 Dependencies

```
streamlit==1.39.0
google-generativeai==0.8.3
faiss-cpu==1.8.0
PyPDF2==3.0.1
python-docx==1.1.2
numpy==1.26.4
python-dotenv==1.0.1
```

## 🎯 Usage Examples

### Effective Questions for Document Q&A

**Specific Information Retrieval:**
- "What are the main findings in this report?"
- "Can you extract all the dates and deadlines mentioned?"
- "What statistics or numbers are provided about [specific topic]?"

**Analysis and Comparison:**
- "Compare the advantages and disadvantages discussed"
- "What are the main differences between [concept A] and [concept B]?"
- "How does this document support or contradict [specific claim]?"

**Summary and Synthesis:**
- "Provide a bullet-point summary of the main topics"
- "What are the key recommendations or action items?"
- "Explain the main argument or thesis of this document"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Gemini API key from Google AI Studio | Yes |

### Model Settings

The application uses optimized settings for Gemini Flash 2.0:
- **Temperature**: 0.1 (focused responses)
- **Top-p**: 0.8
- **Top-k**: 40
- **Max tokens**: 2048

## 📊 Features Overview

### Document Processing
- ✅ Multi-file upload support
- ✅ Automatic text extraction and cleaning
- ✅ Smart chunking with configurable overlap
- ✅ Progress tracking and error handling

### Vector Search
- ✅ FAISS similarity search
- ✅ Gemini embeddings (768 dimensions)
- ✅ Relevance scoring
- ✅ Source attribution

### Chat Interface
- ✅ Real-time conversation
- ✅ Context-aware responses
- ✅ Source citation and expandable references
- ✅ Chat history persistence

### Analytics & Insights
- ✅ Document processing statistics
- ✅ Chat metrics and usage tracking
- ✅ AI-generated suggested questions
- ✅ Performance monitoring

## 🚀 Advanced Features

### Suggested Questions
The application automatically generates relevant questions based on your document content using Gemini's understanding of the material.

### Source Attribution
Every response includes expandable source references showing:
- Relevance scores
- Source document names
- Specific text excerpts used

### Smart Chunking
Documents are intelligently split while preserving:
- Sentence boundaries
- Paragraph structure
- Context continuity

## 🛡️ Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Corrupted documents
- API rate limits
- Network connectivity issues
- Memory constraints

## 🔍 Troubleshooting

### Common Issues

**API Key Problems:**
```python
# Test your API key
import google.generativeai as genai
genai.configure(api_key="your-key-here")
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("Hello!")
print(response.text)
```

**Memory Issues with Large Documents:**
- Reduce chunk_size to 500-800 characters
- Process documents in smaller batches
- Clear vector store between different document sets

**Slow Performance:**
- Use smaller embedding batches
- Limit search results (reduce k parameter)
- Consider FAISS with GPU support for large datasets

**File Processing Errors:**
- Ensure files are not corrupted
- Check file permissions
- Try processing one file at a time

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

**Docker (Recommended):**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Cloud Platforms:**
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Instances
- Heroku
- Streamlit Cloud

## 🔄 Future Enhancements

### Immediate Improvements
- [ ] Add Excel and PowerPoint support
- [ ] Implement semantic chunking
- [ ] Add vector store persistence
- [ ] Enhanced UI with dark mode

### Advanced Features
- [ ] Multi-language support
- [ ] Document comparison tools
- [ ] Export functionality
- [ ] User authentication

### Production Features
- [ ] Docker containerization
- [ ] Cloud deployment templates
- [ ] API endpoints
- [ ] User analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini Team** for the powerful Flash 2.0 model
- **Facebook AI Research** for FAISS vector search
- **Streamlit Team** for the excellent web framework
- **Open Source Community** for the supporting libraries

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: dilshantilakaratne29@gmail.com

## 🌟 Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Built with ❤️ using modern AI technologies**

*Last updated: June 2025*

## Architect Diagram

<svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="frontendGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#11998e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38ef7d;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="processingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#feca57;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="vectorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3742fa;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#70a1ff;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="aiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#5f27cd;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#a55eea;stop-opacity:1" />
    </linearGradient>
    
    <!-- Arrow marker -->
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555" />
    </marker>
    
    <!-- Drop shadow filter -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="3" dy="3" stdDeviation="3" flood-color="#00000030"/>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="1200" height="800" fill="#f8f9fa"/>
  
  <!-- Title -->
  <rect x="0" y="0" width="1200" height="60" fill="url(#headerGrad)"/>
  <text x="600" y="35" text-anchor="middle" fill="white" font-size="24" font-weight="bold" font-family="Arial, sans-serif">
    Modern Document Processing Chatbot Architecture
  </text>
  <text x="600" y="52" text-anchor="middle" fill="white" font-size="12" font-family="Arial, sans-serif" opacity="0.9">
    Powered by Gemini Flash 2.0 & FAISS Vector Search
  </text>
  
  <!-- Frontend Layer -->
  <g id="frontend-layer">
    <rect x="50" y="90" width="300" height="200" rx="15" fill="url(#frontendGrad)" filter="url(#shadow)"/>
    <text x="200" y="115" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Frontend Layer</text>
    <text x="200" y="135" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Streamlit Web App</text>
    
    <!-- Streamlit components -->
    <rect x="70" y="150" width="80" height="35" rx="5" fill="white" opacity="0.9"/>
    <text x="110" y="170" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">File Upload</text>
    
    <rect x="160" y="150" width="80" height="35" rx="5" fill="white" opacity="0.9"/>
    <text x="200" y="170" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">Chat Interface</text>
    
    <rect x="250" y="150" width="80" height="35" rx="5" fill="white" opacity="0.9"/>
    <text x="290" y="170" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">Analytics</text>
    
    <rect x="115" y="195" width="80" height="35" rx="5" fill="white" opacity="0.9"/>
    <text x="155" y="215" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">Progress UI</text>
    
    <rect x="205" y="195" width="80" height="35" rx="5" fill="white" opacity="0.9"/>
    <text x="245" y="215" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">Source Display</text>
    
    <!-- File types -->
    <circle cx="80" cy="255" r="15" fill="#e74c3c"/>
    <text x="80" y="260" text-anchor="middle" fill="white" font-size="8" font-weight="bold">PDF</text>
    
    <circle cx="120" cy="255" r="15" fill="#3498db"/>
    <text x="120" y="260" text-anchor="middle" fill="white" font-size="8" font-weight="bold">DOCX</text>
    
    <circle cx="160" cy="255" r="15" fill="#2ecc71"/>
    <text x="160" y="260" text-anchor="middle" fill="white" font-size="8" font-weight="bold">TXT</text>
  </g>
  
  <!-- Document Processing Layer -->
  <g id="processing-layer">
    <rect x="400" y="90" width="350" height="200" rx="15" fill="url(#processingGrad)" filter="url(#shadow)"/>
    <text x="575" y="115" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Document Processing Layer</text>
    
    <!-- Document Processor -->
    <rect x="420" y="130" width="150" height="70" rx="8" fill="white" opacity="0.9"/>
    <text x="495" y="150" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Document Processor</text>
    <text x="495" y="165" text-anchor="middle" fill="#2c3e50" font-size="9">• Text Extraction</text>
    <text x="495" y="175" text-anchor="middle" fill="#2c3e50" font-size="9">• Format Handling</text>
    <text x="495" y="185" text-anchor="middle" fill="#2c3e50" font-size="9">• Error Handling</text>
    
    <!-- Text Chunking -->
    <rect x="580" y="130" width="150" height="70" rx="8" fill="white" opacity="0.9"/>
    <text x="655" y="150" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Text Chunking</text>
    <text x="655" y="165" text-anchor="middle" fill="#2c3e50" font-size="9">• Smart Boundaries</text>
    <text x="655" y="175" text-anchor="middle" fill="#2c3e50" font-size="9">• Overlap Strategy</text>
    <text x="655" y="185" text-anchor="middle" fill="#2c3e50" font-size="9">• Metadata Addition</text>
    
    <!-- Processing Flow -->
    <rect x="420" y="220" width="310" height="50" rx="8" fill="white" opacity="0.9"/>
    <text x="575" y="240" text-anchor="middle" fill="#2c3e50" font-size="11" font-weight="bold">Processing Pipeline</text>
    <text x="575" y="255" text-anchor="middle" fill="#2c3e50" font-size="9">Upload → Extract → Clean → Chunk → Embed → Store</text>
  </g>
  
  <!-- Vector Store Layer -->
  <g id="vector-layer">
    <rect x="50" y="320" width="300" height="200" rx="15" fill="url(#vectorGrad)" filter="url(#shadow)"/>
    <text x="200" y="345" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Vector Store Layer</text>
    
    <!-- FAISS Database -->
    <rect x="70" y="360" width="120" height="80" rx="8" fill="white" opacity="0.9"/>
    <text x="130" y="380" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">FAISS Index</text>
    <text x="130" y="395" text-anchor="middle" fill="#2c3e50" font-size="9">• Vector Storage</text>
    <text x="130" y="405" text-anchor="middle" fill="#2c3e50" font-size="9">• Similarity Search</text>
    <text x="130" y="415" text-anchor="middle" fill="#2c3e50" font-size="9">• L2 Distance</text>
    <text x="130" y="425" text-anchor="middle" fill="#2c3e50" font-size="9">• Fast Retrieval</text>
    
    <!-- Embeddings -->
    <rect x="210" y="360" width="120" height="80" rx="8" fill="white" opacity="0.9"/>
    <text x="270" y="380" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Embeddings</text>
    <text x="270" y="395" text-anchor="middle" fill="#2c3e50" font-size="9">• 768 Dimensions</text>
    <text x="270" y="405" text-anchor="middle" fill="#2c3e50" font-size="9">• Semantic Search</text>
    <text x="270" y="415" text-anchor="middle" fill="#2c3e50" font-size="9">• Context Matching</text>
    <text x="270" y="425" text-anchor="middle" fill="#2c3e50" font-size="9">• Relevance Score</text>
    
    <!-- Metadata Store -->
    <rect x="140" y="450" width="120" height="50" rx="8" fill="white" opacity="0.9"/>
    <text x="200" y="470" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Metadata Store</text>
    <text x="200" y="485" text-anchor="middle" fill="#2c3e50" font-size="9">Sources • Chunks • Timestamps</text>
  </g>
  
  <!-- AI/LLM Layer -->
  <g id="ai-layer">
    <rect x="800" y="90" width="350" height="430" rx="15" fill="url(#aiGrad)" filter="url(#shadow)"/>
    <text x="975" y="115" text-anchor="middle" fill="white" font-size="16" font-weight="bold">AI/LLM Layer</text>
    <text x="975" y="135" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Google Gemini Flash 2.0</text>
    
    <!-- Embedding API -->
    <rect x="820" y="150" width="150" height="80" rx="8" fill="white" opacity="0.9"/>
    <text x="895" y="170" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Embedding API</text>
    <text x="895" y="185" text-anchor="middle" fill="#2c3e50" font-size="9">text-embedding-004</text>
    <text x="895" y="200" text-anchor="middle" fill="#2c3e50" font-size="9">• Document Encoding</text>
    <text x="895" y="210" text-anchor="middle" fill="#2c3e50" font-size="9">• Query Encoding</text>
    <text x="895" y="220" text-anchor="middle" fill="#2c3e50" font-size="9">• Batch Processing</text>
    
    <!-- Generation API -->
    <rect x="980" y="150" width="150" height="80" rx="8" fill="white" opacity="0.9"/>
    <text x="1055" y="170" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Generation API</text>
    <text x="1055" y="185" text-anchor="middle" fill="#2c3e50" font-size="9">gemini-2.0-flash-exp</text>
    <text x="1055" y="200" text-anchor="middle" fill="#2c3e50" font-size="9">• Context-Aware</text>
    <text x="1055" y="210" text-anchor="middle" fill="#2c3e50" font-size="9">• Fast Response</text>
    <text x="1055" y="220" text-anchor="middle" fill="#2c3e50" font-size="9">• Safety Filters</text>
    
    <!-- Chat Handler -->
    <rect x="820" y="250" width="310" height="80" rx="8" fill="white" opacity="0.9"/>
    <text x="975" y="270" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">Chat Handler</text>
    <text x="975" y="285" text-anchor="middle" fill="#2c3e50" font-size="9">• Prompt Engineering • Context Preparation • Response Generation</text>
    <text x="975" y="300" text-anchor="middle" fill="#2c3e50" font-size="9">• Source Attribution • Question Suggestions • Summary Generation</text>
    <text x="975" y="315" text-anchor="middle" fill="#2c3e50" font-size="9">Temperature: 0.1 • Max Tokens: 2048 • Safety Settings</text>
    
    <!-- RAG Process -->
    <rect x="820" y="350" width="310" height="100" rx="8" fill="white" opacity="0.9"/>
    <text x="975" y="370" text-anchor="middle" fill="#2c3e50" font-size="12" font-weight="bold">RAG (Retrieval-Augmented Generation)</text>
    
    <rect x="840" y="380" width="90" height="25" rx="3" fill="#3498db" opacity="0.8"/>
    <text x="885" y="395" text-anchor="middle" fill="white" font-size="8" font-weight="bold">1. Retrieve</text>
    
    <rect x="940" y="380" width="90" height="25" rx="3" fill="#e74c3c" opacity="0.8"/>
    <text x="985" y="395" text-anchor="middle" fill="white" font-size="8" font-weight="bold">2. Augment</text>
    
    <rect x="1040" y="380" width="90" height="25" rx="3" fill="#2ecc71" opacity="0.8"/>
    <text x="1085" y="395" text-anchor="middle" fill="white" font-size="8" font-weight="bold">3. Generate</text>
    
    <text x="975" y="420" text-anchor="middle" fill="#2c3e50" font-size="9">Query → Vector Search → Context Injection → LLM Response</text>
    <text x="975" y="435" text-anchor="middle" fill="#2c3e50" font-size="9">With source attribution and relevance scoring</text>
    
    <!-- Features -->
    <rect x="820" y="470" width="310" height="40" rx="8" fill="white" opacity="0.9"/>
    <text x="975" y="485" text-anchor="middle" fill="#2c3e50" font-size="10" font-weight="bold">Key Features</text>
    <text x="975" y="500" text-anchor="middle" fill="#2c3e50" font-size="9">Multi-file Support • Real-time Chat • Source Citations • Question Suggestions</text>
  </g>
  
  <!-- Data Flow Arrows -->
  <!-- Frontend to Processing -->
  <path d="M 350 190 Q 375 190 400 190" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="375" y="185" text-anchor="middle" fill="#555" font-size="10">Upload</text>
  
  <!-- Processing to Vector Store -->
  <path d="M 500 290 Q 500 305 350 350" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="425" y="320" text-anchor="middle" fill="#555" font-size="10">Embed</text>
  
  <!-- Processing to AI (Embedding) -->
  <path d="M 650 200 Q 725 200 800 200" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="725" y="195" text-anchor="middle" fill="#555" font-size="10">Text</text>
  
  <!-- Vector Store to AI (Search) -->
  <path d="M 350 420 Q 575 420 800 350" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="575" y="415" text-anchor="middle" fill="#555" font-size="10">Retrieve</text>
  
  <!-- AI back to Frontend -->
  <path d="M 800 300 Q 600 300 600 250 Q 600 200 350 200" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="575" y="275" text-anchor="middle" fill="#555" font-size="10">Response</text>
  
  <!-- Frontend Query to AI -->
  <path d="M 300 150 Q 550 120 800 250" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)" stroke-dasharray="5,5"/>
  <text x="550" y="185" text-anchor="middle" fill="#555" font-size="10">Query</text>
  
  <!-- Technology Stack -->
  <g id="tech-stack">
    <rect x="400" y="550" width="400" height="180" rx="15" fill="white" stroke="#ddd" stroke-width="2" filter="url(#shadow)"/>
    <text x="600" y="575" text-anchor="middle" fill="#2c3e50" font-size="16" font-weight="bold">Technology Stack</text>
    
    <!-- Frontend Tech -->
    <rect x="420" y="590" width="110" height="60" rx="5" fill="#11998e" opacity="0.1" stroke="#11998e" stroke-width="1"/>
    <text x="475" y="605" text-anchor="middle" fill="#2c3e50" font-size="11" font-weight="bold">Frontend</text>
    <text x="475" y="620" text-anchor="middle" fill="#2c3e50" font-size="9">Streamlit 1.39.0</text>
    <text x="475" y="630" text-anchor="middle" fill="#2c3e50" font-size="9">Python 3.8+</text>
    <text x="475" y="640" text-anchor="middle" fill="#2c3e50" font-size="9">Web Interface</text>
    
    <!-- Processing Tech -->
    <rect x="540" y="590" width="110" height="60" rx="5" fill="#ff6b6b" opacity="0.1" stroke="#ff6b6b" stroke-width="1"/>
    <text x="595" y="605" text-anchor="middle" fill="#2c3e50" font-size="11" font-weight="bold">Processing</text>
    <text x="595" y="620" text-anchor="middle" fill="#2c3e50" font-size="9">PyPDF2 3.0.1</text>
    <text x="595" y="630" text-anchor="middle" fill="#2c3e50" font-size="9">python-docx 1.1.2</text>
    <text x="595" y="640" text-anchor="middle" fill="#2c3e50" font-size="9">Text Processing</text>
    
    <!-- Vector Tech -->
    <rect x="660" y="590" width="110" height="60" rx="5" fill="#3742fa" opacity="0.1" stroke="#3742fa" stroke-width="1"/>
    <text x="715" y="605" text-anchor="middle" fill="#2c3e50" font-size="11" font-weight="bold">Vector Store</text>
    <text x="715" y="620" text-anchor="middle" fill="#2c3e50" font-size="9">FAISS 1.8.0</text>
    <text x="715" y="630" text-anchor="middle" fill="#2c3e50" font-size="9">NumPy 1.26.4</text>
    <text x="715" y="640" text-anchor="middle" fill="#2c3e50" font-size="9">Vector Search</text>
    
    <!-- Additional Libraries -->
    <rect x="420" y="660" width="350" height="40" rx="5" fill="#f8f9fa" stroke="#ddd" stroke-width="1"/>
    <text x="595" y="675" text-anchor="middle" fill="#2c3e50" font-size="11" font-weight="bold">Additional Dependencies</text>
    <text x="595" y="690" text-anchor="middle" fill="#2c3e50" font-size="9">google-generativeai 0.8.3 • python-dotenv 1.0.1 • Environment Management</text>
  </g>
  
  <!-- Version and Credits -->
  <text x="1150" y="780" text-anchor="end" fill="#666" font-size="10" font-family="Arial, sans-serif">
    Architecture v1.0 - Modern Document Processing Chatbot
  </text>
</svg>