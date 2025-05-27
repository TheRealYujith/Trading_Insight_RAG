import yfinance as yf
import pandas as pd

def fetch_fundamental_data(ticker: str) -> dict:
    # dict is used as there are multiple dataframes
    stock = yf.Ticker(ticker)
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    income_statement = stock.income_stmt
    
    return {
        # .T is used to swap rows to columns and vice versa
        # .reset_index() is used so the dates are now a column rather than the index
        "financials": financials.T.reset_index(),  
        "balance_sheet": balance_sheet.T.reset_index(),
        "income_statement": income_statement.T.reset_index()
    }
    
# Testing block
if __name__ == "__main__":
    fundamental_data = fetch_fundamental_data("AAPL")
    fundamental_data["financials"].to_csv("fundamentals_financials_AAPL.csv", index=False)
    fundamental_data["balance_sheet"].to_csv("fundamentals_balance_sheet_AAPL.csv", index=False)
    fundamental_data["income_statement"].to_csv("fundamentals_income_statement_AAPL.csv", index=False)