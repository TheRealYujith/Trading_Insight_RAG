import pandas as pd

# Clean Core Market data
def clean_core_market_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna(axis=1, how='all') # Drop columns that hold entirely NaN values
    df = df.loc[:, df.nunique(dropna=False) > 1] # Drop columns that hold the same value across all records
    df = df.dropna(subset=["close"])
    return df
    
# Clean Fundamental data
def clean_fundamental_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    if 'index' in df.columns:
        df = df.rename(columns={'index': 'date'})
        
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(axis=1, how='all') # Drop columns that hold entirely NaN values
    threshold = int(df.shape[1] * 0.5) # Drop rows with more than 50% missing values
    df = df.dropna(thresh=threshold)
    df = df.loc[:, df.nunique(dropna=False) > 1] # Drop columns that hold the same value across all records
    df = df.fillna("N/A") # Replace NaNs with "N/A"
    return df
    
# Clean External News data
def clean_external_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df['headline'] = df['headline'].str.strip().str.lower()
    return df