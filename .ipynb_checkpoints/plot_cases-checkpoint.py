import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg')  # Use a GUI-based backend (TkAgg works in most cases)
import ipywidgets as widgets
from ipywidgets import HBox, VBox
from IPython.display import display
from datetime import datetime

# Output widget for rendering plots
output_widget = widgets.Output()

"""
Strategy:
- Create a plot that uses the combined cases per borough as the data
- kwargs are set to None at initialisation

Functionalities added:
1. Select by borough - done
2. Select by year - done
3. Select by month - testing

Issues:
- Plot legend is ridiculous when showing all boroughs
"""


def plot_cases(cases_df, year=None, month=None, boroughs=None):
    """
    Plot cases for London boroughs with optional filtering by year and boroughs.
    """
    # TODO: Edge case -- data is empty
    if cases_df is None:
        with output_widget:
            output_widget.clear_output(wait=True)
            print("Cannot plot. DataFrame is missing.")
        return

    # TODO: select the year that is not "ALL"
    if year and year != "All":
        cases_df = cases_df[cases_df["date"].dt.year == int(year)]

    # TODO: select month
    if month and month != "All":
        cases_df = cases_df[cases_df["date"].dt.month == int(month)]

    # TODO: select the borough that is not "ALL"
    if boroughs and boroughs != "All":
        cases_df = cases_df[cases_df["borough"].isin(boroughs)]

    # TODO: create the widget with the plot
    with output_widget:
        output_widget.clear_output(wait=True)
        plt.figure(figsize=(16, 6))

        # plot separate line for each borough
        for borough in cases_df["borough"].unique():
            borough_data = cases_df[cases_df["borough"] == borough]
            plt.plot(borough_data["date"], borough_data["metric_value"], label=borough)

        # Add plot details
        plt.title("COVID-19 Cases in London Boroughs")
        plt.xlabel("Date")
        plt.ylabel("Number of Cases")

        # legend adjustment so it doesn't go crazy
        plt.legend(
            loc="upper left",
            bbox_to_anchor=(1.05, 1),
            fontsize="small",
            title="Boroughs",
        )

        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ---------------------------------- WIDGETS ------------------------------------ #

# TODO Year Dropdown widget
year_dropdown = widgets.Dropdown(
    options=["All", "2020", "2021", "2022", "2023", "2024"],
    value="All",
    description="Year:"
)

# TODO Month Dropdown widget
month_dropdown = widgets.Dropdown(
    options=["All"] + [f"{i:02d}" for i in range(1, 13)],
    value="All",
    description="Month:"
)

# TODO Borough Dropdown widget
"""
To improve: 
- Options should be a global variable starting with ["All"]. 
- Append every successful borough in options to  remove boroughs that weren't imported into data
"""
borough_dropdown = widgets.SelectMultiple(
    options=["All", "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley",
             "Camden", "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
             "Hammersmith and Fulham", "Haringey", "Harrow", "Havering",
             "Hillingdon", "Hounslow", "Islington", "Kensington and Chelsea",
             "Kingston upon Thames", "Lambeth", "Lewisham", "Merton", "Newham",
             "Redbridge", "Richmond upon Thames", "Southwark", "Sutton",
             "Tower Hamlets", "Waltham Forest", "Wandsworth", "Westminster"],
    value=("All",),
    description="Borough(s):",
    layout=widgets.Layout(width="50%")
)

update_button = widgets.Button(
    description="Update Plot",
    button_style='primary',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Click to load London Borough Data',
    icon='refresh'
)


# Function to Update Plot
def update_cases_plot(button, cases_df):
    """
    Callback to update the plot based on widget inputs.
    """
    selected_year = year_dropdown.value
    selected_month = month_dropdown.value
    selected_boroughs = list(borough_dropdown.value) if "All" not in borough_dropdown.value else None

    plot_cases(cases_df, year=selected_year, month=selected_month, boroughs=selected_boroughs)


# Link the button to the update function
def setup_widgets(cases_df):
    """
    Initialize widgets and display them with the output widget.
    """
    update_button.on_click(lambda button: update_cases_plot(button, cases_df))
    display(year_dropdown, month_dropdown, borough_dropdown, update_button, output_widget)
