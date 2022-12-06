"""
####################################################################################################

This module extracts the data from results pdf files.

Example file:
https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/JWCH_2014/JWCH_2014_ROWWSCULL1--J---------SFNL000100--_C73X4443.pdf

Basic stats:
* Extraction time per file: approx. 1.2 - 1.6s
####################################################################################################
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import camelot
import re

from utils_pdf import (clean, clean_df, get_string_loc,
                       handle_table_partitions, clean_str, convert_string_to_sec, print_stats)
from utils_general import write_to_json
from api import get_competition_ids, get_pdf_urls

import logging

logger = logging.getLogger(__name__)

NO_OF_COMPETITIONS = 300
# dist includes basic 500m interval and 250m para intervals
DISTS = ['250', '500', '750', '1000', '1500', '2000']
SPECIAL_VALUES = ["dna", "DNS", "DNF", "BUW"]
MEANS = [102.73, 209.96, 314.81, 424.03]
STDS = [17.7, 31.9, 37.7, 103.9]


def get_athletes(df: pd.DataFrame, rows: int, i: int, n_loc: list) -> list:
    """
    Handles extraction of athlete names.
    -----------------------
    Parameters:
    * df:       DataFrame
    * c_row:    Row index of country, a.k.a. start point of names for given country
    * i:        Index of current country with regard to countries in given pdf
    * n_loc:    List with column indices for columns containing names
    -----------------------
    Returns:    List with athlete names
    """
    # slice part of dataframe containing athlete names for given country
    # rows: starts at row of current country, ends at row of following country
    # cols: starts at first occurrence of name col and ends at last occurrence of name col
    start_row = rows[i]
    end_row = rows[i + 1] if (i + 1 < len(rows)) else df.shape[0]
    start_col = n_loc[0]
    # extra margin because some names are one column right of where the names string was found
    end_col = n_loc[len(n_loc) - 1] + 2
    athlete_df = df.iloc[start_row:end_row, start_col:end_col]
    # remove none values and convert to 1-d list
    names = athlete_df.dropna().values.reshape(-1)
    # clean list for relevant data
    names = clean_str(names, style='name')
    names = list(filter(None, names))

    return names


def get_times(df: pd.DataFrame, row: int, cols: list) -> dict:
    """
    Handles extraction of intermediate times.
    ----------------------
    Parameters:
    * df:   DataFrame
    * row:  Row index of Country
    * cols: List of columns containing intermediate times, e.g. 500m, 1000m
    """
    vals, times, dns = [], {}, False
    for col in cols:
        # some time values are one column to the left so here a security margin is added
        # TODO: row -1 because some time values are shifted wrongly one row above
        time = df.iloc[row:row + 1, col - 1:col + 1].values[0]
        for el in time:
            if str(el) in SPECIAL_VALUES:
                logger.warning(' Special value (e.g. DNS, DNF, BUW) found.')
                dns = True
        vals.extend(re.findall(r"(?:\d{1,2}:)?\d{2}\.\d{2}", str(time)))
    # remove duplicates
    time_strings = list(dict.fromkeys(clean_str(vals, style='time')))

    # Check how many time values have to be extracted
    data_list = df.values.tolist()
    data = ''.join(str(el) for el in data_list)
    distances = [x for x in DISTS if x in data]
    num_of_times = len(distances)

    # categorize after standard deviation
    if len(time_strings) != num_of_times:
        logger.warning("Time values missing. Place by std.")
        time_str_list = [None] * num_of_times
        for idx, mean in enumerate(MEANS):
            min_val, max_val = mean - 1.2 * STDS[idx], mean + 1.2 * STDS[idx]
            for el in time_strings:
                time_val = convert_string_to_sec(el)
                if min_val <= time_val <= max_val and idx < num_of_times:
                    time_str_list[idx] = el
        time_strings = time_str_list

    if not dns:
        assert len(time_strings) == num_of_times, "Not enough times found"

    # check interval
    dist_diffs = [int(j)-int(i) for i, j in zip(distances[:-1], distances[1:])]
    intermediate_interval = max(set(dist_diffs), key=dist_diffs.count)
    for key, time in enumerate(time_strings):
        dict_key = (key + 1) * intermediate_interval
        times[dict_key] = time

    return times


def get_intermediate_ranks(df: pd.DataFrame, row: int) -> list:
    times_row = df.iloc[row:row + 1, :].values.tolist()
    ranks = re.findall(r"\((\d)\)", str(times_row))
    return [int(rank) for rank in ranks if rank]


def get_country_code(df: pd.DataFrame, row: int, cols: list) -> str:
    """
    Handles extraction of country code.
    ----------------
    Parameters:
    * df:   DataFrame
    * row:  Row index of country
    * cols: List of column indices containing country codes
    ---------------
    Returns: string representing the country code
    """
    start_row = row
    end_row = row + 1
    start_col = cols[0]
    end_col = cols[-1] + 1

    country_df = df.iloc[start_row:end_row, start_col:end_col]
    country_data = country_df.values.reshape(-1)
    country = clean_str(country_data, style="country")
    country = re.findall(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", str(country))
    return list(filter(None, country))[0]


def get_lane(df: pd.DataFrame, row: int, i: int, cols: int) -> tuple[int: int]:
    start_row = row
    end_row = row + 1
    start_col = cols[0]
    end_col = cols[-1] + 1

    lane_df = df.iloc[start_row:end_row, start_col:end_col]
    lane_data = lane_df.values.reshape(-1)
    # Idea here: Lane is either the number that is not the rank (i+1)
    # If this is not the case then it is equal to the rank
    lane_string = ''.join(str(el) for el in lane_data)[:2]
    assert len(lane_string) == 2, "String has not length of 2!"
    nums = [int(x) for x in lane_string if x.isdigit()]
    if len(nums) == 1:
        return nums[0]
    elif len(nums) == 2:
        num1, num2 = nums
        if num1 == i + 1:
            return num2
        elif num2 == i + 1:
            return num1
        else:
            return i + 1


def check_extracted_data(data: dict) -> dict:
    # restrict number of athletes to most frequent number of athletes
    lens = [len(v["athletes"]) for v in data.values() if "athletes" in v]
    max_len = max(set(lens), key=lens.count)
    for el in data.values():
        if "athletes" in el:
            el["athletes"] = el["athletes"][:max_len]
    return data


def extract_result_data(urls: list) -> tuple[list, list]:
    """
    This function extracts relevant data from the result data pdfs.
    --------------
    Parameters:
    * urls: list of urls to pdfs
    --------------
    Returns: list with extracted data
    """
    logger.info(f"Extracting data from {pdf_urls} pdfs.")
    result_data, failed_requests, errors, empty_files = [], [], 0, 0

    for url in tqdm(urls):
        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")

            # prepare df
            df = clean(handle_table_partitions(tables=tables, results=True))
            rank_row = get_string_loc(df, rank=True, column=0)["rank"]["row"]
            # remove everything above the rank row
            df = df.iloc[rank_row:].copy()
            df = clean_df(df)

            # get distance and country locations
            dist_locs = get_string_loc(df, *DISTS)["str"]["col"]

            # get country locations
            cntry_locs = get_string_loc(df, country=True, results=True)["cntry"]
            country_rows, country_cols = cntry_locs["row"], cntry_locs["col"]

            # get names column index
            n_loc = get_string_loc(df, "Name")["str"]["col"]

            assert len(country_rows) > 0, "No countries found"

            extraction_result = {}
            for idx, row in enumerate(country_rows):
                # extract lane, country, athletes and times via dedicated functions
                lane = get_lane(df, row=row, i=idx, cols=country_cols)
                country_code = get_country_code(
                    df, row=row, cols=country_cols)
                athletes = get_athletes(
                    df=df, rows=country_rows, i=idx, n_loc=n_loc)
                times = get_times(df, row=row, cols=dist_locs)
                inter_ranks = get_intermediate_ranks(df, row=row)

                extraction_result[idx] = {
                    "country": country_code,
                    "rank": idx + 1,
                    "lane": lane,
                    "athletes": athletes,
                    "times": times,
                    "inter_ranks": inter_ranks
                }

            if not extraction_result:
                empty_files += 1
            else:
                extraction_result["url"] = url
                # do sanity check on extracted data here
                res = check_extracted_data(extraction_result)
                result_data.append(res)
                logger.info(f"Extract of {url.split('/').pop()} successful.")

        except Exception as e:
            errors += 1
            failed_requests.append(url)
            logger.exception(f"Error at {url}: {e}.")

    total = len(urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors, empties=empty_files, rate=rate)

    return result_data, failed_requests


for year in range(2012, 2022):
    competition_ids = get_competition_ids(years=year)
    pdf_urls = get_pdf_urls(comp_ids=competition_ids,
                            comp_limit=NO_OF_COMPETITIONS, results=True)[::12]
    pdf_data, failed_req = extract_result_data(urls=pdf_urls)

# TODO: Append event/race id to final dict to match corresponding API data

# write results to file
write_to_json(data=pdf_data, filename="result_data")
write_to_json(data=failed_req, filename="result_data_failed")
