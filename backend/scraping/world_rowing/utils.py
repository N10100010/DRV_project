from typing import Mapping, Optional
#from tenacity import retry, wait_exponential, stop_after_attempt

import requests
import pandas as pd
import numpy as np

from datetime import datetime

############################################################
## ABBREVIATIONS
#WR = WorldRowing

############################################################
# CONSTANTS
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"
############################################################


class Pipeline:
    """
    arguably if this has to be a class.
    Why? because the functions would be fixed and one would want to instantiate a pipeline for a purpose
    """
    functions: list
    default_kwargs: Optional[list[dict]]

    def __init__(self, functions: list, default_kwargs: Optional[list[dict]]):
        self.functions = functions
        self.default_kwargs = default_kwargs

    def __call__(self, df, kwargs_list):
        if kwargs_list is None:
            if self.default_kwargs is None:
                kwargs_list = {}
            else:
                kwargs_list = self.default_kwargs

        for func, kwargs in zip(self.functions, kwargs_list):
            if kwargs is None:
                kwargs = {}
            df = func(df, **kwargs)

        return df


#@retry(wait=wait_exponential(max=42), stop=stop_after_attempt(10))
def load_json(url: str, params=None, timeout=20., **kwargs):
    """
    Loads any json from any URL.
    todo: are we required to filter values on the fly?
     Do we have to have to possiblity to get subsets from the api?
    todo: do the retry, in dependence of the response
    """
    res = requests.get(url, params=params, timeout=timeout, **kwargs)
    res.raise_for_status()
    if res.text:
        return res.json()
    else:
        return {}


def extract_rsc_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies rsc-code columns, extracts the code from the values and adds them as separate column/s.
    The original columns will be suffixed with '_ORG' and the new values will replace the existing ones.

    NOTE: the function can be called without changing the df,
        IF there are no column names, containing the substring 'rsccode'
    """

    def _extract_code(val: str) -> str:
        return val.split('---')[0]

    rsc_col_names = df.filter(like='rsccode').columns.to_list()
    # usually, the rcs_col_names should not be longer than 2 and generally only 1
    for col in rsc_col_names:
        df[f'{col}_ORG'] = df[col]
        df[col] = df[col].map(_extract_code)

    return df


def preprocess_json_to_dataframe(json: dict) -> pd.DataFrame:
    """
    return: dataframe with lowered column names from WR json
    """
    assert ("data" in json.keys())
    df = pd.DataFrame.from_dict(json['data'])
    df.columns = string_list_lower(df.columns.to_list())
    return df


def get_date_columns(str_list: list) -> list:
    """
    return: list of columns that contain 'date' in their name
    """
    lower = [s.lower() for s in str_list]
    filtered = list(filter(lambda x: "date" in x, lower))

    if len(filtered) > 0:
        return [str_list[lower.index(k)] for k in filtered]
    else:
        return []


def get_binary_columns(df: pd.DataFrame) -> list:
    """
    return: list of columns with potentially binary data
    """
    is_binary = df.isin([0., 1., 0, 1, np.nan]).any()
    return [is_binary.index[i] for i, val in enumerate(is_binary) if val]


def string_list_lower(l: list) -> list:
    """
    Applies the lower-func to the columns of a dataframe.
    """
    return [col_name.lower() for col_name in l]


def alter_dataframe_column_types(df: pd.DataFrame, type_mapping: dict[str, str]) -> pd.DataFrame:
    """
    return: DataFrame with altered types, according to `type_mapping`
    """

    def _fix_date_values(values: list[str]) -> list[str]:
        """
        replace not-allowed values for date-parsing
        """
        return [val if val != '0000-00-00 00:00:00' else '1900-00-00 00:00:00' for val in values]

    # TODO: adjust me if we use python >= 3.10
    #  switch/case would be the call here. That is only present in python >= 3.10
    #  UPGRADE TO python 3.10
    assert (set(type_mapping.keys()).issubset(set(df.columns.to_list())))

    try:
        for k, v in type_mapping.items():
            if v == "str":
                df[k] = df[k].astype(str)
            elif v == "int":
                df[k] = df[k].astype(int)
            elif v == "float":
                df[k] = df[k].astype(float)
            elif v == "bool":
                df[k] = df[k].astype(bool)
            #elif v == "date":  # todo: how does that fail?!
            #    df[k] = [datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
            #             for val in _fix_date_values(df[k].values)]
            else:
                # log / error
                print("PANIC!!!")
    except (ValueError, ) as e:  # todo: enter errors that could occur here
        raise e

    return df
