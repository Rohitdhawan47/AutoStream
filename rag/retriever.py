def retrieve_context(vector_store, query: str) -> str:
    results = vector_store.similarity_search_with_score(query, k=3)

    if not results:
        return ""

    # Sort by best score (lowest distance = best match)
    results.sort(key=lambda x: x[1])

    best_doc, best_score = results[0]

    # print("DEBUG BEST SCORE:", best_score)
    # print("DEBUG BEST CHUNK:", best_doc.page_content)

    return best_doc.page_content
