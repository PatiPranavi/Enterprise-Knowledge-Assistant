import streamlit as st
from dotenv import load_dotenv

from rag import process_pdfs, build_rag_chain

load_dotenv()

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Enterprise Knowledge Assistant")
st.write("Upload multiple PDFs and chat with your documents.")

if "chain" not in st.session_state:
    st.session_state.chain = None

with st.sidebar:

    st.header("Upload PDFs")

    pdf_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("Process Documents"):

        if not pdf_files:
            st.warning("Please upload at least one PDF.")
            st.stop()

        with st.spinner("Building Knowledge Base..."):

            vectorstore = process_pdfs(pdf_files)

            st.session_state.chain = build_rag_chain(vectorstore)

        st.success("Knowledge Base Created ✅")

question = st.chat_input("Ask a question...")

if question:

    if st.session_state.chain is None:
        st.warning("Please upload PDFs first.")
        st.stop()

    with st.chat_message("user"):
        st.write(question)

    result = st.session_state.chain(question)

    with st.chat_message("assistant"):
        st.write(result["answer"])

        st.markdown("**Sources:**")

        shown_sources = set()

        for doc in result["sources"]:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "Unknown")
            source_key = (source, page)

            if source_key not in shown_sources:
                st.write(f"📄 {source} — Page {page}")
                shown_sources.add(source_key)