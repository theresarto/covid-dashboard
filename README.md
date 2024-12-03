# COVID Dashboard

The COVID Dashboard is an interactive Jupyter Notebook that analyses and visualises COVID-19 data. This project uses Python to fetch, process, and display real-time or historical data trends across various regions. With features like overlay graphs, stacked bar charts, and interactive widgets, users can explore insights into cases, lineages, and their correlation with other metrics such as deaths.

## Features
- Visualise daily and historical COVID-19 case trends by region.
- Generate insights with interactive graphs and filters.
- Fetch the latest data or work offline with pre-saved datasets.

## Known Issues
- Unfortunately, Voila doesn't allow you to directly save the produced gzip file.

### Fallback Solution
If you need to save the gzip file manually, you can run the notebook locally instead of using Voila. Here's how:
1. Clone the repository to your local machine using `git clone <repository-url>`.
2. Set up the required environment using `conda`:
   ```bash
   conda env create -f environment.yml
   conda activate covid_dashboard_env

## Try it on Binder
You can interact with the project directly in your browser using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/theresarto/covid-dashboard/main?urlpath=voila/render/covid-dashboard.ipynb)

---

Feel free to explore and experiment with the data visualisations!
