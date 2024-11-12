# RSS News Sentiment Analysis Dashboard



## Overview

This project creates a daily-updated dashboard analyzing sentiment in news articles from various broadcasters. It uses RSS feeds to collect news data, performs sentiment analysis, and visualizes the results using a Streamlit web application.

## Pipeline

1. **Data Collection**
   - Script: `rss_datacollection_feed.py`
   - Fetches news articles from RSS feeds of multiple broadcasters (BBC, NYC Times, CBS News, Aljazeera, The Guardian)
   - Uses `requests` library to fetch RSS data
   - Parses XML data using `xml.etree.ElementTree`

2. **Sentiment Analysis**
   - Utilizes VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment scoring
   - Calculates sentiment scores for both article titles and descriptions

3. **Data Processing**
   - Cleans HTML tags from descriptions
   - Removes duplicates
   - Saves processed data to a CSV file with a date stamp

4. **Automated Daily Updates**
   - Uses GitHub Actions for daily execution of the data collection script
   - Workflow defined in `.github/workflows/daily_data_collection.yml`
   - Automatically commits and pushes updated data to the repository

5. **Visualization**
   - Script: `app.py`
   - Creates a Streamlit dashboard
   - Visualizations include:
     - Article count by broadcaster
     - Average sentiment scores
     - Publication time distribution
     - Sentiment distribution pie charts

6. **Deployment**
   - Hosted on Streamlit Cloud
   - Automatically updates with the latest data

## Key Features

- Daily automated data collection and analysis
- Sentiment analysis of news articles from multiple sources
- Interactive web dashboard for data exploration
- Version-controlled data storage using GitHub

## Technologies Used

- Python
- Pandas for data manipulation
- VADER for sentiment analysis
- Matplotlib for creating charts
- Streamlit for web application
- GitHub Actions for automation

## Setup and Running

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run data collection: `python rss_datacollection_feed.py`
4. Launch Streamlit app: `streamlit run app.py`

## Data Update Process

The data is automatically updated daily through a GitHub Actions workflow. This ensures that the dashboard always displays the most recent news sentiment analysis.

## Dashboard Access

The live dashboard can be accessed at (link)[https://rssnewssentimentanalysisdaily.streamlit.app].
---