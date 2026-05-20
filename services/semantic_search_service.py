import chromadb

from sentence_transformers import (
    SentenceTransformer
)


# ----------------------------------------
# ChromaDB Client
# ----------------------------------------

client = chromadb.PersistentClient(
    path="database"
)

collection = client.get_or_create_collection(
    name="engineering_tools"
)


# ----------------------------------------
# Embedding Model
# ----------------------------------------

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)


# ----------------------------------------
# Search Engineering Tools
# ----------------------------------------

def search_tools(
    query,
    top_k=2
):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=10

    )

    filtered_results = []

    query_lower = query.lower()

    important_terms = query_lower.split()

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for document, metadata in zip(
        documents,
        metadatas
    ):

        document_lower = document.lower()

        relevance_score = 0

        for term in important_terms:

            if term in document_lower:

                relevance_score += 1

        if relevance_score >= 2:

            filtered_results.append({

                "document": document,
                "metadata": metadata

            })

    return filtered_results[:top_k]