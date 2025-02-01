# Import necessary libraries
import pandas as pd
from stable_baselines3 import PPO
from RLbot import TradingEnv  # Assuming your TradingEnv class is in a separate file

# Load market data (same or new dataset)
df = pd.read_csv('filtered_data.csv')

# Initialize the trading environment
env = TradingEnv(df)

# Load the trained PPO model
model = PPO.load("rl_sentiment_closing_price_bot")

# Reset the environment
obs, _ = env.reset()

done = False
while not done:
    # Use the model to predict an action
    action, _states = model.predict(obs)

    # Take the action in the environment
    obs, reward, terminated, truncated, info = env.step(action)

    # Check if the episode is over
    done = terminated or truncated

    # Optionally print or log results
    print(f"Action: {action}, Reward: {reward}, Portfolio Value: {env.total_portfolio}")

# Print final portfolio value and cash remaining
print(f"Final Portfolio Value: {env.total_portfolio}")
print(f"Cash Remaining: {env.cash}")
print(f"Shares Owned: {env.shares_owned}")
