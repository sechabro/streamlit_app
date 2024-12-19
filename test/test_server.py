import signal
from unittest.mock import patch, Mock, MagicMock, mock_open, AsyncMock
from json.decoder import JSONDecodeError
from websockets.exceptions import ConnectionClosedError
import websockets
from websockets.legacy.client import Connect, WebSocketCommonProtocol
import asyncio
import pytest
from asyncio import new_event_loop, set_event_loop, Task, create_task
from server.server import loop_manager, loop_close_manager, ticker_choice, main, write_data, call_data, time_limit_reached
import time


def test_ticker_choice():
    choice = "Bitcoin"
    assert ticker_choice(choice=choice) == "BTC"
    choice = "Ethereum"
    assert ticker_choice(choice=choice) == "ETH"
    choice = "Dogecoin"
    assert ticker_choice(choice=choice) == "DOGE"


def test_loop_close_manager():
    loop = asyncio.new_event_loop()
    assert loop_close_manager(loop=loop) == True


@patch('csv.writer')
@pytest.mark.asyncio
async def test_write_data(mock_writer):
    mock_data = "{\"data\": [{\"row1a\": \"data\", \"row1b\": \"more data\", \"row1c\": \"yet more data\", \"row1d\": 400, \"row1e\": \"no not data\"}]}"
    filepath = "/some/filepath"
    with patch("builtins.open"):
        await write_data(data=mock_data, filepath=filepath)
        mock_writer.assert_called_once()
        assert await write_data(data=mock_data, filepath=filepath) == True

    mock_data = None
    with patch("builtins.open"):
        await write_data(data=mock_data, filepath=filepath)
        assert TypeError

    mock_data = "wrong kind of string"
    with patch("builtins.open"):
        await write_data(data=mock_data, filepath=filepath)
        assert JSONDecodeError


@pytest.mark.asyncio
async def test_time_limit_reached():
    assert await time_limit_reached() == True


async def send(msg):
    return


async def recv():
    return "data"


@pytest.mark.asyncio
async def test_call_data():
    mock_ticker = 'BTC'
    mock_websocket = Connect
    mock_websocket.ping_interval = None
    mock_websocket.uri = f"wss://ws.uri.io"
    mock_websocket.send = send
    mock_websocket.recv = recv
    assert await call_data(crypto_ticker=mock_ticker, ws=mock_websocket) == "data"


'''@patch('asyncio.create_task')
@patch('websockets.legacy.client.Connect')
@pytest.mark.asyncio
async def test_main(mock_connect, mock_create_task):

    mock_connect.uri = "wss://ws.url.io"
    mock_connect.ping_interval = None
    mock_start_time = time.time()

    with mock_connect:
        mock_create_task.side_effect = [
            [{"some": "data"}], [{"some more": "data"}]]
        await main(start_time=mock_start_time)'''
