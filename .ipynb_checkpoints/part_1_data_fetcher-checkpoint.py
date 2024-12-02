from ipywidgets import Output
from IPython.display import display
import pandas as pd
from part_1_api_wrapper import APIwrapper, fetch_data_with_wrapper
class LDNDataFetcher:
    """
    High-level class for fetching and combining data for multiple boroughs.
    """
    def __init__(self, geography_type, metric_name):
        self.geography_type = geography_type
        self.metric_name = metric_name
        self.borough_data = {}
        self.output = Output()  # Add an Output widget

    def fetch_borough_data(self, borough):
        """
        Fetch data for a single borough and store it in the borough_data dictionary.
        """
        with self.output:
            try:
                data = fetch_data_with_wrapper(self.geography_type, borough, self.metric_name)
                if not data.empty:
                    data["borough"] = borough.replace("%20", " ")
                    self.borough_data[borough] = data
                    print(".", end="", flush=True)  # Print a dot for progress
                else:
                    print(f"\nNo data available for {borough.replace('%20', ' ')}. Skipping...", flush=True)
            except Exception as e:
                print(f"\nError fetching data for {borough.replace('%20', ' ')}: {e}", flush=True)

    def fetch_all_boroughs(self, borough_list):
        """
        Fetch data for all boroughs in the given list and combine into a single DataFrame.
        """
        with self.output:
            print("Fetching data", end="")  # Print "Fetching data" once
            for borough in borough_list:
                self.fetch_borough_data(borough)  # Fetch data for each borough
            print()  # Move to the next line after all dots are printed

            if self.borough_data:
                combined_df = pd.concat(self.borough_data.values(), ignore_index=True)
                combined_df["date"] = pd.to_datetime(combined_df["date"])  # Ensure date column is datetime
                print(f"Combined data contains {len(combined_df)} rows across {len(self.borough_data)} boroughs.")
                return combined_df
            else:
                print("No data was fetched for any borough.")
                return pd.DataFrame()

    def display_output(self):
        """
        Display the Output widget for Voila compatibility.
        """
        display(self.output)