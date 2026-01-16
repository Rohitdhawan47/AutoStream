from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vector_store():
    with open("knowledge_base/autostream_docs.txt", "r") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    # ✅ LOCAL embeddings (NO API calls)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store
