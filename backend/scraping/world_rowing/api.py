import requests
import utils

import pandas as pd

# CONSTANTS
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"


def load_json(url: str, params=None, timeout=20., **kwargs):
    r = requests.get(url, params=params, timeout=timeout, **kwargs)
    r.raise_for_status()
    if r.text:
        return r.json()
    else:
        return {}


def pre_process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies date- and binary-columns and transforms their types.

    FYI: since python >= 3.9, one can merge dict's the following way:
        d1 = {1:1, 2:2}
        d2 = {2:2, 3:3}
        d1 | d2 == {1: 1, 2: 2, 3: 3}
    """
    date_cols = _get_date_columns(df.columns.to_list())
    binary_cols = _get_binary_columns(df)

    date_cols = {k: "date" for k in date_cols}
    binary_cols = {k: "bool" for k in binary_cols}

    _dict = date_cols | binary_cols

    df = _alter_dataframe_column_types(df, _dict)

    return df


def get_dataframe_from_dict(dictionary: dict) -> pd.DataFrame:
    assert ("data" in dictionary.keys())
    return pd.DataFrame.from_dict(dictionary['data'])


def get_competitions(year: int = None, kind: str = None):
    _json_dict = load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITION}')
    df = get_dataframe_from_dict(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_races(year: int = None, kind: str = None):
    _json_dict = load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_RACE}')
    df = get_dataframe_from_dict(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_events(year: int = None, kind: str = None):
    _json_dict = load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_EVENT}')
    df = get_dataframe_from_dict(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df
