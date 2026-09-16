
import os
from langchain_core.documents import Document
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# -----------------------------
# PDF READER
# -----------------------------
def read_pdf(files):
    documents = []

    for pdf in files:
        reader = PdfReader(pdf)

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                documents.append(
                    Document(
                        page_content=page_text,
                        metadata={
                            "source": pdf.name,
                            "page": page_number
                        }
                    )
                )

    return documents

# -----------------------------
# TEXT SPLITTER
# -----------------------------
def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    return splitter.split_documents(documents)

# -----------------------------
# VECTOR STORE
# -----------------------------
def create_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},

    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore

# -----------------------------
# PROCESS PDFS
# -----------------------------
def process_pdfs(pdf_files):

    raw_text = read_pdf(pdf_files)

    chunks = split_text(raw_text)

    vectorstore = create_vectorstore(chunks)

    return vectorstore


# -----------------------------
# PROMPT
# -----------------------------
prompt = ChatPromptTemplate.from_template(
"""
You are an Enterprise Knowledge Assistant.

Answer ONLY from the provided context.

If the answer is not present inside the context say:

"I couldn't find this information in the uploaded documents."

Context:

{context}

Question:

{question}

Answer:
"""
)


# -----------------------------
# FORMAT DOCUMENTS
# -----------------------------
def format_docs(docs):
    formatted_docs = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        formatted_docs.append(
            f"Source: {source}, Page: {page}\n{doc.page_content}"
        )

    return "\n\n".join(formatted_docs)
# -----------------------------
# BUILD RAG CHAIN
# -----------------------------
def build_rag_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    def retrieve_and_answer(question):
        docs = retriever.invoke(question)

        context = format_docs(docs)

        messages = prompt.invoke({
            "context": context,
            "question": question
        })

        answer = llm.invoke(messages)

        return {
            "answer": StrOutputParser().invoke(answer),
            "sources": docs
        }

    return retrieve_and_answer