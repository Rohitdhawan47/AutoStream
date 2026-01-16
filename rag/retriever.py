def retrieve_context(vector_store, query: str) -> str:
    docs = vector_store.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])
