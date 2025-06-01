from sentence_transformers import SentenceTransformer
from typing import List, Dict
from datetime import datetime
import chromadb
import pandas as pd

def clean_metadata(metadata: Dict) -> Dict:
    cleaned = {}
    for k, v in metadata.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            cleaned[k] = v
        elif isinstance(v, (datetime, pd.Timestamp)):
            cleaned[k] = v.strftime("%Y-%m-%d")  # Or include time: "%Y-%m-%d %H:%M:%S"
        else:
            cleaned[k] = str(v)
    return cleaned

def embedd_and_store_in_chroma(chunks: List[Dict]):
    # Initialize ChromaDB client (local)
    chroma_client = chromadb.PersistentClient(path="./chroma_store")
    collection = chroma_client.get_or_create_collection(name="apple_market_data_finbert")

    texts = [" ".join(chunk["text"]) if isinstance(chunk["text"], list) else str(chunk["text"])for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [clean_metadata(chunk.get("metadata", {})) for chunk in chunks]
    
    # Load model and create embeddings
    model = SentenceTransformer("yiyanghkust/finbert-tone")
    embeddings = model.encode(texts).tolist()

    # Add to ChromaDB
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f" Successfully stored {len(chunks)} chunks in ChromaDB.")
