"""
alphavantage_service.py is used to exercise methods built-in the AlphavantagePrice module of functions.

Usage: python alphavantage_service.py
"""

from AlphavantagePrice import Price, PriceExtended, StockDataAnalyzer, NoDataException
import os
import sys
import matplotlib.pyplot as plt


def get_api_key():
    """Retrieve the hashed value of the API key to access the Alphavantage Service."""

    file_name = os.path.join(os.path.dirname(os.getcwd()), 'alphavantage', 'alphavantage_apikey.txt')
    with open(file_name, "rb") as f:
        hashed_api_key = f.read()
    return hashed_api_key.decode("utf-8")


def enter_stock_symbol_command_line():
    """Retrieve user input for the stock symbol and interval.

    Returns:
        tuple: A tuple containing the stock symbol (str) and time interval in minutes (int).
    """
    symbol_inq = input("Enter Ticker Symbol: ")

    while True:
        interval_desired = [1, 5, 30, 60]
        user_input = input(f'Enter value in minutes for time interval {interval_desired}: ')

        try:
            user_input = int(user_input)

            if user_input in interval_desired:
                break
            else:
                print(f'Invalid Number, please enter {interval_desired}')

        except ValueError:
            print(f'Invalid Number, please enter {interval_desired}')

    return symbol_inq, user_input


def main():
    retrieved_api_key = get_api_key()

    symbol, interval = enter_stock_symbol_command_line()

    ticker_symbol = None
    try:
        ticker_symbol = Price(symbol.upper(), interval, retrieved_api_key)
    except NoDataException as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f'------------------------------------------------------------------')
    print(f'symbol:         {ticker_symbol.get_symbol()}')
    print(f'last refreshed: {ticker_symbol.get_last_refreshed()}')
    print(f'interval:       {ticker_symbol.get_interval()}')
    print('-- daily stats --')
    print(f'open:           {float(ticker_symbol.open()):.2f}')
    print(f'low:            {float(ticker_symbol.low()):.2f}')
    print(f'high:           {float(ticker_symbol.high()):.2f}')
    print(f'close:          {float(ticker_symbol.close()):.2f}')
    print(f'volume:         {int(ticker_symbol.volume()):,.0f}')

    ticker_symbol = PriceExtended(symbol.upper(), interval, retrieved_api_key)

    price_info = ticker_symbol.get_ticker_symbol_info()
    print(f'------------------------------------------------------------------')
    print(f'-- Stock Price Information: --')
    for key, value in price_info.items():
        if key in ['open_series', 'close_series', 'volume_series']:
            # print sample data when it's a series
            num_entries_to_display = 5
            print(f'{key}: {value[:num_entries_to_display]}')
        else:
            print(f'{key}: {value}')

    ticker_symbol = StockDataAnalyzer(symbol.upper(), interval, retrieved_api_key)

    print(f'------------------------------------------------------------------')
    print('-- Stock Data Analyzer --')

    total_days, avg_closing_price = ticker_symbol.average_closing_price()
    if avg_closing_price is not None:
        print(f'Average Closing Price for the last {total_days} days:  {avg_closing_price:.2f}')
    else:
        print('Unable to calculate the average closing price.')

    highest_volume_dates, highest_volume = ticker_symbol.find_max_volume_dates()
    if highest_volume_dates:
        for date in highest_volume_dates:
            print(f'Highest volume of stock for {symbol}, volume: {highest_volume:,.0f} on date: {date}')

    fig = ticker_symbol.plot_latest_closing_prices()

    if fig:
        pdf_filename = f"{ticker_symbol.get_symbol()}_latest_closing_prices.pdf"
        fig.savefig(pdf_filename)
        print(f"Plot saved as {pdf_filename}")
        plt.show()

if __name__ == "__main__":
    main()
