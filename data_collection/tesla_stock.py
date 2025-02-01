import yfinance as yf
start_date = "2023-01-01"
end_date = "2024-12-31"

tesla = yf.Ticker("TSLA")

# Fetch historical stock data for Tesla within the specified date range
data = tesla.history(start=start_date, end=end_date)
data.reset_index(inplace=True)

# Format the 'Date' column as 'MM-DD-YYYY'
data['Date'] = data['Date'].dt.strftime('%m-%d-%Y')

# Round the 'Close' prices to two decimal places
data['Close'] = data['Close'].round(2)

# Save the 'Date' and 'Close' columns to a CSV file named 'tesla_closing_prices.csv'
data[['Date', 'Close']].to_csv('tesla_closing_prices.csv', index=False)

print("Missing values in data:", data.isnull().sum())
print(f"Tesla stock closing prices from {start_date} to {end_date} saved to tesla_closing_prices.csv!")