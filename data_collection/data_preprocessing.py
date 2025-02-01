# import pandas as pd
# #1ST STEP: THIS DELETE ALL NEUTRAL POST
#
# # Load the CSV file
# df = pd.read_csv('tesla_multi_subreddit_posts_year2024_with_sentiment.csv')
#
# # Remove neutral sentiment posts
# df_filtered = df[df['sentiment'] != 'neutral']
#
# # Save the filtered data back to the original CSV file, overwriting it
# df_filtered.to_csv('tesla_multi_subreddit_posts_year2024_with_sentiment.csv', index=False)
#
# # Print confirmation message
# print("Neutral posts have been removed and the file has been updated.")


## 2nd STEP: THIS IS TO CALCULATE THE DAILY SENTIMENT OF EACH PLATFORM AFTER USING LLM
# import pandas as pd
# def calculate_daily_sentiment(df):
#     # Count positive and negative posts for each day
#     pos_posts = len(df[df['sentiment'] == 'positive'])
#     neg_posts = len(df[df['sentiment'] == 'negative'])
#
#     # Calculate sentiment score using the formula
#     if (pos_posts + neg_posts) > 0:
#         sentiment_score = ((pos_posts - neg_posts) / (pos_posts + neg_posts)) * 100
#     else:
#         sentiment_score = 0
#
#     return sentiment_score
#
#
# df = pd.read_csv('mastodon_tesla_posts_year2024_with_sentiment.csv')
#
# # Convert created_utc to datetime
# df['date'] = pd.to_datetime(df['created_utc'], format='%m-%d-%Y').dt.date
#
# # Calculate daily sentiment scores using groupby
# daily_sentiment = df.groupby('date').apply(calculate_daily_sentiment).reset_index()
# daily_sentiment.columns = ['date', 'sentiment_score']
#
# # Save results
# daily_sentiment.to_csv('reddit_daily_sentiment_scores.csv', index=False)
# print("Daily sentiment scores have been calculated and saved.")


# #3RD STEP: THIS IS FOR COMBINING THE REDDIT,MATSODON SENTIMENT SCORE AND THE CLOSING PRICE FILES INTO 1 FILE
# TO MAKE IT EASIER TO ANALYZE
# import pandas as pd
#
# # Read the CSV files.
# mastodon_df = pd.read_csv('mastodon_daily_sentiment_scores.csv')
# reddit_df = pd.read_csv('reddit_daily_sentiment_scores.csv')
# tesla_df = pd.read_csv('tesla_closing_prices_modified.csv')
#
# # Convert the date formats to ensure they align correctly.
# mastodon_df['date'] = pd.to_datetime(mastodon_df['date'])
# reddit_df['date'] = pd.to_datetime(reddit_df['date'])
# tesla_df['Date'] = pd.to_datetime(tesla_df['Date'], format='%m-%d-%Y')
#
# # Rename columns for consistency
# tesla_df.rename(columns={'Date': 'date', 'Close': 'tesla_close'}, inplace=True)
#
# # Combine the dataframes on the date column.
# combined_df = pd.merge(mastodon_df, reddit_df, on='date', how='outer')
# combined_df = pd.merge(combined_df, tesla_df, on='date', how='outer')
#
# # Sort the combined dataframe by date.
# combined_df = combined_df.sort_values(by='date').reset_index(drop=True)
#
# # Save the combined DataFrame to a new CSV file.
# output_file_path = 'combined_sentiment_and_prices.csv'
# combined_df.to_csv(output_file_path, index=False)
#
# print(combined_df.head())



# #4TH STEP: THIS CALCULATE THE COMBINED SENTIMENT OF REDDIT AND MATSODON
# import pandas as pd
#
# # Load the CSV file
# df = pd.read_csv('combined_sentiment_and_prices.csv')
# df['sentiment_score_y'] = df['sentiment_score_y'].fillna(0)
# # Calculate the new column
# df['combined_sentiment'] = 0.7 * df['sentiment_score_x'] + 0.3 * df['sentiment_score_y']
#
# # Display the first few rows to verify the calculation
# print(df.head())
#
# # Save the modified DataFrame back to CSV
# df.to_csv('modified_sentiment_and_prices.csv', index=False)


## 5TH STEP: THIS REMOVE THE DAY THAT DON'T HAVE A PRICE FROM THE CLOSING PRICE COLLUMN
# import pandas as pd
#
# # Load the CSV file
# file_path = 'modified_sentiment_and_prices.csv'
# df = pd.read_csv(file_path)
#
# # Remove rows where 'combined_sentiment' is NaN (not available)
# df_cleaned = df.dropna(subset=['tesla_close'])
# df_cleaned = df_cleaned.dropna(subset=["combined_sentiment"])
# # Save the cleaned DataFrame to a new CSV file
# output_file_path = 'cleaned_sentiment_and_prices.csv'
# df_cleaned.to_csv(output_file_path, index=False)

