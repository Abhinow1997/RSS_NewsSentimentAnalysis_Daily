import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('news_data_2024-11-11.csv')

st.title("RSS Feed News Sentiment Analysis Dashboard")

# Display basic stats
st.write(f"Total articles for the day : {len(df)}")
# st.write(f"Date range: {df['pub_date'].min()} to {df['pub_date'].max()}")

# Distribution of articles by broadcaster
st.subheader("Articles by Broadcaster")
broadcaster_counts = df['broadcast'].value_counts()

# Plotting the bar chart using Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(broadcaster_counts.index, broadcaster_counts.values)
ax.set_title("Article Counts by Broadcaster")
ax.set_xlabel("Broadcaster")
ax.set_ylabel("Number of Articles")
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)

# Display recent articles in a table
st.subheader("Recent Articles")
st.dataframe(df[['broadcast', 'title', 'pub_date', 'title_sentiment_score']].head(10))

# Show average sentiment scores by broadcaster (the chart you generated)
st.subheader("Average Sentiment Scores by Broadcaster")

# Plotting average sentiment scores using Matplotlib
avg_sentiment = df.groupby('broadcast')[['title_sentiment_score', 'description_sentiment_score']].mean()

fig, ax = plt.subplots(figsize=(8, 5))
avg_sentiment.plot(kind='bar', ax=ax)
ax.axhline(0, color='red', linestyle='--')  # Add a horizontal line at 0 for neutral sentiment
ax.set_title("Average Sentiment Scores by Broadcaster")
ax.set_xlabel("Broadcaster")
ax.set_ylabel("Average Sentiment Score")
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)

# Additional features could include filters for date or broadcaster, etc.