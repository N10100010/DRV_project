import backend.scraping.world_rowing.utils as ut
import pandas as pd

# CONSTANTS
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"

PIPE_PRE_PROCESS = ut.Pipeline(
    functions=[ut.alter_dataframe_column_types, ut.extract_rsc_codes],
    default_kwargs=None
)


def _pre_process_to_dataframe(_dict: dict) -> pd.DataFrame:
    """
    Identifies date- and binary-columns and transforms their types.

    FYI: since python >= 3.9, one can merge dict's the following way:
        d1 = {1:1, 2:2}
        d2 = {2:2, 3:3}
        d1 | d2 == {1: 1, 2: 2, 3: 3}
    """
    df = ut.preprocess_json_to_dataframe(_dict)

    date_cols = ut.get_date_columns(df.columns.to_list())
    binary_cols = ut.get_binary_columns(df)

    date_cols = {k: "date" for k in date_cols}
    binary_cols = {k: "bool" for k in binary_cols}
    datatypes = {'type_mapping': date_cols | binary_cols}

    return PIPE_PRE_PROCESS(df, kwargs_list=[datatypes, None])


def get_competitions(year: int = None, kind: str = None):
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITION}')
    df = _pre_process_to_dataframe(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_races(year: int = None, kind: str = None):
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_RACE}')
    df = _pre_process_to_dataframe(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_events(year: int = None, kind: str = None):
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_EVENT}')
    df = _pre_process_to_dataframe(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df
