
import os
from typing import List

from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# -----------------------------
# PDF READER
# -----------------------------
def read_pdf(files):

    text = ""

    for pdf in files:

        reader = PdfReader(pdf)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -----------------------------
# TEXT SPLITTER
# -----------------------------
def split_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200,

        separators=["\n\n", "\n", " ", ""]
    )

    return splitter.split_text(text)


# -----------------------------
# VECTOR STORE
# -----------------------------
def create_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},

    )

    vectorstore = FAISS.from_texts(
        texts=chunks,
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

    return "\n\n".join(doc.page_content for doc in docs)


# -----------------------------
# BUILD RAG CHAIN
# -----------------------------
def build_rag_chain(vectorstore):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain