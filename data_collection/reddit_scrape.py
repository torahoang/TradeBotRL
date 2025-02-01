import praw
import pandas as pd
from datetime import datetime, timezone
# Authenticate with Reddit
reddit = praw.Reddit(
    client_id="wefwefew",
    client_secret="qefq",
    user_agent="34123"
)
posts_count = 0
# Set up the date range
start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)

# List of subreddits to search
subreddits = ["wallstreetbets", "StocksAndTrading", "investing", "stockmarket","dividends","options", "Daytrading"
              ,"Trading","politics","TeslaLounge","electricvehicles","technology", "StockMarket",
              "teslamotors","RealTesla", "CyberStuck", "RealTesla"]

data = []

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search("tesla", sort="new", limit=None)
    for post in posts:
        post_date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
        formatted_post_date = post_date.strftime('%m-%d-%Y')
        self_text = post.selftext
        if start_date <= post_date <= end_date:
            if post.selftext.startswith(('http://', 'https://')):
                self_text = ""
            content = post.title + self_text
            if len(content) < 10:
                continue
            data.append({
                "content_reddit": content,
                "created_utc": formatted_post_date
            })
            print(f"Post from r/{subreddit_name} on {post_date.date()} added")
            posts_count += 1
        elif post_date < start_date:
            break  # Stop if we've gone past our date range

df = pd.DataFrame(data)
df.head()
df.to_csv('tesla_multi_subreddit_posts.csv', index=False)
print(f"Tesla-related posts from {start_date.date()} to {end_date.date()} across multiple subreddits saved to tesla_multi_subreddit_posts_year2022_now.csv!")
print(f"total post {posts_count}")