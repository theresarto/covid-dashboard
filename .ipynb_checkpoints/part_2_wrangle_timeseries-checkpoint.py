import pandas as pd
import json
from datetime import datetime

"""
This is a data wrangling file that I have written (instead of the provided Jupyter Notebook) for better modularity.
There are three steps to wrangling this:
1. Load the timeseries file
2. Group the data by week (because we will be comparing against lineages which is a weekly dat)
3. Clean timeseris if there are any null fields

"""


def load_timeseries(file_path):
    # TODO open the timeseries JSON provided
    with open(file_path, 'r') as f:
        rawdata = json.load(f)

    # TODO convert to dataframe and ensure date is converted to datetime
    if "data" in rawdata:
        df = pd.DataFrame(rawdata["data"])  # Convert to DataFrame
    else:
        raise KeyError("The rawdata does not contain the 'data' key")

    # TODO check if 'date' column exists
    if "date" not in df.columns:
        raise KeyError("The DataFrame does not contain a 'date' column")

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop rows where 'date' could not be converted
    if df['date'].isna().any():
        print("Warning: Some dates could not be converted and will be dropped.")
        df = df.dropna(subset=['date'])

    return df


def group_by_week(df):
    """Aggregate daily cases into weekly cases."""

    # TODO sort by date to ensure proper visualisation
    df = df.sort_values('date')

    # TODO create a 'week' column representing the year and week number
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.isocalendar().year

    # TODO Group by year and week, aggregating cases
    weekly_cases = df.groupby(['year', 'week']).agg({'cases': 'sum'}).reset_index()

    # Calculate week start date (aligned to Monday)
    weekly_cases['week_start'] = (
            pd.to_datetime(weekly_cases['year'].astype(str) + '-01-01')
            + pd.to_timedelta((weekly_cases['week'] - 1) * 7, unit='D')
    )
    weekly_cases['week_start'] = weekly_cases['week_start'] - pd.to_timedelta(
        weekly_cases['week_start'].dt.weekday, unit='D'
    )  # Align week_start to Monday

    # Drop unnecessary columns
    weekly_cases = weekly_cases.drop(columns=['year', 'week'])

    return weekly_cases


def clean_timeseries(df):
    """Clean the timeseries DataFrame."""

    # TODO drop rows with NaN values in 'cases' to ensure data integrity
    df = df.dropna(subset=['cases'])

    # TODO ensure 'cases' column is numeric
    df.loc[:, 'cases'] = pd.to_numeric(df['cases'], errors='coerce')

    return df


# Data testing
if __name__ == "__main__":
    # Example usage
    file_path = "data/timeseries.json"
    df = load_timeseries(file_path)
    df = clean_timeseries(df)
    weekly_cases = group_by_week(df)
    print(weekly_cases.head(20))
    weekly_cases.to_pickle("data/weekly_cases.pkl")
