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

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Document Processing Chatbot - Architecture</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
        }

        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            color: #7f8c8d;
            font-size: 1.2em;
            font-weight: 300;
        }

        .architecture-diagram {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            grid-template-rows: auto auto auto auto;
            gap: 30px;
            margin: 40px 0;
            position: relative;
        }

        .layer {
            grid-column: 1 / -1;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
            margin: 10px 0;
            border-radius: 15px;
            position: relative;
        }

        .input-layer {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: white;
        }

        .processing-layer {
            background: linear-gradient(135deg, #fd79a8, #e84393);
            color: white;
        }

        .storage-layer {
            background: linear-gradient(135deg, #fdcb6e, #e17055);
            color: white;
        }

        .output-layer {
            background: linear-gradient(135deg, #6c5ce7, #a29bfe);
            color: white;
        }

        .component {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            min-width: 180px;
            transition: all 0.3s ease;
            position: relative;
        }

        .component:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.3);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .component-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
            display: block;
        }

        .component-title {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 8px;
        }

        .component-desc {
            font-size: 0.9em;
            opacity: 0.9;
            line-height: 1.4;
        }

        .arrow {
            position: absolute;
            font-size: 2em;
            color: #2c3e50;
            z-index: 10;
        }

        .arrow-down {
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
        }

        .flow-arrows {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        .flow-arrow {
            position: absolute;
            width: 3px;
            background: #2c3e50;
            opacity: 0.7;
        }

        .flow-arrow::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: -5px;
            width: 0;
            height: 0;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 12px solid #2c3e50;
        }

        .tech-stack {
            margin-top: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
        }

        .tech-stack h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.5em;
        }

        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .tech-item {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .tech-item:hover {
            transform: translateY(-3px);
        }

        .tech-icon {
            font-size: 2em;
            margin-bottom: 10px;
            display: block;
        }

        .data-flow {
            margin-top: 30px;
            padding: 20px;
            background: rgba(52, 152, 219, 0.1);
            border-radius: 15px;
            border-left: 5px solid #3498db;
        }

        .data-flow h4 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }

        .flow-steps {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .flow-step {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            min-width: 120px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            position: relative;
        }

        .flow-step:not(:last-child)::after {
            content: '→';
            position: absolute;
            right: -25px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.5em;
            color: #3498db;
            font-weight: bold;
        }

        .step-number {
            background: #3498db;
            color: white;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 8px;
            font-size: 0.9em;
            font-weight: bold;
        }

        @media (max-width: 768px) {
            .architecture-diagram {
                grid-template-columns: 1fr;
            }
            
            .layer {
                flex-direction: column;
                gap: 20px;
            }
            
            .flow-steps {
                flex-direction: column;
            }
            
            .flow-step:not(:last-child)::after {
                content: '↓';
                right: 50%;
                bottom: -25px;
                top: auto;
                transform: translateX(50%);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Modern Document Processing Chatbot</h1>
            <p class="subtitle">Powered by Gemini Flash 2.0 & FAISS Vector Search</p>
        </div>

        <div class="architecture-diagram">
            <!-- Input Layer -->
            <div class="layer input-layer">
                <div class="component">
                    <span class="component-icon">📄</span>
                    <div class="component-title">Document Upload</div>
                    <div class="component-desc">PDF, DOCX, TXT files via Streamlit interface</div>
                </div>
                <div class="component">
                    <span class="component-icon">💬</span>
                    <div class="component-title">User Query</div>
                    <div class="component-desc">Natural language questions about documents</div>
                </div>
                <div class="arrow arrow-down">⬇️</div>
            </div>

            <!-- Processing Layer -->
            <div class="layer processing-layer">
                <div class="component">
                    <span class="component-icon">🔍</span>
                    <div class="component-title">Document Processor</div>
                    <div class="component-desc">Text extraction & intelligent chunking</div>
                </div>
                <div class="component">
                    <span class="component-icon">🧠</span>
                    <div class="component-title">Gemini Embeddings</div>
                    <div class="component-desc">Convert text to vector representations</div>
                </div>
                <div class="component">
                    <span class="component-icon">🎯</span>
                    <div class="component-title">Query Processing</div>
                    <div class="component-desc">Semantic search & context retrieval</div>
                </div>
                <div class="arrow arrow-down">⬇️</div>
            </div>

            <!-- Storage Layer -->
            <div class="layer storage-layer">
                <div class="component">
                    <span class="component-icon">🗄️</span>
                    <div class="component-title">FAISS Vector Store</div>
                    <div class="component-desc">High-performance similarity search</div>
                </div>
                <div class="component">
                    <span class="component-icon">💾</span>
                    <div class="component-title">Document Metadata</div>
                    <div class="component-desc">Source tracking & chunk information</div>
                </div>
                <div class="component">
                    <span class="component-icon">🔄</span>
                    <div class="component-title">Session State</div>
                    <div class="component-desc">Chat history & user context</div>
                </div>
                <div class="arrow arrow-down">⬇️</div>
            </div>

            <!-- Output Layer -->
            <div class="layer output-layer">
                <div class="component">
                    <span class="component-icon">⚡</span>
                    <div class="component-title">Gemini Flash 2.0</div>
                    <div class="component-desc">Context-aware response generation</div>
                </div>
                <div class="component">
                    <span class="component-icon">📊</span>
                    <div class="component-title">Response UI</div>
                    <div class="component-desc">Formatted answers with source citations</div>
                </div>
                <div class="component">
                    <span class="component-icon">💡</span>
                    <div class="component-title">Smart Features</div>
                    <div class="component-desc">Suggested questions & analytics</div>
                </div>
            </div>
        </div>

        <!-- Data Flow -->
        <div class="data-flow">
            <h4>📈 Data Flow Process</h4>
            <div class="flow-steps">
                <div class="flow-step">
                    <div class="step-number">1</div>
                    <div>Upload</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">2</div>
                    <div>Extract</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">3</div>
                    <div>Chunk</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">4</div>
                    <div>Embed</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">5</div>
                    <div>Store</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">6</div>
                    <div>Query</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">7</div>
                    <div>Search</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">8</div>
                    <div>Generate</div>
                </div>
                <div class="flow-step">
                    <div class="step-number">9</div>
                    <div>Respond</div>
                </div>
            </div>
        </div>

        <!-- Technology Stack -->
        <div class="tech-stack">
            <h3>🛠️ Technology Stack</h3>
            <div class="tech-grid">
                <div class="tech-item">
                    <span class="tech-icon">🌐</span>
                    <div><strong>Streamlit 1.39.0</strong></div>
                    <div>Web Interface</div>
                </div>
                <div class="tech-item">
                    <span class="tech-icon">🤖</span>
                    <div><strong>Gemini Flash 2.0</strong></div>
                    <div>AI Language Model</div>
                </div>
                <div class="tech-item">
                    <span class="tech-icon">🔍</span>
                    <div><strong>FAISS 1.8.0</strong></div>
                    <div>Vector Search</div>
                </div>
                <div class="tech-item">
                    <span class="tech-icon">📄</span>
                    <div><strong>PyPDF2 + docx</strong></div>
                    <div>Document Parsing</div>
                </div>
                <div class="tech-item">
                    <span class="tech-icon">🐍</span>
                    <div><strong>Python 3.8+</strong></div>
                    <div>Core Language</div>
                </div>
                <div class="tech-item">
                    <span class="tech-icon">🔢</span>
                    <div><strong>NumPy 1.26.4</strong></div>
                    <div>Numerical Computing</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>