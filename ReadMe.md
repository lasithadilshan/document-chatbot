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
- **Email**: your-email@example.com

## 🌟 Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Built with ❤️ using modern AI technologies**

*Last updated: June 2025*