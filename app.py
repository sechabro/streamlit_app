import importlib
import time
import pandas as pd
import streamlit as st
data_sorter = importlib.import_module('data_sorter')


st.set_page_config(layout="wide")
st.header('Binance: BTCUSDT Trade Volume', divider=True)


data = data_sorter.get_data()
sorted_data = data_sorter.sort_data(data)
price = data_sorter.latest_price(sorted_data)

text_display = st.subheader(body="Current Trading Price: :green[{price:.2f}]".format(
    price=price), help="price based on most recent trade in dataset")

bar = st.bar_chart(data=sorted_data, x='Time',
                   y=['Buy Volume', 'Sell Volume'], color=["#79ea86", "#e75757"], height=500, width=1200, use_container_width=True)

time.sleep(2)
st.rerun()
