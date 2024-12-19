import os
import json
from json.decoder import JSONDecodeError
import csv
import websockets
from websockets.exceptions import ConnectionClosedError
from websockets.legacy.client import connect, Connect
import asyncio
import datetime
import time
import signal
from argparse import ArgumentParser
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
start_time = time.time()


async def call_data(crypto_ticker: str, ws=None):
    req = '{"type":"subscribe","symbol":"BINANCE:%sUSDT"}' % crypto_ticker
    try:
        await ws.send(req)
        data = await ws.recv()
        return data
    except ConnectionClosedError as e:
        message = "There was an error closing the websocket connection. Attempting reconnect..."
        logger.info(f"---- {message} ----\n")
        e.rcvd = message
        pass


async def write_data(data: str | None, filepath=None):
    try:
        message_dict = json.loads(data)
        data_response = message_dict.get("data")
        logger.info(f"{data_response}\n")
        with open(filepath, "a", newline='') as file:
            csv_writer = csv.writer(file)
            for row in data_response:
                values = list(row.values())
                unix_time = values[3]/1000
                dt_value = datetime.datetime.fromtimestamp(
                    unix_time).strftime('%m-%d %H:%M:%S:%f')[:-4]
                value_write = [values[1], dt_value, values[4]]
                csv_writer.writerow(str(value) for value in value_write)
            return True
    except (TypeError, JSONDecodeError) as e:
        logger.warning(
            f"---- RESPONSE WARNING! DATA RECEIVED: {data} ----\n{e}")
        pass


async def time_limit_reached():
    return True


async def main(start_time=None):
    async with Connect(uri, ping_interval=None) as ws:
        # async with websockets.connect(uri, ping_interval=None) as ws:
        while True:
            current_time = time.time()
            if current_time - start_time < 180:
                data_to_send = asyncio.create_task(
                    call_data(crypto_ticker=crypto_ticker, ws=ws))
                await data_to_send
                data = data_to_send.result()
                send_data = asyncio.create_task(
                    write_data(data=data, filepath=filepath))
                await send_data
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(1)
                return await time_limit_reached()


def ticker_choice(choice: str | None):
    if choice == "Bitcoin":
        return "BTC"
    elif choice == "Ethereum":
        return "ETH"
    else:
        return "DOGE"


def loop_close_manager(loop=None, msg=None):
    loop.stop()
    loop.close()
    if loop.is_closed():
        logger.info(f"{msg}. Terminating subprocess...\n")
        return True


def loop_manager():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(main(start_time=start_time))

    try:
        loop.run_until_complete(task)
        msg = f"\n\n------- SSE LOOP TIME LIMIT REACHED -------\n\n"
        loop_close = loop_close_manager(loop=loop, msg=msg)
        logger.info(loop_close)
        process_id = os.getpid()
        os.kill(int(process_id), signal.SIGTERM)
    except ConnectionClosedError as e:
        msg = f"\n\n------- WEBSOCKET CONNECTION CLOSED: {e.rcvd} -------\n\n"
        return loop_close_manager(loop=loop, msg=msg)
    except KeyboardInterrupt:
        logger.info(f"------ SSE LOOP HAS BEEN STOPPED ------\n")
        return True


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--choice', help='currency choice', required=True)
    args = parser.parse_args()
    currency_choice = args.choice

    api_key = str(os.getenv('FINN', default=None))
    filepath = str(os.getenv('BCSV', default=None))
    uri = f"wss://ws.finnhub.io?token={api_key}"

    with open(filepath, "w", newline='') as file:
        csv_writer = csv.writer(file)
        order_keys = ["Price", "Time", "Trade Volume"]
        csv_writer.writerow(order_keys)

    crypto_ticker = ticker_choice(choice=currency_choice)

    loop_manager()
