# def retrieve_context(vector_store, query: str, threshold: float = 1.8) -> str:
#     """
#     Returns relevant context only if similarity is strong enough.
#     Prevents garbage retrieval and hallucination.
#     """
#     results = vector_store.similarity_search_with_score(query, k=2)

#     good_chunks = []
#     for doc, score in results:
#         print("DEBUG SCORE:", score)
#         print("DEBUG CHUNK:", doc.page_content)
#         # FAISS score = distance (lower is better)
#         if score <= threshold:
#             good_chunks.append(doc.page_content)

#     return "\n".join(good_chunks)
def retrieve_context(vector_store, query: str) -> str:
    results = vector_store.similarity_search_with_score(query, k=3)

    if not results:
        return ""

    # Sort by best score (lowest distance = best match)
    results.sort(key=lambda x: x[1])

    best_doc, best_score = results[0]

    print("DEBUG BEST SCORE:", best_score)
    print("DEBUG BEST CHUNK:", best_doc.page_content)

    return best_doc.page_content
