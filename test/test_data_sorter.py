import pandas as pd
from unittest.mock import patch, Mock, MagicMock, mock_open
from data_sorter import get_data, sort_data, latest_price
from random import choice, randint
from string import ascii_lowercase, digits


@patch('pandas.read_csv', autospec=True)
def test_get_data(mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame(
        {'A': ["some", "data"], 'B': ["more", "data"]})
    get_data()
    mock_read_csv.return_value = pd.DataFrame({})
    assert pd.errors.EmptyDataError
    mock_read_csv.side_effect = FileNotFoundError
    get_data()
    assert FileNotFoundError


def test_sort_data():
    mock_data_1 = pd.DataFrame({"Price": [randint(
        1, 100) for _ in range(100)], "Time": [''.join(choice(digits) for _ in range(5)) for _ in range(100)], "Trade Volume": [randint(
            1, 100) for _ in range(100)]})
    sort_data(data=mock_data_1)
    mock_data_2 = pd.DataFrame({"Price": [randint(
        1, 100) for _ in range(100)], "Timee": [''.join(choice(digits) for _ in range(5)) for _ in range(100)], "Trade Volume": [randint(
            1, 100) for _ in range(100)]})
    assert sort_data(data=mock_data_2) == None
    assert KeyError
    mock_data_3 = None
    sort_data(data=mock_data_3)
    assert AttributeError


def test_latest_price():
    mock_data = pd.DataFrame({"Price": [randint(1, 100) for _ in range(100)], "Time": [''.join(
        choice(digits) for _ in range(5)) for _ in range(100)], "Trade Volume": [randint(1, 100) for _ in range(100)]})
    assert latest_price(mock_data)
