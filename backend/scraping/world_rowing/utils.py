import requests
import pandas as pd
import numpy as np


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

# HELPER FUNCTIONS FOR UTILS
def _get_date_columns(str_list: list) -> list:
    """
    return: list of columns that contain 'date' in their name
    """
    lower = [s.lower() for s in str_list]
    filtered = list(filter(lambda x: "date" in x, lower))

    if len(filtered) > 0:
        return [str_list[lower.index(k)] for k in filtered]
    else:
        return []


def _get_binary_columns(df: pd.DataFrame) -> list:
    """
    return: list of columns with potentially binary data
    """
    return df.loc[:, df.isin([0, 1, np.nan])].columns.to_list()


def _alter_dataframe_column_types(df: pd.DataFrame, type_mapping: dict[str, str]) -> pd.DataFrame:
    """
    return: DataFrame with altered types, according to `type_mapping`
    """
    # TODO: adjust me if we use python >= 3.10
    #  switch/case would be the call here. That is only present in python >= 3.10
    assert (set(type_mapping.keys()).issubset(set(df.columns.to_list())))

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
            df[k] = pd.to_datetime(df[k])
        else:
            # log / error
            print("PANIC!!!")

    return df
