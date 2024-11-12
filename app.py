import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('news_data.csv')

# Convert pub_date to datetime
df['pub_date'] = pd.to_datetime(df['pub_date'], format='mixed', utc=True)

# Find the most common publication date
most_common_date = df['pub_date'].dt.date.mode().iloc[0].strftime('%Y-%m-%d')

# Set page title and configuration
st.set_page_config(page_title="RSS Feed News Sentiment Analysis", layout="wide")

# Main title with most common publication date
st.title(f"RSS Feed News Sentiment Analysis Dashboard - {most_common_date}")

# Display basic stats
st.header("Overview")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Articles", len(df))
with col2:
    st.metric("Date Range", f"{df['pub_date'].min().date()} to {df['pub_date'].max().date()}")

# Distribution of articles by broadcaster
st.header("Article Distribution by Broadcaster")
broadcaster_counts = df['broadcast'].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(broadcaster_counts.index, broadcaster_counts.values, color='skyblue')
ax.set_title("Article Counts by Broadcaster", fontsize=16)
ax.set_xlabel("Broadcaster", fontsize=12)
ax.set_ylabel("Number of Articles", fontsize=12)
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(broadcaster_counts.values):
    ax.text(i, v, str(v), ha='center', va='bottom')
st.pyplot(fig)

# Display recent articles in a table
st.header("Recent Articles")
st.dataframe(df[['broadcast', 'title', 'pub_date', 'title_sentiment_score']].head(10), use_container_width=True)

# Average Sentiment Scores by Broadcaster
st.header("Average Sentiment Scores by Broadcaster")
avg_sentiment = df.groupby('broadcast')[['title_sentiment_score', 'description_sentiment_score']].mean()

fig, ax = plt.subplots(figsize=(12, 6))
avg_sentiment.plot(kind='bar', ax=ax)
ax.axhline(0, color='red', linestyle='--')
ax.set_title("Average Sentiment Scores by Broadcaster", fontsize=16)
ax.set_xlabel("Broadcaster", fontsize=12)
ax.set_ylabel("Average Sentiment Score", fontsize=12)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Histogram of Publication Times
st.header("Publication Time Distribution")
latest_feed_data_df = df.copy()
latest_feed_data_df['hour'] = latest_feed_data_df['pub_date'].dt.hour

fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(latest_feed_data_df['hour'], bins=24, color='#5EBD89', edgecolor='black')
ax.set_xlabel('Hour of the Day', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Histogram of Publication Times', fontsize=16)
st.pyplot(fig)

# Add predicted sentiment columns
latest_feed_data_df['title_predicted_sentiment'] = latest_feed_data_df['title_sentiment_score'].apply(
    lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
latest_feed_data_df['description_predicted_sentiment'] = latest_feed_data_df['description_sentiment_score'].apply(
    lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Function to create pie charts for sentiment distribution
def create_sentiment_pie_charts(data, sentiment_column, title):
    broadcasters = data['broadcast'].unique()
    color_map = {
        'Positive': '#5EBD89',
        'Negative': '#FF8680',
        'Neutral': '#EBDE96'
    }
    
    fig, axes = plt.subplots(nrows=(len(broadcasters)+1)//2, ncols=2, figsize=(15, 5*((len(broadcasters)+1)//2)))
    fig.suptitle(title, fontsize=20)
    axes = axes.flatten()

    for i, broadcaster in enumerate(broadcasters):
        broadcaster_data = data[data['broadcast'] == broadcaster]
        sentiment_counts = broadcaster_data[sentiment_column].value_counts()
        for sentiment in color_map.keys():
            if sentiment not in sentiment_counts.index:
                sentiment_counts[sentiment] = 0
        sentiment_counts = sentiment_counts.sort_index()
        colors = [color_map[sentiment] for sentiment in sentiment_counts.index]    
        axes[i].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=20, colors=colors)
        axes[i].set_title(f'{broadcaster}', fontsize=14)
    
    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    st.pyplot(fig)

# Create pie charts for title sentiment distribution by broadcaster
st.header("Sentiment Distribution by Broadcaster")
create_sentiment_pie_charts(latest_feed_data_df, 'title_predicted_sentiment', 'Distribution of Title Sentiment by Broadcaster')

# Create pie charts for description sentiment distribution by broadcaster
create_sentiment_pie_charts(latest_feed_data_df, 'description_predicted_sentiment', "Distribution of Article's Description Sentiment by Broadcaster")