import streamlit as st
import time
import os
import importlib
utils = importlib.import_module('utils')
data_sorter = importlib.import_module('data_sorter')
session = st.session_state
choice = session.get("choice")
csv = session.get("datacsv")
data = data_sorter.get_data()


st.set_page_config(
    page_title=f"{choice} Real-Time Trade Volume Data", layout="wide")

###### ERROR HANDLING FOR BROWSER REFRESH & EDGE CASE ######


def check_session_reset():
    if choice == None:
        container = st.container(height=60, border=False)
        container.error(body=f"Session has been reset.\n"
                        "Please return to the homepage and begin another session.", icon=":material/thumb_down:")
        kill_server = utils.server_search_and_terminate(script="server.py")
        print(kill_server)
        container2 = st.container(height=60, border=False)
        if container2.button("Home"):
            st.switch_page("app.py")
    else:
        return False


def csv_deleted():
    container = st.container(height=60, border=False)
    container.error(body=f"You need to choose a cryptocurrency first.\n"
                    "Please return to the homepage and choose.", icon=":material/thumb_down:")
    container2 = st.container(height=60, border=False)
    if container2.button("Home"):
        st.switch_page("app.py")


def run_page_2():
    ####### WHEN FULL DATAFRAME IS RETURNED ######
    sorted_data = data_sorter.sort_data(data)
    if sorted_data is not None:
        st.header(
            f'{choice} - USDT Trade Volume')
        st.divider()
        price = data_sorter.latest_price(sorted_data)
        col1, col2 = st.columns(
            spec=[0.65, 0.35], gap="large", vertical_alignment="center")
        col1.bar_chart(data=sorted_data, x='Time', y=['Volume'], color=[
            "#79ea86"], height=500, use_container_width=True, horizontal=True)
        col2.subheader(body="Currently trading at {price:.2f}".format(
            price=price), help="price based on most recent trade in dataset", divider=True)
        col2.write(f'Displaying current trade volume for {choice}.\n'
                   'This data being received, though minimal, is important in\n'
                   'knowing the amount of action on a particular cryptocurrency\n'
                   'at any given moment.\n\n'
                   'Much of the volume data contains multiple trades at the same\n'
                   'price, split into separate lines. This manifests visually as a\n'
                   '\"stacking\" effect on any bar in the graph.\n\n'
                   'Click \"Back\" to return to the home page. Click \"Next\" for github\n'
                   'repo link.')

        button_container = col2.container(height=100, border=False)
        col3, col5, col4 = button_container.columns(
            spec=[.3, .4, .4], vertical_alignment="bottom")
        if col3.button("Back"):
            st.switch_page("app.py")
        elif col4.button("Next"):
            st.switch_page("pages/page_3.py")
        time.sleep(1)
        st.rerun()

    ###### WHILE DATAFRAME IS STILL PROCESSING ######
    else:
        st.divider()
        with st.spinner(text=f"Data populating. This usually takes around a minute"):
            time.sleep(7)
        st.rerun()


session_reset = check_session_reset()
if session_reset == False and csv != None:
    if os.path.isfile(csv) == True:
        run_page_2()
    if os.path.isfile(csv) == False:
        csv_deleted()
