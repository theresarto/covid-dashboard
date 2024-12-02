from ipywidgets import Output
from IPython.display import display
import pandas as pd
from api_wrapper import APIwrapper, fetch_data_with_wrapper


class Fetcher:
    """
    High-level class for fetching and combining data for multiple boroughs.
    """

    # TODO 1: initialise this fetcher. When you initialise, this will require you to add your params
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
                # TODO 2: Use the outside function for fetchin (comes from APIwrapper module)
                data = fetch_data_with_wrapper(self.geography_type, borough, self.metric_name)

                if not data.empty:
                    data["borough"] = borough.replace("%20", " ")
                    self.borough_data[borough] = data
                    print(".", end="", flush=True)  # Print a dot for progress because it's long
                else:
                    print(f"\nNo data available for {borough.replace('%20', ' ')}. Skipping...", flush=True)
                    print(f"Fetching more data", end="", flush=True)

            except Exception as e:
                print(f"\nError fetching data for {borough.replace('%20', ' ')}: {e}", flush=True)

    def fetch_all_boroughs(self, borough_list):
        """
        Fetch data for all boroughs in the given list and combine into a single DataFrame.
        """
        with self.output:
            print("Fetching data", end="")  # Print "Fetching data" once

            # TODO 3: The borough list is in notebook. Iterate through each so you can get all teh data
            for borough in borough_list:
                self.fetch_borough_data(borough)  # Fetch data for each borough
            print()  # Move to the next line after all dots are printed

            # TODO 4: Bec a lot of boroughs, we'll combine them into one DF
            if self.borough_data:
                combined_df = pd.concat(self.borough_data.values(), ignore_index=True)
                combined_df["date"] = pd.to_datetime(combined_df["date"])  # Ensure date column is datetime
                print(f"SUCCESS! Combined data contains {len(combined_df)} rows across {len(self.borough_data)} boroughs.")
                return combined_df
            else:
                print("No data was fetched for any borough.")
                return pd.DataFrame()

    def display_output(self):
        """
        Display the Output widget for Voila compatibility.
        """
        display(self.output)

    # TODO 5: Save this into a JSON file. Call this every time BUTTON in next module wants to reload data
    def save_combined_data(self, boroughs):
        """
        Fetches and saves combined borough data as a JSON file.
        """
        combined_df = self.fetch_all_boroughs(boroughs)

        # TODO 6: I'm nominating my file path already to avoid issues deleting this on Jupyter Notebook
        filename = "data/combined_df.json"

        if not combined_df.empty:
            with open(filename, "w") as json_file:
                combined_df.to_json(json_file, orient="records", indent=4)
            print(f"Data saved to {filename}")
        else:
            print("No data available to save.")
        return combined_df

