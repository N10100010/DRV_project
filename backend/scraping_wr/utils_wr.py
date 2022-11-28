from tenacity import retry, wait_exponential, stop_after_attempt
from datetime import datetime
from typing import Union

import requests
import pandas as pd
import numpy as np


import logging
logger = logging.getLogger(__name__)

############################################################
## ABBREVIATIONS
#WR = WorldRowing


WR_FILTER_MAPPING = {
    'year': 'Year',
    'others': 'Others'
    # todo: extend me...
}


@retry(wait=wait_exponential(max=5), stop=stop_after_attempt(5))
def load_json(url: str, params=None, timeout=20., **kwargs):
    """
    Loads any json from any URL.
    The function will be retried, if the endpoint might not be reachable atm.
    ------------
    :param url: str - A url to an endpoint, that might contain a filter string.
    :param params: not used
    :param timeout: should stay at default (most of the time)
    :param kwargs: mostly not used
    :return: dict
    """
    res = None
    try:
        res = requests.get(url, params=params, timeout=timeout, **kwargs)
        res.raise_for_status()
    except (Exception, ) as e:
        logger.error(f"Error appeared during get(). \n\tStatuscode: {res.status_code}\n\tURL: {url}")
        return {}

    if res.text and res.status_code != 404:
        return res.json()['data']
    else:
        return {}


def stringify_params(val: Union[int, float, str, list]) -> str:
    """
    Stringifies a value
    ---------
    :param val: The parameter that will be stringified.
    :return: Stringified val
    """
    if isinstance(val, (str, int, float, np.int64)):
        return str(val)
    elif isinstance(val, list):
        return '||'.join(map(str, val))
    else:
        logger.error(f"Passed value of unknown type: {type(val)}. Allowed types: [str, int, np.int64, float, list]")


def build_filter_string(filter_params: dict) -> str:
    """
    -
    :param filter_params: dict - containing the parameters that are supposed to be filtered.
        example: {'year': 2010} OR {'year': [2010, 2012]}
        The passed value in the dict is allowed to be a list.

    :returns: returns the string containing the parameters for filtering the resulting json.
    """
    ret = '?'
    splitter = '&'
    schema = f'filter[KEY]=PARAM'

    if not set(filter_params.keys()).issubset(set(WR_FILTER_MAPPING.keys())):
        # the keys for filters start with capital letters. For ease of use, this is taken care of by the function.
        logger.error(f"A key of the passed filter is not allowed. Allowed filters: {list(WR_FILTER_MAPPING.keys())}")

    last_key = list(filter_params.keys())[-1]
    for k, v in filter_params.items():
        ret += schema.replace('KEY', WR_FILTER_MAPPING[k]).replace('PARAM', stringify_params(val=v))
        if k != last_key:
            ret += splitter

    return ret


def extract_competition_ids(values: dict) -> list[str]:
    """
    -
    @param values: dict - holding information about competitions
    @return: list[str] - list holding the competition ids
    """
    return [comp['id'] for comp in values]

########################################################################################################################
# NICK - OLD
########################################################################################################################


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
