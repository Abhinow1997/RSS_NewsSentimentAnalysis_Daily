import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# New Broadcasters Newsfeeds:
bbc_url = "http://feeds.bbci.co.uk/news/rss.xml"  
nytimes_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
cbsnews_url = "https://www.cbsnews.com/latest/rss/world"
aljazeera_url = "https://www.aljazeera.com/xml/rss/all.xml"
theguardian_url = "https://www.theguardian.com/uk/rss"

url_linkers = [
    (bbc_url, "BBC"),
    (nytimes_url, "NYC Times"),
    (cbsnews_url, "CBS News"),
    (aljazeera_url, "Aljazeera"),
    (theguardian_url, "The Guardian")
]

# Function to fetch and parse RSS feeds
def get_newsfeed(url, broadcast):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    items = root.findall('.//item')
    
    news_data = []
    for item in items:
        title = item.find('title').text if item.find('title') is not None else ""
        description = item.find('description').text if item.find('description') is not None else ""
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
        
        news_data.append({
            'broadcast': broadcast,
            'title': title,
            'description': description,
            'pub_date': pub_date
        })
    
    return pd.DataFrame(news_data)

# Function to calculate VADER sentiment
def calculate_sentiment_vader(text):
    scores = analyzer.polarity_scores(text)
    return scores['compound']

# Function to clean HTML tags
def clean_html(text):
    return re.sub('<.*?>', '', text) if text else ''

# Main function
def main():
    # Fetch and combine news data
    all_news = []
    for url, broadcast in url_linkers:
        print(f"News feed from: {broadcast}")
        df_url = get_newsfeed(url, broadcast)
        cnt = len(df_url)
        print(f"Collected Articles: {cnt}")
        all_news.append(df_url)

    df_combined = pd.concat(all_news, ignore_index=True)
    print(f"\nTotal articles collected: {len(df_combined)}")

    # Title Sentiment Calculation
    df_combined['title_sentiment_score'] = df_combined['title'].apply(calculate_sentiment_vader)

    # Description Sentiment Calculation
    df_combined['description_sentiment_score'] = df_combined['description'].apply(calculate_sentiment_vader)

    # Remove duplicates
    df_combined = df_combined.drop_duplicates()

    # Clean HTML from description
    df_combined['description'] = df_combined['description'].apply(clean_html)

    # Save to CSV with date stamp
    today = date.today().strftime("%Y-%m-%d")
    filename = f"news_data.csv"
    df_combined.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()