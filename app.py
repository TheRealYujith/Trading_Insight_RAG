import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
import asyncio
from fetchingScripts.fetchCoreMarketData import fetch_core_market_data
from fetchingScripts.fetchFundamentalData import fetch_fundamental_data
from preprocessing.cleaning import clean_core_market_data, clean_fundamental_data
from preprocessing.formatting import (
    preprocess_core_market_data,
    core_market_data_to_text,
    fundamentals_balance_sheet_to_text,
    fundamentals_financials_to_text,
)
from preprocessing.embeddings import embedd_and_store_in_chroma
from retrieval.promptConstruction import prompt_construction
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
        
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Cache model load and ChromaDB initialization
@st.cache_resource
def load_model():
    hf_hub_download(
        repo_id="QuantFactory/finance-Llama3-8B-GGUF",
        filename="finance-Llama3-8B.Q4_K_M.gguf",
        local_dir="./models"
    )
    return Llama(
        model_path="./models/finance-Llama3-8B.Q4_K_M.gguf",
        n_ctx=8192,
        n_threads=os.cpu_count() or 4
    )

st.title("📈 Trading Insight Generator (LLM + RAG)")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="AAPL")
query = st.text_area("Enter your question", value="What are the financial insights for Apple in 2024?")
generate_button = st.button("Generate Insights")

if generate_button and ticker and query:
    with st.spinner("Fetching and processing data..."):
        try:
            # Fetch and clean data
            core_market_df = clean_core_market_data(
                fetch_core_market_data(ticker, "2023-12-31", "2025-01-01")
            )
            fundamentals = fetch_fundamental_data(ticker)
            balance_sheet_df = clean_fundamental_data(fundamentals["balance_sheet"])
            financials_df = clean_fundamental_data(fundamentals["financials"])

            # Preprocess
            preprocessed_core_market_df = preprocess_core_market_data(core_market_df)
            core_market_list = core_market_data_to_text(preprocessed_core_market_df)
            balance_sheet_list = fundamentals_balance_sheet_to_text(balance_sheet_df)
            financials_list = fundamentals_financials_to_text(financials_df)
            all_chunks = core_market_list + balance_sheet_list + financials_list

            # Embed and store
            embedd_and_store_in_chroma(all_chunks)

            # Prompt construction
            prompt = prompt_construction(query)

            # LLM response
            llm = load_model()
            response = llm(prompt, max_tokens=512)

            st.subheader("📊 Insight")
            st.write(response['choices'][0]['text'].strip() if isinstance(response, dict) else response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
