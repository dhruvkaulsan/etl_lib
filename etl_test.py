import datetime
import requests
from typing import (
    Dict,
)

import pandas as pd
from pandas.tseries.offsets import BDay

API_KEY = r"XIO28NTCLFY0XJ85"
BASE_URL = r"https://www.alphavantage.co/query?"


def generic_make_av_request(query: Dict[str, str]) -> Dict:
    """Returns JSON from API request. Intended to be used inside of metric
    specific wrappers.
    """

    # TODO: add try/except here

    # can do a nested list comp join also
    str_query = str(query).replace('{', '').replace('}', '').replace("'", "").replace(": ", "=", ).replace(", ", "&", )
    request_url = f"{BASE_URL}{str_query}&apikey={API_KEY}"
    response = requests.get(request_url)
    json_data = response.json()
    return json_data


def get_px_df_for_single_ticker(
        ticker_name: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
):
    # need to confirm if order matters
    query = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': ticker_name,
        'outputsize': 'full',
    }

    px_json_data = generic_make_av_request(query)

    df_px = pd.DataFrame(
        px_json_data['Time Series (Daily)'],
    ).transpose()

    dict_rename_map = {
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. adjusted close': 'AdjClose',
        '6. volume': 'Volume',
        '7. dividend amount': 'DividendAmount',
        '8. split coefficient': 'SplitCoefficient',
    }

    df_px.index = pd.to_datetime(df_px.index)
    df_px = df_px.rename(columns=dict_rename_map)
    df_px = df_px.astype(dtype={col: float for col in df_px.columns})
    df_px = df_px.sort_index()

    df_px = df_px.loc[
        lambda x: (x.index >= start_date) & (x.index <= end_date)
    ]

    print(df_px.head())
    print('SUCCESSFULLY GOT PRICE DATA')
    return df_px


if __name__ == '__main__':
    res = get_px_df_for_single_ticker(
        ticker_name='IBM',
        end_date=(datetime.datetime.now().date() - BDay(1)).to_pydatetime(),
        start_date=datetime.datetime(2000, 1, 1)
    )

