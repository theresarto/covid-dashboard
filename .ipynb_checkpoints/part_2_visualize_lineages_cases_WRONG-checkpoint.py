import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display



def load_merged_data(file_path):
    """Load the merged lineage cases data."""
    data = pd.read_csv(file_path)
    data['week_start'] = pd.to_datetime(data['week_start'])
    return data


def plot_stacked_bar(data, output_path=None):
    """Plot a stacked bar chart of cases per strain over time."""
    # TODO isolate columns to week start, date, and cases to match weekly-cases
    strain_columns = [col for col in data.columns if col not in ['week_start', 'date', 'cases']]

    # TODO convert week_start to datetime for better plotting
    data['week_start'] = pd.to_datetime(data['week_start'])

    # TODO create stacked bar chart
    data.plot(
        x='week_start',
        y=strain_columns,
        kind='bar',
        stacked=True,
        figsize=(14, 8),
        title="Weekly Cases Per Strain (Stacked)",
    )

    # Customize the plot
    plt.xticks(data['week_start'][::4], rotation=45)  # Rotate x-axis labels for clarity
    plt.xlabel("Week Start")
    plt.ylabel("Cases per 100,000 People")
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal gridlines
    plt.legend(title="Strain")
    plt.tight_layout()

    # Save or display the plot
    if output_path:
        plt.savefig(output_path)
        print(f"Chart saved to {output_path}")
    else:
        plt.show()



def interactive_plot(data):
    """
    Interactive visualization with widgets for dynamic filtering and plotting.

    Args:
        data (pd.DataFrame): The input dataset with cases and strain data.
    """
    # Extract unique strains and years
    strains = ['All'] + [col for col in data.columns if col not in ['week_start', 'date', 'cases']]
    years = ['All'] + sorted(data['week_start'].dt.year.unique().tolist())

    # Create widgets
    strain_dropdown = widgets.Dropdown(
        options=strains,
        value='All',
        description='Strain:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px')  # Adjust widget width
    )

    year_dropdown = widgets.Dropdown(
        options=years,
        value='All',
        description='Year:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='200px')  # Adjust widget width
    )

    update_button = widgets.Button(
        description="Update Plot",
        button_style='primary',  # Styling for the button
        tooltip='Click to refresh the plot with current selections',
        icon='refresh'  # FontAwesome icon
    )

    # Create an output widget for rendering the plot
    output = widgets.Output()

    # Define the update function
    def update_chart(button=None):
        """
        Update chart based on widget values.
        """
        with output:
            # Clear previous output
            output.clear_output(wait=True)

            # Filter the data
            filtered_data = data.copy()
            selected_year = year_dropdown.value
            selected_strain = strain_dropdown.value

            # Filter by year
            if selected_year != 'All':
                filtered_data = filtered_data[filtered_data['week_start'].dt.year == int(selected_year)]

            # Filter by strain
            strain_columns = [selected_strain] if selected_strain != 'All' else [
                col for col in data.columns if col not in ['week_start', 'date', 'cases']
            ]

            # Debugging: Print filtered data and strains
            print(f"Filtered Data:\n{filtered_data.head()}")
            print(f"Strain Columns: {strain_columns}")

            # Check if filtered data is empty
            if filtered_data.empty:
                print("No data available for the selected strain/year.")
                return

            # Plot the updated chart
            filtered_data.plot(
                x='week_start',
                y=strain_columns,
                kind='bar',
                stacked=True,
                figsize=(14, 8),
                title="Weekly Cases Per Strain (Stacked)",
            )

            # Enhance the chart
            plt.xticks(filtered_data['week_start'][::4], rotation=45)  # Rotate x-axis labels
            plt.xlabel("Week Start")
            plt.ylabel("Cases per 100,000 People")
            plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add gridlines
            plt.legend(title="Strain")
            plt.tight_layout()
            plt.show()

    # Link the button to the update function
    update_button.on_click(update_chart)

    # Display widgets and the output area
    display(widgets.VBox([strain_dropdown, year_dropdown, update_button]))
    display(output)

    # Trigger initial rendering
    update_chart()


# Main execution logic
if __name__ == "__main__":
    # File path for merged data
    merged_data_path = "data/merged_lineage_cases.csv"  # Update with your actual file path

    # Load the merged data
    data = load_merged_data(merged_data_path)

    # Start the interactive plot
    interactive_plot(data)