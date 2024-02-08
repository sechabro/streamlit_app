import importlib
import time
import pandas as pd
import streamlit as st
data_sorter = importlib.import_module('data_sorter')


data = data_sorter.get_data()
sorted_data = data_sorter.sort_data(data)
st.set_page_config(
    page_title="Binance BTCUSDT Real-Time Trade Volume Data", layout="wide")

if sorted_data is not None:
    st.header('Binance: BTCUSDT Trade Volume', divider=True)
    price = data_sorter.latest_price(sorted_data)
    text_display = st.subheader(body="Current Trading Price: :green[{price:.2f}]".format(
        price=price), help="price based on most recent trade in dataset")

    bar = st.bar_chart(data=sorted_data, x='Time',
                       y=['Buy Volume', 'Sell Volume'], color=["#79ea86", "#e75757"], height=600, width=1200, use_container_width=True)

    time.sleep(2)
    st.rerun()

else:
    with st.spinner(text=f"Please wait while data is populating..."):
        time.sleep(7)
    st.rerun()
