import pandas as pd
from transformers import pipeline

# Load the CSV file
df = pd.read_csv('tesla_multi_subreddit_posts_year2024.csv')

# Initialize the sentiment analysis pipeline
sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", device=0,
                          max_length=512, truncation=True)
post = 0
# Function to perform sentiment analysis and extract sentiment and score
def analyze_sentiment(text):
    global post
    print(post)
    result = sentiment_task(text)
    sentiment = result[0]['label']
    post = post + 1
    return sentiment

df['sentiment'] = df['content_reddit'].apply(analyze_sentiment)
# Save the updated DataFrame back to CSV
df.to_csv('tesla_multi_subreddit_posts_year2024_with_sentiment.csv', index=False)

print("Sentiment analysis complete. Results saved to 'tesla_multi_subreddit_posts_oct23_nov22_with_sentiment.csv'")