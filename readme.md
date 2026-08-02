# Enterprise Knowledge Assistant

Enterprise Knowledge Assistant is a Retrieval-Augmented Generation (RAG) application that enables users to interact with PDF documents through natural language. Instead of manually searching through lengthy documents, users can upload one or more PDFs and ask questions in plain English. The system retrieves the most relevant content from the uploaded documents and generates context-aware answers using Google's Gemini large language model.

This project demonstrates the practical implementation of modern Generative AI concepts, including document processing, semantic search, vector databases, embeddings, and large language model integration.

---

# Features

- Upload and process multiple PDF documents simultaneously.
- Extract text from PDF files automatically.
- Split large documents into meaningful text chunks.
- Generate semantic embeddings using Hugging Face Sentence Transformers.
- Store embeddings in a FAISS vector database for efficient similarity search.
- Retrieve the most relevant document sections based on user queries.
- Generate accurate answers using Google's Gemini model.
- Interactive web interface built with Streamlit.
- Environment variable support for secure API key management.

---

# Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Frontend | Streamlit |
| LLM Framework | LangChain |
| Large Language Model | Google Gemini |
| Embedding Model | Hugging Face Sentence Transformers |
| Vector Database | FAISS |
| PDF Processing | PyPDF2 |
| Environment Management | Python Dotenv |

---

# Project Structure

```
Enterprise-Knowledge-Assistant/
│
├── docs/
│   └── PDF-LangChain.jpg
│
├── app.py                 # Streamlit application
├── rag.py                 # RAG pipeline implementation
├── utils.py               # Utility functions
├── htmlTemplates.py       # UI templates
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variable template
├── .gitignore
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/PatiPranavi/Enterprise-Knowledge-Assistant.git

cd Enterprise-Knowledge-Assistant
```

## Create a Virtual Environment

```bash
python -m venv venv
```

## Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

Add your Google Gemini API key.

```env
GOOGLE_API_KEY=your_google_api_key
```

---

# Running the Application

Start the Streamlit server.

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# Workflow

The application follows a Retrieval-Augmented Generation (RAG) pipeline:

1. Users upload one or more PDF documents.
2. Text is extracted from each document using PyPDF2.
3. The extracted text is divided into smaller chunks using LangChain's Recursive Character Text Splitter.
4. Each chunk is converted into vector embeddings using Hugging Face Sentence Transformers.
5. The embeddings are stored in a FAISS vector database.
6. When a user submits a question, the system retrieves the most relevant document chunks through semantic similarity search.
7. The retrieved context is passed to Google's Gemini model, which generates a context-aware response.

---

# Example Use Cases

- Resume analysis
- Research paper summarization
- Academic document question answering
- Company policy document search
- Legal and technical documentation assistance
- Knowledge base chatbot
- Enterprise document search

---

# Future Enhancements

- Source citations with page numbers
- Conversation memory
- Chat history
- Streaming responses
- Support for DOCX, TXT and Markdown files
- OCR support for scanned PDFs
- User authentication
- Cloud deployment
- Multi-language document support
- Export chat history

---

# Acknowledgements

This project leverages several open-source technologies including Streamlit, LangChain, Hugging Face, FAISS, PyPDF2, and Google's Gemini API.
