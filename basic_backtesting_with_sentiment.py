import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("cleaned_sentiment_and_prices.csv")

initial_cash = 10000
cash = initial_cash
shares = 0
transaction_log = []

buy_sentiment_threshold = float(input("Enter the Buy sentiment threshold: "))
sell_sentiment_threshold = float(input("Enter the Sell sentiment threshold: "))

#trading strat
for i in range(1, len(df)):
    sentiment = df.loc[i, 'combined_sentiment']
    current_price = df.loc[i, 'tesla_close']
    date = df.loc[i, 'date']

    if sentiment > buy_sentiment_threshold:
        if cash >= current_price:
            shares_bought = int(cash // current_price)
            cash -= shares_bought * current_price
            shares += shares_bought
            transaction_log.append((date, 'Buy', shares_bought, current_price))

    elif sentiment < sell_sentiment_threshold:
        if shares > 0:
            cash += shares * current_price
            transaction_log.append((date, 'Sell', shares, current_price))
            shares = 0

# Calculate performance metrics
final_cash = cash + (shares * df.loc[len(df) - 1, 'tesla_close'])
roi = (final_cash - initial_cash) / initial_cash * 100

win_trades = 0
loss_trades = 0
returns = []
peak = -np.inf
max_drawdown = 0

#document the logs
for i in range(1, len(transaction_log)):
    if transaction_log[i][1] == 'Sell':
        buy_price = transaction_log[i - 1][3]
        sell_price = transaction_log[i][3]
        profit_loss = sell_price - buy_price
        returns.append((sell_price - buy_price) / buy_price)

        if profit_loss > 0:
            win_trades += 1
        else:
            loss_trades += 1

    # Calculate maximum drawdown
    if transaction_log[i][3] > peak:
        peak = transaction_log[i][3]
    drawdown = (peak - transaction_log[i][3]) / peak
    if drawdown > max_drawdown:
        max_drawdown = drawdown

win_loss_ratio = win_trades / loss_trades if loss_trades > 0 else float('inf')

mean_return = np.mean(returns)
std_return = np.std(returns)
sharpe_ratio = mean_return / std_return if std_return > 0 else float('inf')  # Assuming 2% risk-free rate

print(f"ROI: {roi:.2f}%")
print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Maximum Drawdown: {max_drawdown:.2f}")


# Save metrics to CSV
metrics = {
    'buy_sentiment_threshold': buy_sentiment_threshold,
    'sell_sentiment_threshold':sell_sentiment_threshold,
    'Initial Cash': initial_cash,
    'Final Portfolio Value': final_cash,
    'ROI (%)': roi,
    'Win/Loss Ratio': win_loss_ratio,
    'Sharpe Ratio': sharpe_ratio,
    'Max Drawdown (%)': max_drawdown
}

metrics_df = pd.DataFrame([metrics])
metrics_df.to_csv('performance_metrics.csv', index=False)

# Save transaction log to CSV
transaction_df = pd.DataFrame(transaction_log, columns=['Date', 'Action', 'Shares', 'Price'])
transaction_df.to_csv('transaction_log.csv', index=False)
