import pandas as pd
import os

filepath = str(os.getenv('BCSV', default=None))
DATA_URL = (filepath)


def get_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_URL)
    rev_data = data[::-1]
    return rev_data


def sort_data(data) -> pd.DataFrame:
    new_data = pd.DataFrame({
        "Price": [],
        "Time": [],
        "Buy Volume": [],
        "Sell Volume": []
    })

    time_units = {}
    for row_index in data.index:
        new_row = {"Price": data['Price'][row_index],
                   "Time": data['Time'][row_index]}
        if data["Trade Volume"][row_index] > 0:
            new_row["Buy Volume"] = data["Trade Volume"][row_index]
        elif data["Trade Volume"][row_index] < 0:
            new_row["Sell Volume"] = data["Trade Volume"][row_index]

        # Adding a new row and adding timestamp to time_units if it doesn't exist already. Otherwise just adding the row.
        if not time_units.get(str(data["Time"][row_index])):
            new_data.loc[len(new_data)] = new_row
            time_units[str(data["Time"][row_index])] = True
        elif time_units.get(str(data["Time"][row_index])):
            new_data.loc[len(new_data)] = new_row

        # Returning dataframe when time_units array contains 30 unique units of time.
        if len(time_units) == 70:
            return new_data
        else:
            continue


def latest_price(data):
    price_column = data.get('Price')
    column_last = price_column.tail(1)
    latest_price = column_last.iloc[0]
    return latest_price
