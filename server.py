import os
import json
import csv
import finnhub as fn
import websockets
from websockets.exceptions import ConnectionClosedError as cce
import asyncio
import datetime
import random


async def call_data(ws=None):
    req = '{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}'
    try:
        await ws.send(req)
        data = await ws.recv()
        print(f'response received: {data}\n')
        return data
    except cce as e:
        print(
            f'Connection Closed Error rcvd: {e.rcvd}, sent: {e.sent}, rts: {e.rcvd_then_sent}\nWaiting for 5 seconds...')
        await asyncio.sleep(5)


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


async def main():
    async with websockets.connect(uri, ping_interval=None) as ws:
        while True:
            data_to_send = asyncio.create_task(call_data(ws=ws))
            await data_to_send
            data = data_to_send.result()
            send_data = asyncio.create_task(write_data(data=data))
            await send_data
            await asyncio.sleep(2)

if __name__ == "__main__":
    api_key = str(os.getenv('FINN', default=None))
    filepath = str(os.getenv('BCSV', default=None))
    uri = f"wss://ws.finnhub.io?token={api_key}"

    if os.path.isfile(filepath) == True:
        os.remove(filepath)
        print(f'\n\n-------- {filepath} REMOVED. STARTING SSE NOW -------\n\n')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
        print(f"\n\n------- SSE LOOP HAS BEEN STOPPED -------\n\n")
