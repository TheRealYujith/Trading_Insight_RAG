import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_yahoo_finance_news(ticker: str) -> pd.DataFrame:
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0"  # Mimic a real browser so that the site doesnt block the script thinking its a bot
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.find_all("h3", class_="Mb(5px)")  # Find headline containers (Yahoo Finance uses h3 and Mb(5px) as a standard for its headlines)

    headlines: list[dict] = []
    for item in news_items[:20]:  # Fetches the 20 latest headlines
        link = item.find("a")
        if link:
            headline = link.text.strip()
            article_url = "https://finance.yahoo.com" + link['href']
            headlines.append({"headline": headline, "url": article_url})

    return pd.DataFrame(headlines)
