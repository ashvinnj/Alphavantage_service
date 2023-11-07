r"""
    AlphavantagePrice.py defines module of python class(es): 'Price', 'PriceExtended' and 'StockDataAnalyzer.'
    that provides methods to make access convenient to the Alphavantage service. Categories of services offered are:
    (1) Core Time Series Stock Data APIs,
    (2) Alpha Intelligence™,
    (3) Fundamental Data,
    (4) Physical and Digital/Crypto Currencies (e.g., Bitcoin),
    (5) Commodities, (6) Economic Indicators, and
    (7) Technical Indicators.
    This script is build to get exposure to learn web APIs in Pyton.
    We will explore intraday Time Series Stock Data APIs
    e.g. url:
    https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
    also Tracking search utilities
    Sample Json:
    {
     "Meta Data": {
          "1. Information": "Intraday (60min) open, high, low, close prices and volume",
          "2. Symbol": "IBM",
          "3. Last Refreshed": "2023-11-03 15:00:00",
          "4. Interval": "60min",
          "5. Output Size": "Full size",
          "6. Time Zone": "US/Eastern"
     },
     "Time Series (60min)": {
          "2023-11-03 15:00:00": {
               "1. open": "148.1500",
               "2. high": "148.2300",
               "3. low": "147.7800",
               "4. close": "147.9000",
               "5. volume": "709177"
          },
          "2023-11-03 14:00:00": {
               "1. open": "147.9450",
               "2. high": "148.2500",
               "3. low": "147.9000",
               "4. close": "148.1450",
               "5. volume": "257079"
          }
    }
}
"""

import datetime
import json
import matplotlib.pyplot as plt
import requests


class NoDataException(Exception):
    pass


