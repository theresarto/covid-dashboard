import matplotlib.pyplot as plt
from ipywidgets import interact, widgets, Button, Output
from IPython.display import display, clear_output
import pandas as pd
import json
from fetcher import Fetcher
from time import sleep
import sys

# Output widget for rendering plots
output_widget = Output()

# Global variable to store cases data (not ideal but works in this notebook setting)
# cases_df = None

# ----------------------------------- PLOTTING ----------------------------------- #

# TODO: Set up the plot
def plot_cases(cases_df, year=None, month=None, boroughs=None):
    """
    Plot cases for London boroughs with optional filtering by year, month, and boroughs.
    """

    # # TODO debug!!
    # print("Initial DataFrame:")
    # print(cases_df.head())  # Debug: Print the DataFrame before filtering

    if cases_df is None or cases_df.empty:
        with output_widget:
            output_widget.clear_output(wait=True)
            print("Cannot plot. DataFrame is missing or empty.")
        return

    # Filter data by year
    if year and year != "All":
        cases_df = cases_df[cases_df["date"].dt.year == int(year)]

    # Filter data by month
    if month and month != "All":
        cases_df = cases_df[cases_df["date"].dt.month == int(month)]

    # TODO: DEBUG BOROUGHS
    # Filter data by boroughs
    if boroughs and "All" not in boroughs:
        print("Filtering for boroughs:", boroughs)  # Debug
        cases_df = cases_df[cases_df["borough"].isin(boroughs)]
    # Sort boroughs alphabetically before plotting
    sorted_boroughs = sorted(cases_df["borough"].unique())

    # print("Filtered DataFrame after applying boroughs, year, and month:")
    # print(cases_df.head())  # Debug

    # Plot the filtered data
    with output_widget:
        output_widget.clear_output(wait=True)
        plt.figure(figsize=(16, 7))

        for borough in sorted_boroughs:
            borough_data = cases_df[cases_df["borough"] == borough]
            plt.plot(borough_data["date"], borough_data["metric_value"], label=borough)

        plt.title("COVID-19 Cases in London Boroughs")
        plt.xlabel("Date")
        plt.ylabel("Number of Cases")
        plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1), fontsize="small", title="Boroughs")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# --------------------------------- INITIAL SETUP -------------------------------- #

# TODO: Load the initial JSON
def load_initial_data(filepath="data/combined_df.json"):
    """
    Load the initial data from the JSON file for offline access.
    """
    try:
        with open(filepath, 'r') as f:
            json_data = json.load(f)
        print("Loaded initial data successfully.")
        df = pd.DataFrame(json_data)
        df["date"] = pd.to_datetime(df["date"], unit='ms')
        df = df.sort_values(by="date").reset_index(drop=True)
        return df
    except FileNotFoundError:
        print(f"File {filepath} not found. Please fetch data using the 'Fetch Data' button.")
        return None


# ------------------------------ CREATE WIDGET ------------------------------ #

def update_cases_plot(cases_df, year, month, boroughs):
    """
    Update the plot dynamically based on widget values.
    We will be calling this in create_widgets(df) below!
    """
    print(f"Year: {year}, Month: {month}, Boroughs: {boroughs}")  # Debug print
    plot_cases(cases_df, year=year, month=month, boroughs=boroughs)


def create_widgets(cases_df):
    """
    Create interactive widgets and display them.
    """
    # TODO Debugging: Ensure DataFrame is passed correctly
    # print("Initial DataFrame passed to create_widgets:")
    # print(cases_df.head())
    # print("Unique boroughs in DataFrame:", cases_df["borough"].unique())  # Debug

    # TODO: Detail the dropdown widgets
    year_dropdown = widgets.Dropdown(
        options=["All", "2020", "2021", "2022", "2023", "2024"],
        value="All",
        description="Year:"
    )

    month_dropdown = widgets.Dropdown(
        options=["All"] + [f"{i:02d}" for i in range(1, 13)],
        value="All",
        description="Month:"
    )

    borough_dropdown = widgets.SelectMultiple(
        options=["All"] + sorted(cases_df["borough"].unique()),
        value=("All",),
        description="Borough(s):",
        layout=widgets.Layout(width="50%")
    )

    fetch_button = Button(
        description="Fetch New Data",
        button_style='success',
        tooltip="Fetch latest data from the API",
        icon="refresh"
    )

    # TODO: MAJOR ONE! Ensure callback function works
    def fetch_button_callback(button):
        global cases_df
        print("Fetching data...")

        london_boroughs = ["Barking%20and%20Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden", "Croydon",
                           "Ealing", "Enfield", "Greenwich", "Hackney", "Hammersmith%20and%20Fulham", "Haringey",
                           "Harrow", "Havering", "Hillingdon", "Hounslow", "Islington", "Kensington%20and%20Chelsea",
                           "Kingston%20upon%20Thames", "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
                           "Richmond%20upon%20Thames", "Southwark", "Sutton", "Tower%20Hamlets", "Waltham%20Forest",
                           "Wandsworth", "Westminster"]

        geography_type = "Lower%20Tier%20Local%20Authority"
        metrics = "COVID-19_cases_casesByDay"
        fetcher = Fetcher(geography_type, metrics)  # Have to call again every time we fetch :(

        # TODO: Reload the output_widget with new data
        with output_widget:  # Use the global `output_widget` to show progress to solve progress issue
            clear_output(wait=True)
            print("FETCH REQUESTED. Please see progress below:")
            fetcher.display_output()  # Display Fetcher's Output widget in the notebook. Have to do this because can't see progress
            cases_df = fetcher.fetch_all_boroughs(london_boroughs)  # Reuse fetcher to fetch all borough data

            # Final update!!
            if not cases_df.empty:
                print("\nData fetching complete. Click on your selected filter to plot.")
                # TODO: Get plot to load agin after fetching or else will look silly
                update_cases_plot(cases_df, year="All", month="All", boroughs=("All",))  # Plot fetched data
            else:
                print("\nNo data could be fetched. Please try again.")

    # TODO: Combines everything above into a click
    fetch_button.on_click(fetch_button_callback)

    # TODO: Create interactive widgets for plotting. Failed to work w/o interact :(
    interact(lambda year, month, boroughs: update_cases_plot(cases_df, year, month, boroughs),
             year=year_dropdown, month=month_dropdown, boroughs=borough_dropdown)
    display(fetch_button, output_widget)


# ------------------------------------ MAIN ------------------------------------ #

# Prevent automatic execution on import. Also, for Pycharm
if __name__ == "__main__":
    # Load initial data
    cases_df = load_initial_data()

    # Show initial plot if data exists
    if cases_df is not None:
        plot_cases(cases_df)

    # Create widgets
    create_widgets(cases_df)