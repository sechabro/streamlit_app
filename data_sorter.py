import pandas as pd
import os

filepath = str(os.getenv('BCSV', default=None))
DATA_URL = (filepath)


def get_data() -> pd.DataFrame:
    try:
        data = pd.read_csv(DATA_URL)
        rev_data = data[::-1]
        return rev_data
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return None


def sort_data(data) -> pd.DataFrame:
    try:
        new_data = pd.DataFrame({
            "Price": [],
            "Time": [],
            "Volume": []
        })

        time_units = {}
        for row_index in data.index:
            new_row = {"Price": data["Price"][row_index],
                       "Time": data["Time"][row_index],
                       "Volume": data["Trade Volume"][row_index]}

            # Adding a new row and adding timestamp to time_units if it doesn't exist already. Otherwise just adding the row.
            if not time_units.get(str(data["Time"][row_index])):
                new_data.loc[len(new_data)] = new_row
                time_units[str(data["Time"][row_index])] = True
            elif time_units.get(str(data["Time"][row_index])):
                new_data.loc[len(new_data)] = new_row

            # Returning dataframe when time_units array contains 20 unique units of time.
            if len(time_units) == 20:
                return new_data
            else:
                continue
    except (AttributeError, KeyError):
        return None


def latest_price(data):
    price_column = data.get('Price')
    column_last = price_column.tail(1)
    latest_price = column_last.iloc[0]
    return latest_price