class Price():
    """
    AlphavantagePrice.py defines a module containing Python classes: 'Price', 'PriceExtended' and 'StockDataAnalyzer.'
    These classes provide methods to conveniently access Alphavantage service, particularly for intraday
    Time Series Stock Data APIs. These APIs offer access to a wide range of financial data for stocks.
    Further extension possible to access cryptocurrencies, commodities, and more.

    This module allows users to access and analyze financial data, retrieve metadata, and perform
    various calculations and visualizations.

    Author: Ashvin Patel
    Date: 10-15-2023
    """

    def __init__(self, in_symbol, minutes, apikey, extended_hours=False):
        """Initialize a Price instance.

        Args:
            in_symbol (str): The stock symbol of interest.
            minutes (int): The time interval in minutes for data retrieval.
            apikey (str): Your API key for accessing financial data (hash key version used)
            extended_hours (bool, optional): Whether to include extended hours data. Default is False.
        """

        self.interval_mins = f'{minutes}min'
        self.symbol = in_symbol
        self.apikey = apikey
        self.extended_hours = extended_hours
        self.json_data = self.download_data()

    def download_data(self):
        """Download data from Alphavantage API and parse it into JSON format.

        Returns:
            dict: A dictionary containing the JSON data retrieved from the Alphavantage API.

        connects with Apivantage service and retrieves json data for given ticker symbol
        The download_data method sends an HTTP GET request to the Alpha Vantage API to retrieve intraday price data
        for the specified stock symbol. It specifies various parameters such as the symbol, time interval,
        extended hours, and API key. The response from the API is expected to be in JSON format,
        and it is parsed into a Python dictionary using json.loads.

        """

        extended_hours_str = 'true' if self.extended_hours else 'false'  # give me pre&post opening data as well
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.symbol,
            'interval': self.interval_mins,
            'extended_hours': extended_hours_str,
            'outputsize': 'full',
            'apikey': self.apikey
        }
        base_url = 'https://www.alphavantage.co/query'
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Check for HTTP errors
            json_data = json.loads(response.text)
            if "Meta Data" not in json_data:
                raise NoDataException("No valid data found in the response.")
            return json_data
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_metadata(self):
        """Retrieve metadata information from the JSON data.

        Returns:
            dict: A dictionary containing metadata information from the JSON data.

        The get_metadata method extracts the "metaData" section from the JSON response,
        which contains information about the stock data. This "metadata" section is a dictionary
        within the larger JSON object. metadata = price_instance.get_metadata() then
        to get to symbol: symbol = metadata["2. Symbol"]
        """

        metadata = self.json_data.get("Meta Data", {})
        return metadata

    def get_json(self):
        """Get the JSON data in a pretty-printed format for debugging.

        Returns:
            str: The JSON data as a well-formatted string.
        """
        return json.dumps(self.json_data, indent=5)

    def get_interval(self):
        """Retrieve the time interval of the data retrieved from the API.

          Returns:
              str: The time interval (e.g., "60min").

        """

        key_value1 = self.get_metadata()
        key_value = key_value1["1. Information"]
        interval = key_value.split(' ')[1]
        interval = interval.replace('(', '').replace(')', '')
        return interval

    def get_symbol(self):
        """Retrieve the stock symbol associated with the data.

        Returns:
            str: The stock symbol.
        """
        key_value = self.get_metadata()
        return key_value["2. Symbol"]

    def get_last_refreshed(self):
        """Retrieve the date and time when the service was last consulted.

        Returns:
            str: The date and time (e.g., "2023-11-03 15:00:00").
        """

        key_value = self.get_metadata()
        return key_value["3. Last Refreshed"]

    def get_data_for_last_refreshed(self):
        """Get data from the time series for the last refreshed timestamp.

         Returns:
             dict: Data for the last refreshed timestamp, or None if not found.
         """

        last_refreshed = self.get_last_refreshed()
        time_series = self.json_data.get("Time Series (" + self.interval_mins + ")")

        if time_series:
            for key, value in time_series.items():
                if key.strip() == last_refreshed:
                    data_for_last_refreshed = value
                    return data_for_last_refreshed

        return None

    def open(self):
        """Retrieve the stock's opening price for the last refreshed timestamp.

        Returns:
            str: The opening price, or None if not found.
        """
        daily_stats = self.get_data_for_last_refreshed()
        if daily_stats:
            return daily_stats["1. open"]
        return None

    def high(self):
        """Retrieve the stock's highest price for the day at the last refreshed timestamp.

        Returns:
            str: The highest price, or None if not found.
        """
        daily_stats = self.get_data_for_last_refreshed()
        if daily_stats:
            return daily_stats["2. high"]
        return None

    def low(self):
        """Retrieve the stock's lowest price for the day at the last refreshed timestamp.

        Returns:
            str: The lowest price, or None if not found.
        """

        daily_stats = self.get_data_for_last_refreshed()
        if daily_stats:
            return daily_stats["3. low"]
        return None

    def close(self):
        """Retrieve the stock's closing price for the last refreshed timestamp.

        Returns:
            str: The closing price, or None if not found.
        """

        daily_stats = self.get_data_for_last_refreshed()
        if daily_stats:
            return daily_stats["4. close"]
        return None

    def volume(self):
        """Retrieve the volume data for the last refreshed timestamp.

        Returns:
            str: The volume data, or None if not found.
        """

        daily_stats = self.get_data_for_last_refreshed()
        if daily_stats:
            return daily_stats["5. volume"]
        return None

    def get_timestamps(self):
        """Get timestamps from the time series data.

        Returns:
            list: A list of timestamps from the time series data, or an empty list if no data is found.
        """

        time_series = self.json_data.get("Time Series (" + self.interval_mins + ")")
        if time_series:
            timestamps = [timestamp for timestamp in time_series.keys()]
            return timestamps
        return []

    def get_data_for_timestamp(self, timestamp):
        """Get data for a specific timestamp from the time series data.

         Args:
             timestamp (str): The timestamp for which to retrieve data.

         Returns:
             dict or None: Data for the specified timestamp returned as dict object,
            or None if the timestamp is not found in the data.
         """

        time_series = self.json_data.get("Time Series (" + self.interval_mins + ")")
        if time_series:
            return time_series.get(timestamp)
        return None


