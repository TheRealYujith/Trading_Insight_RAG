from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load previously saved collection
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="./chroma_store"))
collection = chroma_client.get_collection(name="apple_market_data")
    
def prompt_construction(query: str, top_k: int = 5) -> str:
    query_embedding = embedding_model.encode(query).tolist()
    
    # Retrieve relevant chunks from ChromaDB
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    relevant_chunks = [doc for doc in results['documents'][0]]
    
    # Prompt construction
    context = "\n".join(relevant_chunks)
    prompt = f"""Use the following financial context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Answer:"""
    
    return prompt