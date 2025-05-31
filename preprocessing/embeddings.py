from sentence_transformers import SentenceTransformer
from typing import List, Dict
import chromadb
from chromadb.config import Settings

def embedd_and_store_in_chroma(chunks: List[Dict]):
    # Initialize ChromaDB client (local)
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_store"))
    collection = chroma_client.get_or_create_collection(name="apple_market_data")

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [chunk.get("metadata", {}) for chunk in chunks]
    
    # Load model and create embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(texts).tolist()

    # Add to ChromaDB
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f" Successfully stored {len(chunks)} chunks in ChromaDB.")
