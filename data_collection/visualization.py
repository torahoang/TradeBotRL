import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('cleaned_sentiment_and_prices.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Load the transaction log from the CSV file
transaction_log_df = pd.read_csv('transaction_log.csv')

# Convert the DataFrame to a list of tuples
transaction_log = list(transaction_log_df.itertuples(index=False, name=None))

plt.figure(figsize=(14, 8))

# Plot 1: Combined Sentiment Over Time
ax1 = plt.subplot(3, 1, 1)
df['combined_sentiment'].plot(ax=ax1, color='blue')
ax1.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
ax1.set_title('Combined Sentiment Over Time')
ax1.set_ylabel('Sentiment Score')
ax1.grid()

# Plot 2: Tesla Close Price Over Time
ax2 = plt.subplot(3, 1, 2)
df['tesla_close'].plot(ax=ax2, color='orange')
ax2.set_title('Tesla Close Price Over Time')
ax2.set_ylabel('Price ($)')
ax2.grid()

# Plot 3: Stock Price and Sentiment with Trading Decisions
ax3 = plt.subplot(3, 1, 3)
df['tesla_close'].plot(ax=ax3, label='Tesla Close Price', color='orange')
df['combined_sentiment'].plot(ax=ax3.twinx(), label='Combined Sentiment (right)', color='blue')
ax3.axhline(y=0, color='black', linewidth=0.5, linestyle='--')

for date, action, shares, price in transaction_log:
    color = 'green' if action == 'Buy' else 'red'
    marker = '^' if action == 'Buy' else 'v'
    ax3.scatter(date, price, color=color, label=f'{action} ({shares} shares)', marker=marker)

ax3.set_title('Stock Price and Sentiment with Trading Decisions')
ax3.set_ylabel('Price ($)')
ax3.grid()

plt.tight_layout()
plt.show()