import pandas as pd
from api_wrapper import APIwrapper, fetch_data_with_wrapper


class LDNDataFetcher:
    """
    Created class for fetching and combining data for multiple boroughs. This is a module that solely works for London Boroughs.
    """
    def __init__(self, geography_type, metric_name):
        self.geography_type = geography_type
        self.metric_name = metric_name
        self.borough_data = {}

    def fetch_borough_data(self, borough):
        """
        Fetch data for a single borough and store it in the borough_data dictionary.
        """
        try:
            data = fetch_data_with_wrapper(self.geography_type, borough, self.metric_name)
            if not data.empty:
                data["borough"] = borough.replace("%20", " ")
                self.borough_data[borough] = data
                print(".", end="", flush=True)
            else:
                print(f"\nNo data available for {borough.replace('%20', ' ')}. Skipping...")
                print(f"Fetching more data", end="")
        except Exception as e:
            print(f"Error fetching data for {borough.replace('%20', ' ')}: {e}")    def fetch_borough_data(self, borough):
        """
        Fetch data for a single borough and store it in the borough_data dictionary.
        """
        try:
            data = fetch_data_with_wrapper(self.geography_type, borough, self.metric_name)
            if not data.empty:
                data["borough"] = borough.replace("%20", " ")
                self.borough_data[borough] = data
                print(".", end="", flush=True)
            else:
                print(f"\nNo data available for {borough.replace('%20', ' ')}. Skipping...")
                print(f"Fetching more data", end="")
        except Exception as e:
            print(f"Error fetching data for {borough.replace('%20', ' ')}: {e}")

    def fetch_all_boroughs(self, borough_list):
        """
        Fetch data for all boroughs in the given list and combine into a single DataFrame.
        """
        print(f"Fetching data", end="")
        for borough in borough_list:
            self.fetch_borough_data(borough)

        print()

        if self.borough_data:
            combined_df = pd.concat(self.borough_data.values(), ignore_index=True)
            combined_df["date"] = pd.to_datetime(combined_df["date"])  # Ensure date column is datetime
            print(f"Combined data contains {len(combined_df)} rows across {len(self.borough_data)} boroughs.")
            return combined_df
        else:
            print("No data was fetched for any borough.")
            return pd.DataFrame()