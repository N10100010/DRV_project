from typing import Mapping, Optional
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity.retry import retry_if_result
from tenacity import Retrying

import logging
import requests
import pandas as pd
import numpy as np

from datetime import datetime

import logging

logger = logging.getLogger(__name__)

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


@retry(wait=wait_exponential(max=5), stop=stop_after_attempt(5))
def load_json(url: str, params=None, timeout=20., **kwargs):
    """
    Loads any json from any URL.
    todo: are we required to filter values on the fly?
     Do we have to have to possibility to get subsets from the api?
    """
    res = None
    try:
        res = requests.get(url, params=params, timeout=timeout, **kwargs)
        res.raise_for_status()
    except (Exception, ) as e:
        logger.error(f"Error appeared during get(). \n\tStatuscode: {res.status_code}\n\tURL: {url}")
        return {}


    if res.text and res.status_code != 404:
        return res.json()
    else:
        # todo: depending on how we want to use this function
        #  (with kwargs for filtering), we should either return an empty
        #  dict here or raise an error
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
        return [val if val not in ['0000-00-00 00:00:00', None, ''] else '1900-01-01 00:00:00' for val in values]

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
            elif v == "date":
                if np.mean(df[k].isna()) < .35:
                    # there are date columns that contain less than 24% data and these dates contain unknown timezones.
                    # Can we get the information if we need that data?
                    df[k] = [datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                             for val in _fix_date_values(df[k].values)]
                else:
                    logger.info(f"Skipping type-mapping: {k}:{v}. Less than 35% data present.")
            else:
                logger.warning(f"Received unknown type-mapping for {k}: {v}")
    except (ValueError, ) as e:
        raise e

    return df


def merge(dfs, **kwargs):
    left = dfs[0]
    n = len(dfs[1:])

    def iterate(val):
        if isinstance(val, tuple):
            return iter(val)
        else:
            return (val for _ in range(n))

    iter_kwargs = {k: iterate(val) for k, val in kwargs.items()}

    for right in dfs[1:]:
        kws = {
            k: next(val) for k, val in iter_kwargs.items()
        }
        left = pd.merge(left, right, **kws)

    return left
