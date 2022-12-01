
"""
####################################################################################################

This module extracts race data (speed[m/s] and stroke[1/m]) for each country per race and writes them to a json file.
Those files for which the extraction process fails, the corresponding URLs are written to a failed_requests.json file.

Basic stats:
* For the 1000 competition IDs provided by the API, there are approximately 11.700 race data pdfs.
* Processing time per pdf: approx. 1.8 - 2.5s
* Time to process 11.7k pdfs: approx. 7 hours
* Last test - successful extractions: 11092/11509 PDFs | (96,38%)

####################################################################################################
"""

import matplotlib.pyplot as plt
import collections
import traceback
import logging
import camelot  # on Mac via 'pip install camelot-py[cv]'
from tqdm import tqdm
import itertools
import numpy as np
import pandas as pd

from utils_general import write_to_json
from api import get_competition_ids, get_pdf_urls
from utils_pdf import (handle_table_partitions, get_data_loc, print_stats,
                       clean_df, get_string_loc, clean_convert_to_list, reset_axis, clean_str)

import logging
logger = logging.getLogger(__name__)

# CONSTANTS
JSON_INDENT_SIZE = 4
NO_OF_COMPETITIONS = 100


def df_to_json(df: pd.DataFrame) -> dict:
    """
    Extracts data (countries, ranks, data) from final dataframe and return json-like structure.
    """
    # Handle top part with countries and ranks
    df = clean_df(df)
    cnty_idx = get_string_loc(df, country=True)["cntry"]["row"]
    cnty_idx = cnty_idx[0] if cnty_idx else None
    rank_found = bool(get_string_loc(df, rank=True, column=0)["rank"]["row"])
    top_part = df.iloc[cnty_idx:cnty_idx+(2 if rank_found else 1)]
    top_df = reset_axis(top_part, axes=[0])

    # extract country codes
    country_data = top_df.iloc[0:1, ].values.flatten().tolist()
    country_list = [x.split('\n') for x in country_data if x]
    countries = list(itertools.chain(*country_list))
    countries = clean_str(countries, style="country")

    if rank_found:
        ranks = [x for x in np.concatenate(
            top_df.iloc[1:2, 1:].to_numpy()) if x]

    # Handle data part (incl. wrong column asignments where \n occurs)
    data_range = get_data_loc(df)
    data_df = df.iloc[data_range[0]:data_range[1]+1]

    placeholder_df = pd.DataFrame()
    for col in data_df.columns:
        if data_df[col].astype(str).str.contains('\n').any():
            new_cols = data_df[col].astype(str).str.split('\n', expand=True)
        else:
            new_cols = data_df[col]
        placeholder_df = pd.concat([placeholder_df, new_cols], axis=1)
    data_df = data_df.loc[:, (data_df != 0).any(axis=0)]
    data_df = clean_df(data_df)
    data_df = reset_axis(data_df, axes=[0, 1])
    # Create dict with relevant data and return as list of dicts.
    data, offset = {}, 0
    dist = clean_str(data_df[0].values, style="dist")

    for idx, country in enumerate(countries):
        speed = data_df.iloc[:, (idx + 1) + offset: (idx + 2) + offset]
        stroke = data_df.iloc[:, (idx + 2) + offset: (idx + 3) + offset]

        data[idx] = {
            "country": country,
            "rank": ranks[idx] if rank_found else None,
            "data": {
                "dist [m]": dist,
                "speed [m/s]": clean_convert_to_list(speed),
                "stroke": clean_convert_to_list(stroke)
            }
        }
        offset += 1
    return data


def extract_table_data(pdf_urls: list) -> tuple[list, list]:
    """
    Extracts data from given pdf urls using camelot-py.
    -----------------------
    Parameters:
    * pdf_urls:     List containing all urls linking to pdf files
    -----------------------
    Returns: tuple
    * List with json-like objects (final structure needs to be discussed) for each team per race
    * List containing the urls of all failed requests
    """
    json_lst, failed_requests,  = [], []
    errors, empty_files = 0, 0

    for url in tqdm(pdf_urls):
        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")
            df = handle_table_partitions(tables=tables, results=0)
            json_data = None if df.empty else df_to_json(df)

            if json_data:
                json_data["url"] = url
                json_lst.append(json_data)
                logging.info(f"Extract of {url.split('/').pop()} successful.")
            else:
                empty_files += 1
                logging.info(f"Empty file found: {url.split('/').pop()}.")

        except Exception as e:
            errors += 1
            failed_requests.append(url)
            logging.error(
                f"Error at {url}:\n{traceback.print_exc()}.\nErrors so far: {errors}.")

    # create extraction statistics
    total = len(pdf_urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors,
                empties=empty_files, rate=rate)

    return json_lst, failed_requests


competition_ids = get_competition_ids(years=2020)
pdf_urls = get_pdf_urls(comp_ids=competition_ids,
                        comp_limit=NO_OF_COMPETITIONS, results=0)[:10]  # [::15]
print(pdf_urls)

race_data, failed_req = extract_table_data(pdf_urls=pdf_urls)


write_to_json(data=race_data, filename="race_data")
write_to_json(data=failed_req, filename="race_data_failed")
