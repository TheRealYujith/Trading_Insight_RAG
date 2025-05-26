import yfinance as yf
import pandas as pd

def fetch_corporate_events(ticker: str, start_date: str, end_date: str) -> dict:
    stock = yf.Ticker(ticker)
    dividends = stock.dividends.loc[start_date:end_date].reset_index()
    splits = stock.splits.loc[start_date:end_date].reset_index()
    earnings = stock.earnings.reset_index()  # Annual earnings
    calendar = stock.calendar.T.reset_index()  # Upcoming events

    return {
        "dividends": dividends,
        "splits": splits,
        "earnings": earnings,
        "calendar": calendar
    }