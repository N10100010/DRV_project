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


class Pipeline:
    """
    arguable if this has to be a class.
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
