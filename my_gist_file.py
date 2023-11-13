
{
     "Meta Data": {
          "1. Information": "Intraday (30min) open, high, low, close prices and volume",
          "2. Symbol": "IBM",
          "3. Last Refreshed": "2023-11-03 19:30:00",
          "4. Interval": "30min",
          "5. Output Size": "Full size",
          "6. Time Zone": "US/Eastern"
     },
     "Time Series (30min)": {
          "2023-11-03 19:30:00": {
               "1. open": "147.7800",
               "2. high": "147.7800",
               "3. low": "147.7800",
               "4. close": "147.7800",
               "5. volume": "75"
          },
          "2023-11-03 19:00:00": {
               "1. open": "147.9000",
               "2. high": "148.0000",
               "3. low": "147.7800",
               "4. close": "147.8900",
               "5. volume": "387981"
          }
     }
}


def get_metadata(self):
    """Retrieve metadata information from the JSON data as dict obj"""
    metadata = self.json_data.get("Meta Data", {})
    return metadata

def get_last_refreshed(self):
        return self.get_metadata().get("3. Last Refreshed")
def get_data_for_timestamp(self, timestamp):
    """Get data for a specific timestamp from the time series data as a list """
    time_series = self.json_data.get("Time Series (" + self.interval_mins + ")")
    if time_series:
        return time_series.get(timestamp)
    return None

##  class StockDataAnalyzer(Price):

    def find_max_volume_dates(self):

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
        # list comprehension to get dates of matching max volume i.e. catch tie-breakers
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

            if date in closing_prices_by_date:
                existing_timestamp = closing_prices_by_date[date]
                if timestamp > existing_timestamp:
                    closing_prices_by_date[date] = timestamp
            else:
                closing_prices_by_date[date] = timestamp

        latest_closing_prices = {}
        for date, latest_timestamp in closing_prices_by_date.items():
            data = self.get_data_for_timestamp(latest_timestamp)
            closing_price = float(data.get("4. close"))
            latest_closing_prices[date] = closing_price

        return latest_closing_prices

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
