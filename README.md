# alphavantage_service
Provides convenient methods to access alphavantage.co service to fetch financial market data through a set of 
powerful and developer-friendly data APIs

The Alphavantage service is relatively easy to use, but it's still requires that you remember
how the data is structured and to write the necessary JSON or CSV parsing code.  
If you plan to access the service frequently, 

# AlphavantagePrice Python Module
The `AlphavantagePrice` module provides Python classes for convenient access to the Alphavantage service,
primarily focused on intraday Time Series Stock Data APIs.
It offers a variety of methods for retrieving, analyzing, and visualizing financial data.

# AlphavantagePrice Python Module

## Classes

### Price

The `Price` class allows you to access intraday stock data, 
including opening, closing, high, low prices, and volume. 
It also provides methods for extracting metadata and historical data.

### PriceExtended

The `PriceExtended` class extends the functionality of the `Price` class and provides additional methods 
for working with stock data, including historical series data.

### StockDataAnalyzer

The `StockDataAnalyzer` class further extends the features for working with intraday stock data. 
It includes methods for calculating the average closing price, finding dates with the highest trading volume,
and plotting the latest closing prices.

## Usage

To use the `AlphavantagePrice` module, you'll need to obtain an API key from Alphavantage. 
Make sure to provide the key when initializing the classes.

Here's an example of using the module:

# Import the required classes
from AlphavantagePrice import Price, PriceExtended, StockDataAnalyzer, NoDataException

# Initialize the classes with your API ke
ticker_symbol = Price("AAPL", 30, "your_api_key")
ticker_symbol_extended = PriceExtended("AAPL", 30, "your_api_key")
data_analyzer = StockDataAnalyzer("AAPL", 30, "your_api_key")

# Retrieve and analyze stock data
print(ticker_symbol.get_symbol())
print(ticker_symbol.open())
# ... see class documentation

# Analyze extended data
print(ticker_symbol_extended.get_symbol())
print(ticker_symbol_extended.open())
# ... # ... see class documentation

# Analyze stock data
average_days, avg_close = data_analyzer.average_closing_price()
print(f"Average Closing Price for the last {average_days} days: {avg_close:.2f}")

max_vol_dates, max_vol = data_analyzer.find_max_volume_dates()
for date in max_vol_dates:
    print(f"Highest volume on {date} with volume: {max_vol:,.0f}")

# to see clsoing price over time use method:
data_analyzer.plot_latest_closing_prices()
