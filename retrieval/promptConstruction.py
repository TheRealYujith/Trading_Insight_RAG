from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

embedding_model = SentenceTransformer("yiyanghkust/finbert-tone")

# Load previously saved collection
chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="apple_market_data_finbert")
    
def prompt_construction(query: str, top_k: int = 5) -> str:
    query_embedding = embedding_model.encode(query).tolist()
    
    # Retrieve relevant chunks from ChromaDB
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    
    # Check if any documents were returned
    if not results['documents'][0]:
        return f"""No relevant context found. Unable to answer the question: {query}"""
    
    relevant_chunks = [doc for doc in results['documents'][0]]
    
    # Prompt construction
    context = "\n".join(relevant_chunks)
    prompt = f"""You are a financial analyst AI. Use the following financial context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Answer:"""
    
    print ("Successfully constructed the prompt")
    
    return prompt