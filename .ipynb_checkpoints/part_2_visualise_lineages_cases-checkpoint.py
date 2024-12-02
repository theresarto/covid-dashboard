import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


class LineageVisualiser:
    def __init__(self, data=None):
        self.data = data
        self.strain_columns = None

    def load_data(self, file_path):
        """
        Load merged data from a CSV file.
        """
        self.data = pd.read_csv(file_path)
        self.data['week_start'] = pd.to_datetime(self.data['week_start'])
        self.strain_columns = [
            col for col in self.data.columns if col not in ['week_start', 'cases', 'date']
        ]
        print(f"Data loaded with {len(self.data)} rows and {len(self.strain_columns)} strain columns.")

    def interactive_plot(self):
        """
        Interactive plot with dynamic y-axis limits based on strain selection.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data available to plot. Please load the data first.")

        # Create strain dropdown
        strain_dropdown = widgets.SelectMultiple(
            options=["All"] + self.strain_columns,
            value=["All"],
            description="Strains:",
            layout=widgets.Layout(width='50%'),
            style={'description_width': 'initial'}
        )

        # Output widget
        output = widgets.Output()

        def update_plot(change=None):
            with output:
                output.clear_output(wait=True)

                # Filter strains
                selected_strains = list(strain_dropdown.value) 
                if "All" in selected_strains:
                    selected_strains = self.strain_columns

                # Subset data
                filtered_data = self.data[selected_strains]

                # Find the maximum value across the selected strains for dynamic ylim
                max_value = filtered_data.values.max()

                # Plot data
                ax = self.data.plot(
                    x='week_start',
                    y=selected_strains,
                    kind='bar',
                    stacked=True,
                    figsize=(16, 6),
                    title="Weekly Cases Per Strain (Stacked)"
                )

                ax.set_ylim(0, max_value + (0.1 * max_value))  # Add 10% padding for visual clarity

                ax.set_xticks(range(0, len(self.data), max(1, len(self.data) // 10)))
                ax.set_xticklabels(
                    [pd.Timestamp(date).strftime('%Y-%m-%d') for date in self.data['week_start']][::max(1, len(self.data) // 10)],
                    rotation=45,
                    ha="right"
                )
                ax.set_xlabel("Week Start")
                ax.set_ylabel("Cases per 100,000 People")
                ax.legend(title="Strain", bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()

        # Link the dropdown to the plot
        strain_dropdown.observe(update_plot, names='value')

        # Display widgets
        display(widgets.VBox([strain_dropdown, output]))

        # Trigger the first plot
        update_plot()


# Example Usage
if __name__ == "__main__":
    # Initialize the visualiser
    visualiser = LineageVisualiser()

    # Load the data
    try:
        visualiser.load_data("data/merged_lineage_cases.csv")
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

    # Show the interactive plot
    visualiser.interactive_plot()