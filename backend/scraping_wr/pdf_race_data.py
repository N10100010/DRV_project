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
from statistics import mean, stdev
import camelot  # on Mac via 'pip install camelot-py[cv]'
from tqdm import tqdm
import itertools
import numpy as np
import pandas as pd

from utils_general import write_to_json
from api import get_competition_ids, get_pdf_urls
from utils_pdf import (handle_table_partitions, get_data_loc, print_stats,
                       clean_df, get_string_loc, check_speed_stroke, reset_axis, clean_str)

import logging

logger = logging.getLogger(__name__)


def df_to_json(df: pd.DataFrame) -> dict:
    """
    Extracts data (countries, ranks, data) from final dataframe and return json-like structure.
    """
    # Handle top part with countries and ranks
    df = clean_df(df)
    country_idx = get_string_loc(df, country=True)["cntry"]["row"]
    country_idx = country_idx[0] if country_idx else None
    rank_found = bool(get_string_loc(df, rank=True, column=0)["rank"]["row"])
    top_part = df.iloc[country_idx:country_idx + (2 if rank_found else 1)]
    top_df = reset_axis(top_part, axes=[0])

    # extract country codes
    country_data = top_df.iloc[0:1, ].values.flatten().tolist()
    # special codes for the country line, which could affect the detection --> must be excluded
    special_codes = ["NPC", "NOC"]
    country_list = [x.split('\n') for x in country_data if x and x not in special_codes]
    countries = list(itertools.chain(*country_list))
    countries = clean_str(countries, style="country")

    # handle ranks data
    ranks = None
    if rank_found:
        ranks = [x for x in np.concatenate(top_df.iloc[1:2, 1:].to_numpy()) if x]

    # Handle data part (incl. wrong column assignments where \n occurs)
    data_range = get_data_loc(df)
    data_df = df.iloc[data_range[0]:data_range[1] + 1]

    # split columns that are accidentally combined via linebreaks
    placeholder_df = pd.DataFrame()
    for col in data_df.columns:
        if data_df[col].astype(str).str.contains('\n').any():
            new_cols = data_df[col].astype(str).str.split('\n', expand=True)
        else:
            new_cols = data_df[col]
        placeholder_df = pd.concat([placeholder_df, new_cols], axis=1)
    data_df = placeholder_df.loc[:, (placeholder_df != 0).any(axis=0)].copy()
    data_df = reset_axis(clean_df(data_df), axes=[0, 1])

    # Create dict with relevant data and return as list of dicts.
    data, offset = {}, 0
    dist = clean_str(data_df[0].values, style="dist")

    for idx, country in enumerate(countries):
        speed_data = data_df.iloc[:, (idx + 1) + offset: (idx + 2) + offset]
        stroke_data = data_df.iloc[:, (idx + 2) + offset: (idx + 3) + offset]
        speeds = check_speed_stroke(speed_data, lb=0.01, ub=10.)
        strokes = check_speed_stroke(stroke_data, lb=15., ub=100.)
        rank = ranks[idx] if ranks else None

        data[idx] = {
            "country": country,
            "rank": rank,
            "data": {
                "dist [m]": dist,
                "speed [m/s]": speeds,
                "stroke": strokes
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
    data, failed_requests, = [], []
    errors, empty_files = 0, 0

    for url in tqdm(pdf_urls):
        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")
            df = handle_table_partitions(tables=tables, results=False)
            json_data = None if df.empty else df_to_json(df)

            if json_data:
                json_data["url"] = url
                data.append(json_data)
                logging.info(f"Extract of {url.split('/').pop()} successful.")
            else:
                empty_files += 1
                logging.info(f"Empty file found: {url.split('/').pop()}.")

        except Exception as e:
            errors += 1
            failed_requests.append(url)
            logging.error(f"Error at {url}:\n{traceback.print_exc()}.\nErrors so far: {errors}.")

    # create extraction statistics
    total = len(pdf_urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors, empties=empty_files, rate=rate)

    return data, failed_requests


for year in range(2010, 2022):
    competition_ids = get_competition_ids(years=year)
    pdf_urls = get_pdf_urls(comp_ids=competition_ids, comp_limit=1000, results=False)[::7]
    race_data, failed_req = extract_table_data(pdf_urls=pdf_urls)

# TODO: Append event/race id to final dict to match corresponding API data

#write_to_json(data=race_data, filename="race_data")
#write_to_json(data=failed_req, filename="race_data_failed")
