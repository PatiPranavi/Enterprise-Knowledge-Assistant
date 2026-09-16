# Enterprise Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF documents and ask questions about their content using natural language.

## Features

- Upload multiple PDF documents
- Extract text page by page
- Split documents into smaller chunks
- Generate semantic embeddings using HuggingFace
- Store embeddings in FAISS
- Retrieve relevant chunks using similarity search
- Generate grounded answers using Google Gemini
- Display source document and page numbers
- Reduce unsupported answers using a grounding prompt
- Interactive Streamlit interface

## How It Works

```text
PDF Documents
      ↓
Text Extraction
      ↓
Document Chunking
      ↓
HuggingFace Embeddings
      ↓
FAISS Vector Store
      ↓
Similarity Search
      ↓
Relevant Context
      ↓
Grounded Prompt
      ↓
Google Gemini
      ↓
Answer + Sources
```

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini
- HuggingFace Sentence Transformers
- FAISS
- PyPDF2

## RAG Pipeline

### 1. Document Processing

PDF files are read page by page using PyPDF2.

Each page is stored as a LangChain `Document` with metadata containing:

- Source PDF filename
- Page number

This metadata is used to display the source of retrieved information.

### 2. Text Chunking

Documents are split into smaller chunks using `RecursiveCharacterTextSplitter`.

- Chunk size: 1000 characters
- Chunk overlap: 200 characters

Chunking allows the system to work with smaller portions of documents during retrieval.

### 3. Embeddings

Each text chunk is converted into a numerical vector using the HuggingFace model:

`sentence-transformers/all-MiniLM-L6-v2`

These vectors capture the semantic meaning of the text and are used for similarity-based retrieval.

### 4. Vector Store

The generated embeddings are stored in a FAISS vector store.

FAISS is used to perform efficient similarity searches over the embedded document chunks.

### 5. Retrieval

When a user asks a question, the question is compared against the stored document embeddings.

The system retrieves the top 4 most relevant chunks using vector similarity search.

### 6. Answer Generation

The retrieved chunks are passed to Google Gemini as context.

The prompt instructs the model to answer only using the provided context.

If the required information is not present in the provided context, the assistant is instructed to respond that the information could not be found in the uploaded documents.

### 7. Source Traceability

Each retrieved document chunk contains metadata identifying its source PDF and page number.

The application displays the source PDF filename and page number below the generated answer.

## Grounding

The application uses a grounding prompt to reduce unsupported responses.

If the required information is not present in the retrieved context, the assistant responds:

> "I couldn't find this information in the uploaded documents."

This keeps the generated response focused on the uploaded documents.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_google_api_key
```

## Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application allows users to upload multiple PDF documents, build a searchable knowledge base, and ask questions about their content.

## Project Structure

```text
Enterprise-Knowledge-Assistant/
│
├── app.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
├── readme.md
├── htmlTemplates.py
├── utils.py
│
└── docs/
    └── PDF-LangChain.jpg
```

## Future Improvements

The current implementation focuses on a simple and explainable RAG pipeline. Possible future improvements include:

- Hybrid search combining semantic and keyword-based retrieval
- Reranking retrieved documents
- Conversation memory
- Streaming responses
- Support for DOCX, TXT, and Markdown files
- OCR support for scanned PDFs
- Authentication and access control
- Cloud deployment
- RAG evaluation and monitoring
