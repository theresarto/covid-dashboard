import pandas as pd
import pickle


def prepare_data(weekly_cases_path, lineage_data_path):
    """ Loads weekly cases and lineage data (in percentage)"""

    # TODO Load weekly cases
    weekly_cases = pd.read_pickle('data/weekly_cases.pkl')  # Replace with your file path

    # TODO Load lineage data
    lineage_data = pd.read_pickle('data/lineagedf.pkl')
    lineage_data = lineage_data.reset_index()
    lineage_data = lineage_data.rename(columns={'index': 'date'})
    lineage_data['date'] = pd.to_datetime(lineage_data['date'])

    # TODO Find common date ranges (fix issue of empty df)
    common_start = max(weekly_cases['week_start'].min(), lineage_data['date'].min())
    common_end = min(weekly_cases['week_start'].max(), lineage_data['date'].max())
    # print(f"Common Date Range: {common_start} to {common_end}")


    # # TODO DEBUG
    # print("Weekly Cases - Week Start:")
    # print(weekly_cases['week_start'].head(10))

    # print("\nLineage Data - Date:")
    # print(lineage_data['date'].head(10))

    # TODO Merge datasets on 'year' and 'week'
    weekly_cases = weekly_cases[
        (weekly_cases['week_start'] >= common_start) &
        (weekly_cases['week_start'] <= common_end)
        ]

    lineage_data = lineage_data[
        (lineage_data['date'] >= common_start) &
        (lineage_data['date'] <= common_end)
        ]

    # TODO Merge datasets on 'week_start' and 'date'
    merged_data = pd.merge(weekly_cases, lineage_data, left_on='week_start', right_on='date')

    # Calculate cases per strain
    lineage_columns = [col for col in lineage_data.columns if col not in ['date']]
    for strain in lineage_columns:
        merged_data[strain] = merged_data['cases'] * (merged_data[strain] / 100)

    # print(f"PRINTING MERGED DATA HEAD: \n{merged_data.head()}")
    # print(f"PRINTING MERGED DATA TAIL: \n{merged_data.tail()}")

    return merged_data


def save_prepared_data(merged_data, output_path):
    """Save prepared data for visualization."""
    merged_data.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    # File paths
    weekly_cases_path = "data/weekly_cases.pkl"
    lineage_data_path = "data/lineagedf.pkl"
    output_path = "data/merged_lineage_cases.csv"

    # Load and prepare data
    merged_data = prepare_data(weekly_cases_path, lineage_data_path)

    # Save the prepared data
    save_prepared_data(merged_data, output_path)
