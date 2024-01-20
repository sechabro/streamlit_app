import streamlit as st
import pandas as pd
import numpy as np
import os
import time

price_set = 0
st.set_page_config(layout="wide")
st.header('Binance: BTCUSDT Trade Volume', divider=True)
filepath = filepath = str(os.getenv('BCSV', default=None))

DATE_COLUMN = 'date/time'
DATA_URL = (filepath)


# @st.cache_data
def get_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_URL)
    rev_data = data[::-1]
    # last_60 = data.tail(60)
    new_data = pd.DataFrame({
        "Price": [],
        "Time": [],
        "Buy Volume": [],
        "Sell Volume": []
    })

    time_units = []
    for row_index in rev_data.index:
        new_row = {"Price": rev_data['Price'][row_index],
                   "Time": rev_data['Time'][row_index]}
        if rev_data["Trade Volume"][row_index] > 0:
            new_row["Buy Volume"] = rev_data["Trade Volume"][row_index]
        elif rev_data["Trade Volume"][row_index] < 0:
            new_row["Sell Volume"] = rev_data["Trade Volume"][row_index]
        if rev_data["Time"][row_index] not in time_units:
            new_data.loc[len(new_data)] = new_row
            time_units.append(rev_data["Time"][row_index])
        elif rev_data["Time"][row_index] in time_units:
            new_data.loc[len(new_data)] = new_row
        if len(time_units) == 25:
            return new_data
        else:
            continue
    # return new_data


data = get_data()
price_column = data.get('Price')
column_last = price_column.tail(1)
text_display = st.subheader(body="Current Trading Price: :green[{price:.2f}]".format(
    price=column_last.iloc[0]), help="price based on most recent trade in dataset")

bar = st.bar_chart(data=data, x='Time',
                   y=['Buy Volume', 'Sell Volume'], color=["#79ea86", "#e75757"], height=500, width=1200, use_container_width=True)


time.sleep(2)
st.rerun()
