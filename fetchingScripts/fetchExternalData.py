import pandas as pd
import feedparser

def scrape_yahoo_finance_news(ticker: str) -> pd.DataFrame:
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)
    keywords = {"apple", "aapl"}
    headlines = []
    
    for entry in feed.entries:
        title_lower = entry.title.lower()
        if any(keyword in title_lower for keyword in keywords):
            headlines.append({"headline": entry.title, "url": entry.link})

    return pd.DataFrame(headlines)

# Testing block
if __name__ == "__main__":
    news_data = scrape_yahoo_finance_news("AAPL")
    print(news_data.head())
    news_data.to_csv("news_data_AAPL.csv", index=False)
    