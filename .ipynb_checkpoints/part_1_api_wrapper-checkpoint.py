import requests
import time
import json
import pandas as pd


class APIwrapper:
    # class variables shared among all instances
    _access_point = "https://api.ukhsa-dashboard.data.gov.uk"
    _last_access = 0.0  # time of last api access

    def __init__(self, theme, sub_theme, topic, geography_type, geography, metric):
        """ Init the APIwrapper object, constructing the endpoint from the structure
        parameters """
        # build the path with all the required structure parameters. You do not need to edit this line,
        # parameters will be replaced by the actual values when you instantiate an object of the class!
        url_path = (f"/themes/{theme}/sub_themes/{sub_theme}/topics/{topic}/geography_types/" +
                    f"{geography_type}/geographies/{geography}/metrics/{metric}")
        # our starting API endpoint
        self._start_url = APIwrapper._access_point + url_path
        self._filters = None
        self._page_size = -1
        # will contain the number of items
        self.count = None

    def get_page(self, filters={}, page_size=5):
        """ Access the API and download the next page of data. Sets the count
        attribute to the total number of items available for this query. Changing
        filters or page_size will cause get_page to restart from page 1. Rate
        limited to three request per second. The page_size parameter sets the number
        of data points in one response page (maximum 365); use the default value 
        for debugging your structure and filters. """
        # Check page size is within range
        if page_size > 365:
            raise ValueError("Max supported page size is 365")
        # restart from first page if page or filters have changed
        if filters != self._filters or page_size != self._page_size:
            self._filters = filters
            self._page_size = page_size
            self._next_url = self._start_url
        # signal the end of data condition
        if self._next_url == None:
            return []  # we already fetched the last page
        # simple rate limiting to avoid bans
        curr_time = time.time()  # Unix time: number of seconds since the Epoch
        deltat = curr_time - APIwrapper._last_access
        if deltat < 0.33:  # max 3 requests/second
            time.sleep(0.33 - deltat)
        APIwrapper._last_access = curr_time
        # build parameter dictionary by removing all the None
        # values from filters and adding page_size
        parameters = {x: y for x, y in filters.items() if y != None}
        parameters['page_size'] = page_size
        # the page parameter is already included in _next_url.
        # This is the API access. Response is a dictionary with various keys.
        # the .json() method decodes the response into Python object (dictionaries,
        # lists; 'null' values are translated as None).
        response = requests.get(self._next_url, params=parameters).json()
        # update url so we'll fetch the next page
        self._next_url = response['next']
        self.count = response['count']
        # data are in the nested 'results' list
        return response['results']

    def get_all_pages(self, filters={}, page_size=365):
        """ Access the API and download all available data pages of data. Sets the count
        attribute to the total number of items available for this query. API access rate
        limited to three request per second. The page_size parameter sets the number
        of data points in one response page (maximum 365), and controls the trade-off
        between time to load a page and number of pages; the default should work well 
        in most cases. The number of items returned should in any case be equal to 
        the count attribute. """
        data = []  # build up all data here
        while True:
            # use get_page to do the job, including the pacing
            next_page = self.get_page(filters, page_size)
            if next_page == []:
                break  # we are done
            data.extend(next_page)
        return data


def fetch_data_with_wrapper(geography_type, borough, metric_name):
    """
    Fetch all pages of data for a given metric using the APIwrapper.
    Returns a Pandas DataFrame.
    """
    structure = {
        "theme": "infectious_disease",
        "sub_theme": "respiratory",
        "topic": "COVID-19",
        "geography_type": geography_type,
        "geography": borough,
        "metric": metric_name,
    }

    api = APIwrapper(**structure)

    try:
        data = api.get_all_pages()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching data for metric {metric_name}: {e}")
        return pd.DataFrame()