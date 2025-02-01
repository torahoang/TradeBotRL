import pandas as pd

# Read the CSV file
df = pd.read_csv('modified_sentiment_and_prices.csv')

# Normalize the sentiment_score to range -1 to 1
df['sentiment_score'] = df['sentiment_score'] / 100.0

# Save the updated DataFrame to a new CSV file
df.to_csv('normalized_sentiment_and_prices.csv', index=False)

# Display the first few rows to verify
print(df.head())

# Verify the range of sentiment_score
print("\nVerification:")
print("Sentiment score range:", df['sentiment_score'].min(), "to", df['sentiment_score'].max())
