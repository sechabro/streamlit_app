import os
from signal import SIGKILL
import json
import csv
import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
from asyncio import Future, InvalidStateError
import datetime
import random
import time
import sys

start_time = time.time()


async def call_data(ws=None):
    req = '{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}'
    try:
        await ws.send(req)
        data = await ws.recv()
        print(f'response received: {data}\n')
        return data
    except ConnectionClosedError as e:
        message = "There was an error closing the websocket connection. Attempting reconnect..."
        e.rcvd = message
        pass


async def write_data(data=None):
    try:
        message_dict = json.loads(data)
        data_response = message_dict.get("data")
        if os.path.isfile(filepath) == True:
            with open(filepath, "a", newline='') as file:
                csv_writer = csv.writer(file)
                for row in data_response:
                    values = list(row.values())
                    unix_time = values[3]/1000
                    dt_value = datetime.datetime.fromtimestamp(
                        unix_time).strftime('%m-%d %H:%M:%S:%f')[:-4]
                    trade_type = random.choice([values[4], -values[4]])
                    value_write = [values[1], dt_value, trade_type]
                    csv_writer.writerow(str(value) for value in value_write)
        else:
            with open(filepath, "w", newline='') as file:
                csv_writer = csv.writer(file)
                order_keys = ["Price", "Time", "Trade Volume"]
                csv_writer.writerow(order_keys)
                for row in data_response:
                    values = list(row.values())
                    unix_time = values[3]/1000
                    dt_value = datetime.datetime.fromtimestamp(
                        unix_time).strftime('%m-%d %H:%M:%S:%f')[:-4]
                    trade_type = random.choice([values[4], -values[4]])
                    value_write = [values[1], dt_value, trade_type]
                    csv_writer.writerow(str(value) for value in value_write)
    except TypeError as e:
        print(f'ERROR: {e}\nDATA RECEIVED: {data}')
        pass


async def time_limit_reached():
    return True


async def main(start_time=None):
    async with websockets.connect(uri, ping_interval=None) as ws:
        while True:
            current_time = time.time()
            if current_time - start_time < 180:
                data_to_send = asyncio.create_task(call_data(ws=ws))
                await data_to_send
                data = data_to_send.result()

                # if data.rcvd:
                #    asyncio.sleep(5)
                #    raise ConnectionClosedError(
                #        rcvd=f'Connection Closed Error. Received: {data.rcvd}, Sent: {data.sent}, Received then Sent: {data.rcvd_then_sent}\n')

                send_data = asyncio.create_task(write_data(data=data))
                await send_data
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(1)
                return await time_limit_reached()


def loop_close_manager(loop=None, msg=None):
    loop.stop()
    loop.close()
    if loop.is_closed():
        print(msg)
        return True


def loop_manager():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(main(start_time=start_time))

    try:
        loop.run_until_complete(task)
        msg = f"\n\n------- SSE LOOP TIME LIMIT REACHED -------\n\n"
        return loop_close_manager(loop=loop, msg=msg)
    except ConnectionClosedError as e:
        msg = f"\n\n------- WEBSOCKET CONNECTION CLOSE ERROR: {e.rcvd} -------\n\n"
        return loop_close_manager(loop=loop, msg=msg)
    except KeyboardInterrupt:
        print(f"\n\n------- SSE LOOP HAS BEEN STOPPED -------\n\n")
        return True


if __name__ == "__main__":
    api_key = str(os.getenv('FINN', default=None))
    filepath = str(os.getenv('BCSV', default=None))
    uri = f"wss://ws.finnhub.io?token={api_key}"

    if os.path.isfile(filepath) == True:
        os.remove(filepath)
        print(f'\n\n-------- {filepath} REMOVED. STARTING SSE NOW -------\n\n')

    loop_manager()