class PriceExtended(Price):
    def __init__(self, symbol, interval, api_key):
        """Initialize a PriceExtended instance.

        Args:
            symbol (str): The stock symbol of interest.
            interval (int): The time interval in minutes for data retrieval.
            api_key (str): Your API key for accessing financial data.
        """

        super().__init__(symbol, interval, api_key)

    def get_ticker_symbol_info(self):
        """Get detailed price information.

        Returns:
            dict: A dictionary containing detailed price information including symbol, last refreshed timestamp,
                  interval, open, low, high, close, volume, and historical series data if available.
        """

        timestamps = self.get_timestamps()
        info = {
            'symbol': self.get_symbol(),
            'last_refreshed': self.get_last_refreshed(),
            'interval': self.get_interval(),
            'open': "{:.2f}".format(float(self.open())),
            'low': "{:.2f}".format(float(self.low())),
            'high': "{:.2f}".format(float(self.high())),
            'close': "{:.2f}".format(float(self.close())),
            'volume': "{:,}".format(int(self.volume()))
        }

        if timestamps:
            info['open_series'] = self.series('1. open')
            info['close_series'] = self.series('4. close')
            info['volume_series'] = self.series('5. volume')
        else:
            info['open_series'] = []
            info['close_series'] = []
            info['volume_series'] = []

        return info

    def series(self, parameter):
        """Retrieve historical series data for a given attribute (parameter).

        Args:
            parameter (str): The attribute for which to retrieve historical data (e.g., '1. open', '4. close').

        Returns:
            list: A list of historical data values for the specified attribute, or an empty list if no data is found.
        """
        time_series = self.json_data.get("Time Series (" + self.interval_mins + ")")
        if time_series:
            series_list_values = []
            for timestamp, data in time_series.items():
                series_list_values.append(data.get(parameter, None))
            return series_list_values
        return []


class StockDataAnalyzer(Price):
    def __init__(self, symbol, interval, api_key):
        """Initialize a StockDataAnalyzer instance.

        Args:
            symbol (str): The stock symbol of interest.
            interval (int): The time interval in minutes for data retrieval.
            api_key (str): Your API key for accessing financial data.
        """

        super().__init__(symbol, interval, api_key, extended_hours=True)

    def find_max_volume_dates(self):
        r"""Find maximum volume exchanged on given date(s) and handle tie breakers.

        Returns:
            tuple: A tuple containing a list of dates with maximum volume and the maximum volume value.
        """
        timestamps = self.get_timestamps()
        daily_volumes = {}

        for timestamp in timestamps:
            date = timestamp.split()[0]
            data = self.get_data_for_timestamp(timestamp)
            volume = int(data["5. volume"])

            if date in daily_volumes:
                daily_volumes[date] += volume
            else:
                daily_volumes[date] = volume

        max_volume = max(daily_volumes.values())
        # list comprehension to get dates of matching max volume
        max_volume_dates = [date for date, volume in daily_volumes.items() if volume == max_volume]

        return max_volume_dates, max_volume

    def average_closing_price(self):
        """Calculate the average closing price for the last 'xx' days.

        Returns:
            tuple: A tuple containing the total number of unique days and the average closing price,
                   or (None, None) if no data is available.
        """
        timestamps = self.get_timestamps()

        if not timestamps:
            return None, None

        today = datetime.datetime.today().date()
        unique_days = set()

        for timestamp in timestamps:
            date = timestamp.split()[0]
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date != today:
                unique_days.add(date)

        # Calculate the average closing price for unique days
        total_closing_price = 0.0
        total_days = len(unique_days)

        for timestamp in timestamps:
            date = timestamp.split()[0]
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date in unique_days:
                daily_stats = self.get_data_for_timestamp(timestamp)
                if daily_stats:
                    total_closing_price += float(daily_stats["4. close"])
                    unique_days.remove(date)

        if total_days > 0:
            return total_days, total_closing_price / total_days

        return None, None

    def get_latest_closing_prices_by_date(self):
        r"""Get the latest closing price for each unique date.

        Returns:
            dict: A dictionary containing dates as keys and the latest closing prices as values.
        """

        timestamps = self.get_timestamps()
        closing_prices_by_date = {}

        for timestamp in timestamps:
            date = timestamp.split()[0]
            data = self.get_data_for_timestamp(timestamp)
            closing_price = data.get("4. close")

            # Capture the latest closing price for each unique date
            closing_prices_by_date[date] = float(closing_price)

        return closing_prices_by_date

    def plot_latest_closing_prices(self):
        r"""Create a plot of the latest closing prices.

        Returns:
            Figure or None: A Matplotlib figure of the plot or None if there's no data available for plotting.
        """

        closing_prices_by_date = self.get_latest_closing_prices_by_date()

        if not closing_prices_by_date:
            print("No data available for plotting.")
            return None

        dates = list(closing_prices_by_date.keys())
        prices = list(closing_prices_by_date.values())

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, prices, marker='o', linestyle='-')
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price")
        ax.set_title(f"Latest Closing Prices for {self.get_symbol()}")
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        return fig  # Return the figure
