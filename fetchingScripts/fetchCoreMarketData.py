import yfinance as yf
import pandas as pd

def fetch_core_market_data(ticker:str, start_date:str, end_date:str) -> pd.Dataframe:
    stock = yf.Ticker(ticker) 
    df = stock.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    
    return df
    