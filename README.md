# Trading_Insight_RAG

This project generates real-time trading insights for cryptocurrency markets by analyzing news headlines and market data using a quantized large language model (LLM) and Retrieval-Augmented Generation (RAG) pipeline.

## Features
- Real-time data ingestion from Yahoo Finance and crypto news APIs
- Vector database (ChromaDB + FAISS) for efficient retrieval
- Quantized LLM (LLaMA or similar) via `llama-cpp-python` for local inference
- RAG pipeline for contextual insight generation
- Actionable output including key market movers and sentiment-driven takeaways

## Tech Stack
- Python 3.13
- [yfinance](https://pypi.org/project/yfinance/)
- [sentence-transformers](https://www.sbert.net/)
- [faiss-cpu](https://github.com/facebookresearch/faiss)
- [ChromaDB](https://www.trychroma.com/)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [requests](https://docs.python-requests.org/)