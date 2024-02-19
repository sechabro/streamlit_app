import importlib
import time
import pandas as pd
import streamlit as st
data_sorter = importlib.import_module('data_sorter')


data = data_sorter.get_data()
sorted_data = data_sorter.sort_data(data)
st.set_page_config(
    page_title="Binance BTCUSDT Real-Time Trade Volume Data", layout="wide")

with st.sidebar:
    st.subheader(body="About this Websocket Application")
    st.text_area(height=550, label='label', value='This websocket demo application displays live trading data from Binance, via the Finnhub API.'
                 ' A call is made to the API every 2 seconds, the data is processed, and presented on this moving bar chart.'
                 ' The y-axis represents BTC trading volume in BTC, and the x-axis represents the time at which trading action occurred.'
                 ' The timestamps are in ascending order from right to left.'
                 ' Data collection occurs for 3 minutes, and ceases upon reaching the time limit.', label_visibility="collapsed")

if sorted_data is not None:
    st.header('Binance: BTCUSDT Trade Volume', divider=True)
    price = data_sorter.latest_price(sorted_data)
    text_display = st.subheader(body="Currently Trading at {price:.2f}".format(
        price=price), help="price based on most recent trade in dataset")

    bar = st.bar_chart(data=sorted_data, x='Time',
                       y=['Buy Volume', 'Sell Volume'], color=["#79ea86", "#e75757"], height=550, width=1200, use_container_width=True)

    time.sleep(2)
    st.rerun()

else:
    with st.spinner(text=f"Data populating. This usually takes around a minute"):
        time.sleep(7)
    st.rerun()
