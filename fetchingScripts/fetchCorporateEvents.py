import yfinance as yf
import pandas as pd

def fetch_corporate_events(ticker: str, start_date: str, end_date: str) -> dict:
    stock = yf.Ticker(ticker)
    dividends = stock.dividends.loc[start_date:end_date].reset_index()
    splits = stock.splits.loc[start_date:end_date].reset_index()
    earnings = stock.income_stmt.T.reset_index() # Annual earnings
    
    # Handling calendar when its a dict or dataframe
    calendar_raw = stock.calendar
    if isinstance(calendar_raw, pd.DataFrame):
        calendar = calendar_raw.T.reset_index()
    elif isinstance(calendar_raw, dict):
        calendar = pd.DataFrame(calendar_raw.items(), columns=["Event", "Date"])
    else:
        calendar = pd.DataFrame()

    return {
        "dividends": dividends,
        "splits": splits,
        "earnings": earnings,
        "calendar": calendar
    }
    
# Example usage
if __name__ == "__main__":
    corporate_events_data = fetch_corporate_events("AAPL", "2023-12-31", "2025-01-01")
    corporate_events_data["dividends"].to_csv("corporate_dividends_AAPL.csv", index=False)
    corporate_events_data["splits"].to_csv("corporate_splits_AAPL.csv", index=False)
    corporate_events_data["earnings"].to_csv("corporate_earnings_AAPL.csv", index=False)
    corporate_events_data["calendar"].to_csv("corporate_calendar_AAPL.csv", index=False)