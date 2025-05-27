import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser

# def scrape_yahoo_finance_news(ticker: str) -> pd.DataFrame:
#     url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
#     headers = {
#         "User-Agent": "Mozilla/5.0"  # Mimic a real browser so that the site doesnt block the script thinking its a bot
#     }

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
#     news_items = soup.find_all("h3", class_="clamp  yf-1y7058a")  # Find headline containers (Yahoo Finance uses h3 and Mb(5px) as a standard for its headlines)
    
#     headlines: list[dict] = []
#     for item in news_items[:20]:  # Fetches the 20 latest headlines
#         link = item.find("a")
#         if link:
#             headline = link.text.strip()
#             article_url = "https://finance.yahoo.com" + link['href']
#             headlines.append({"headline": headline, "url": article_url})

#     return pd.DataFrame(headlines)

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
    