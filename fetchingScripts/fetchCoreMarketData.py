import yfinance as yf
import pandas as pd

def fetch_core_market_data(ticker:str, start_date:str, end_date:str) -> pd.DataFrame:
    stock = yf.Ticker(ticker) 
    df = stock.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    
    return df
    
# Testing block
if __name__ == "__main__":
    df_core = fetch_core_market_data("AAPL", "2023-12-31", "2025-01-01")
    print(df_core.head())
    df_core.to_csv("core_market_data_AAPL.csv", index=False)