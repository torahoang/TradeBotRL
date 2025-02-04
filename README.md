# TradeBotRL - Smarter Trading Decisions, Simplified 📈🤖

TradeBot is a reinforcement learning-powered trading assistant designed to help users make informed and optimized trading decisions. By leveraging sentiment analysis and market data, TradeBot dynamically adjusts buy and sell thresholds to maximize portfolio performance. This tool is ideal for traders seeking to integrate artificial intelligence into their strategies, offering insights based on real-time sentiment and price trends.


## How It is Built 👷

### Tech Stack 💻
- **Python** for backend development and reinforcement learning implementation.
- **Stable-Baselines3 PPO** for reinforcement learning model training.
- **Gymnasium** for creating a custom trading environment.
- **Pandas & NumPy** for data handling and preprocessing.
- **Sentiment Analysis Model**: Hugging Face's `twitter-roberta-base-sentiment-latest` for analyzing sentiment scores from social media data.

### How It Works 🧑‍🍳
1. **Data Collection**: 
   - Scrape Reddit posts using `reddit_scrape.py` or Mastodon posts with `mastodon_scraping.py`. Specify the start/end dates and subreddit or hashtag.
2. **Sentiment Analysis**:
   - Analyze collected posts with `sentiment_analysis.py`, which uses a pre-trained sentiment model to generate sentiment scores.
3. **Trading Strategy Implementation**:
   - The custom Gymnasium environment (`TradingEnv`) simulates trading decisions based on sentiment scores and market data (e.g., closing prices).
4. **Reinforcement Learning**:
   - Train a Proximal Policy Optimization (PPO) model to optimize buy/sell thresholds dynamically.
5. **Backtesting Framework**:
   - Use `backtesting_with_sentiment.py` to evaluate the basic performance, generating metrics and transaction logs.
   - use `testingRL.py` to evaluate automatic trade bot, generating action steps and final value 

### Usage 🍳
1. Prepare your dataset by running the scraping scripts (`reddit_scrape.py` or `mastodon_scraping.py`) and analyzing them with `sentiment_analysis.py`.
2. Train the PPO model using market data in `TradingEnv`.
3. Deploy the trained model to simulate trading or use it in real-world scenarios.

## How to Run the Program 💻

### Environment Setup
1. Clone the repository and navigate to the project folder.
2. Install required libraries:
```shell
> pip install -r requirements.txt
```

### Data collection
1. Use `reddit_scrape.py` and mastodon_scraping.py to collect post data from reddit and mastodon
2. Use `sentiment_analysis.py` to categorize the sentiment of each post content
3. Use `data_preprocessing.py` and necessary script to clean the data

### Train and test RL agent
1. Train the model by tesla stock data using the `RLbot.py` file, altering the timestep to train to your needs
2. Test the model by nvidia stock data using the `testingRL.py` file

### License 

`TradeBotRL` is licensed under MIT License. All development is currently maintain by [Hoang Quy Nguyen](https://github.com/torahoang).


### Disclaimer: Use this bot at your own risk

