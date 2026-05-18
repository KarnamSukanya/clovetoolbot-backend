import chromadb

from sentence_transformers import SentenceTransformer


# ----------------------------------------
# ChromaDB Connection
# ----------------------------------------

client = chromadb.PersistentClient(
    path="database"
)

collection = client.get_collection(
    name="engineering_tools"
)


# ----------------------------------------
# Embedding Model
# ----------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ----------------------------------------
# Semantic Search
# ----------------------------------------

def search_tools(user_query, top_k=3):

    query_embedding = embedding_model.encode(
        user_query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return documents