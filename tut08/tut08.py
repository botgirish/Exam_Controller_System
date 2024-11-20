# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

# Task 1: Load and Inspect the Data
# Loading the dataset
df = pd.read_csv('infy_stock.csv', parse_dates=['Date'])

# Displaying the first 10 rows
print("First 10 rows of the dataset:")
print(df.head(10))

# Checking for missing values
print("\nMissing values in the dataset:")
print(df.isnull().sum())

# Handling missing values (dropping rows with missing values)
df.dropna(inplace=True)

# Task 2: Data Visualization
# Plotting the closing price over time
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Closing Price')
plt.title('Stock Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price (INR)')
plt.legend()
plt.grid(True)
plt.show()

# Plotting a candlestick chart for stock prices
df_candlestick = df.set_index('Date')
mpf.plot(df_candlestick, type='candle', style='charles', title='Candlestick Chart', ylabel='Price')

# Task 3: Statistical Analysis
# Calculate daily return percentage
df['Daily Return (%)'] = ((df['Close'] - df['Open']) / df['Open']) * 100

# Calculate the average and median of daily returns
average_return = df['Daily Return (%)'].mean()
median_return = df['Daily Return (%)'].median()

# Calculate the standard deviation of the closing prices
std_dev_close = df['Close'].std()

print(f"\nAverage Daily Return: {average_return:.2f}%")
print(f"Median Daily Return: {median_return:.2f}%")
print(f"Standard Deviation of Closing Prices: {std_dev_close:.2f}")

# Task 4: Moving Averages
# Calculate 50-day and 200-day moving averages
df['50-day MA'] = df['Close'].rolling(window=50).mean()
df['200-day MA'] = df['Close'].rolling(window=200).mean()

# Plot the moving averages along with closing price
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Closing Price')
plt.plot(df['Date'], df['50-day MA'], label='50-day MA', color='orange')
plt.plot(df['Date'], df['200-day MA'], label='200-day MA', color='green')
plt.title('Stock Closing Price with 50-day and 200-day Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.grid(True)
plt.show()

# Task 5: Volatility Analysis
# Calculate rolling standard deviation (volatility) with a 30-day window
df['Volatility (30-day)'] = df['Close'].rolling(window=30).std()

# Plot the volatility
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Volatility (30-day)'], label='30-day Rolling Volatility', color='red')
plt.title('30-day Rolling Volatility of Stock')
plt.xlabel('Date')
plt.ylabel('Volatility (Standard Deviation)')
plt.legend()
plt.grid(True)
plt.show()

# Task 6: Trend Analysis (Bullish and Bearish Trends)
# Identifying bullish and bearish trends based on moving averages
df['Trend'] = np.where(df['50-day MA'] > df['200-day MA'], 'Bullish', 'Bearish')

# Plotting bullish and bearish trends
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Closing Price')
plt.fill_between(df['Date'], df['Close'], where=df['50-day MA'] > df['200-day MA'], color='green', alpha=0.3, label='Bullish Trend')
plt.fill_between(df['Date'], df['Close'], where=df['50-day MA'] <= df['200-day MA'], color='red', alpha=0.3, label='Bearish Trend')
plt.title('Bullish and Bearish Trends Based on Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.grid(True)
plt.show()

# End of the code
