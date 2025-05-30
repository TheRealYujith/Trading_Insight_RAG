import pandas as pd
from typing import List, Dict
import uuid

def preprocess_core_market_data(df: pd.DataFrame) -> pd.DataFrame:
   df['daily_return'] = df['close'].pct_change() # Close percentage change
   df['ma_5'] = df['close'].rolling(window=5).mean() # Moving average for short term trends
   df['ma_20'] = df['close'].rolling(window=20).mean() # Moving average for long term trends
   df['volatility_20'] = df['daily_return'].rolling(window=20).std() # Volatility gives the price variability over a period
   return df

def core_market_data_to_text(df: pd.DataFrame) -> List[Dict]:
    market_data_chunks = []
    # Convert each row into a descriptive sentence
    for _, row in df.iterrows():
        sentence = (
            f"On {row['date']}, AAPL opened at ${row['open']:.2f}, "
            f"reached a high of ${row['high']:.2f}, a low of ${row['low']:.2f}, "
            f"and closed at ${row['close']:.2f}, with a volume of "
            f"{row['volume'] / 1_000_000:.1f} million shares traded. "
            f"The close percentage change was %{row['daily_return']:.2f}, "
            f"with a 5 day moving average of ${row['ma_5']:.2f} and 20 day moving average of ${row['ma_20']:.2f}. "
            f"Volatility for a 20 day period is ${row['volatility_20']:.2f}."
        )
        market_data_chunks.append({
            "id": str(uuid.uuid4()),
            "text": sentence,
            "metadata": {
                "source": "core_market_data",
                "date": row["date"],
                "ticker": "AAPL"
            }
        })
        
    return market_data_chunks 

def fundamentals_balance_sheet_to_text(df: pd.DataFrame) -> List[Dict]:
    balance_sheet_chunks = []

    for _, row in df.iterrows():
        lines = []
        
        for col in df.columns:
            if col != "date":
                value = row[col]
                key = col.replace("_", " ").title() # Clean key formatting ("ordinary_shares_number" -> "Ordinary Shares Number")
                if pd.notnull(value):
                    lines.append(f"{key}: {value}")
                else:
                    lines.append(f"{key}: Not available")

        balance_sheet_chunks.append({
            "id": str(uuid.uuid4()),
            "text": lines,
            "metadata": {
                "source": "balance_sheet_data",
                "date": row["date"],
                "ticker": "AAPL"
            }
        })

    return balance_sheet_chunks

def fundamentals_financials_to_text(df: pd.DataFrame) -> list[str]:
    financial_chunks = []

    for _, row in df.iterrows():
        lines = []
        
        for col in df.columns:
            if col != "date":
                value = row[col]
                key = col.replace("_", " ").title() # Clean key formatting ("ordinary_shares_number" -> "Ordinary Shares Number")
                if pd.notnull(value):
                    lines.append(f"{key}: {value}")
                else:
                    lines.append(f"{key}: Not available")

        financial_chunks.append({
            "id": str(uuid.uuid4()),
            "text": lines,
            "metadata": {
                "source": "financial_data",
                "date": row["date"],
                "ticker": "AAPL"
            }
        })

    return financial_chunks