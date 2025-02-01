import pandas as pd
def calculate_daily_sentiment(df):
    # Count positive and negative posts for each day
    pos_posts = len(df[df['sentiment'] == 'positive'])
    neg_posts = len(df[df['sentiment'] == 'negative'])

    # Calculate sentiment score using the formula
    if (pos_posts + neg_posts) > 0:
        sentiment_score = ((pos_posts - neg_posts) / (pos_posts + neg_posts)) * 100
    else:
        sentiment_score = 0

    return sentiment_score


df = pd.read_csv('nvidia2024_reddit_with_sentiment.csv')

# Convert created_utc to datetime
df['date'] = pd.to_datetime(df['created_utc'], format='%m-%d-%Y').dt.date

# Calculate daily sentiment scores using groupby
daily_sentiment = df.groupby('date').apply(calculate_daily_sentiment).reset_index()
daily_sentiment.columns = ['date', 'sentiment_score']

# Save results
daily_sentiment.to_csv('nvidia2024_reddit_with_sentiment.csv', index=False)
print("Daily sentiment scores have been calculated and saved.")