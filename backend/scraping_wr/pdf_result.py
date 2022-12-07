"""
####################################################################################################
This module extracts results data from World Rowing Result pdf files.

Example file:
https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/JWCH_2014/JWCH_2014_ROWWSCULL1--J---------SFNL000100--_C73X4443.pdf

Basic stats:
* Extraction time per file: approx. 1.0 - 1.8s
####################################################################################################
"""

import pandas as pd
import itertools
from tqdm import tqdm
import camelot
import re

from utils_pdf import (clean, clean_df, get_string_loc,
                       handle_table_partitions, clean_str, convert_string_to_sec, print_stats)
from utils_general import write_to_json
from api import get_competition_ids, get_pdf_urls

import logging
logger = logging.getLogger(__name__)

# dist includes basic 500m interval and 250m para intervals
DISTS = ["250", "500", "750", "1000", "1500", "2000"]
SPECIAL_VALUES = ["dna", "DNS", "DNF", "BUW"]
MEANS = [102.73, 209.96, 314.81, 424.03]
STDS = [17.7, 31.9, 37.7, 103.9]


def get_athletes(df: pd.DataFrame, rows: list, i: int) -> list:
    """
    Handles extraction of athlete names.
    -----------------------
    Parameters:
    * df:       dataframe
    * rows:     list of country row indices as start points for names of given country
    * i:        index of current country w.r.t. countries in given pdf
    -----------------------
    Returns:    list of strings containing athlete names
    """
    # rows: starts at row of current country, ends at row of following country
    start_row = rows[i]
    end_row = rows[i + 1] if (i + 1 < len(rows)) else df.shape[0]
    athlete_df = df.iloc[start_row:end_row, 0:df.shape[1] - 1]
    names = athlete_df.dropna().values.reshape(-1)
    return clean_str(names, style='name')


def get_times(df: pd.DataFrame, row: int, cols: list) -> dict:
    """
    Handles extraction of intermediate times.
    ----------------------
    Parameters:
    * df:   dataframe
    * row:  row index of country
    * cols: list of columns containing intermediate times, e.g. 500m, 1000m
    """
    vals, times = [], {}
    for col in cols:
        [time] = df.iloc[row:row + 1, col - 2:col + 2].values
        for el in time:
            if str(el) in SPECIAL_VALUES:
                logger.warning(' Special value (e.g. DNS, DNF, BUW) found.')
        vals.extend(re.findall(r"(?:\d{1,2}:)?\d{2}\.\d{2}", str(time)))
    # remove duplicates
    time_strings = list(dict.fromkeys(clean_str(vals, style='time')))
    # Check how many time values have to be extracted
    data_list = df.values.tolist()
    data = ''.join(str(el) for el in data_list)
    distances = [x for x in DISTS if x in data]
    num_of_times = len(distances)

    # if time values are missing categorize times to distance after standard deviation
    if len(time_strings) != num_of_times:
        logger.warning(" Time values missing – place times w.r.t. stdv of data.")
        time_str_list = [None] * num_of_times
        for idx, mean in enumerate(MEANS):
            min_val, max_val = mean - 1.2 * STDS[idx], mean + 1.2 * STDS[idx]
            for el in time_strings:
                time_val = convert_string_to_sec(el)
                if min_val <= time_val <= max_val and idx < num_of_times:
                    time_str_list[idx] = el
        time_strings = time_str_list

    # check interval and place time values according to distance
    dist_diffs = [int(j) - int(i) for i, j in zip(distances[:-1], distances[1:])]
    intermediate_interval = max(set(dist_diffs), key=dist_diffs.count)
    for key, time in enumerate(time_strings):
        dict_key = (key + 1) * intermediate_interval
        times[dict_key] = time

    return times


def get_intermediate_ranks(df: pd.DataFrame, row: int) -> list:
    times_row = df.iloc[row:row + 1, :].values.tolist()
    ranks = re.findall(r"\((\d)\)", str(times_row))
    return [int(rank) for rank in ranks if rank]


def get_country_code(df: pd.DataFrame, row: int) -> str:
    """
    Handles extraction of country code.
    ----------------
    Parameters:
    * df:   dataframe
    * row:  row index of country
    * cols: list of column indices containing country codes
    ---------------
    Returns: string representing the country code
    """
    country_df = df.iloc[row:row + 1, 0:df.shape[1] - 1]
    country_data = country_df.values.reshape(-1)
    reg = r"(?<![A-Z])[A-Z]{3}(?![A-Z])(?!\s)"
    country = list(itertools.chain(*[re.findall(reg, str(x)) for x in country_data]))
    return clean_str(country, style="country")


def get_lane(df: pd.DataFrame, row: int, i: int) -> tuple[int: int]:
    lane_data = df.iloc[row:row + 1, 0:df.shape[1] - 1].values.reshape(-1)
    lane_string = ''.join(str(el) for el in lane_data)
    nums = [int(re.findall(r"^\d{1,2}$", str(el))[0]) for el in lane_string if el.isdigit()][:2]
    # lane is either the number that is not the rank (i+1) or it is equal to the rank
    if len(nums) == 1:
        return nums
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
    # restrict number of intermediate ranks to n - 1 ranks where n is the number of distances
    inter_ranks_len = [len(v["times"]) for v in data.values() if "times" in v]
    max_inter_len = max(set(inter_ranks_len), key=lens.count)-1
    for el in data.values():
        if "inter_ranks" in el:
            el["inter_ranks"] = el["inter_ranks"][:max_inter_len]
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
            tables = camelot.read_pdf(url, flavor="stream", pages="all", column_tol=2)

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
            country_rows, _ = cntry_locs["row"], cntry_locs["col"]

            extraction_result = {}
            for idx, row in enumerate(country_rows):
                extraction_result[idx] = {
                    "country": get_country_code(df=df, row=row),
                    "rank": idx + 1,
                    "lane": get_lane(df=df, row=row, i=idx),
                    "athletes": get_athletes(df=df, rows=country_rows, i=idx),
                    "times": get_times(df=df, row=row, cols=dist_locs),
                    "inter_ranks": get_intermediate_ranks(df=df, row=row)
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


complete_data, all_failed = [], []
for year in range(2011, 2012):
    competition_ids = get_competition_ids(years=year)
    pdf_urls = get_pdf_urls(comp_ids=competition_ids,
                            comp_limit=1000, results=True)[:5]
    pdf_data, failed_req = extract_result_data(urls=pdf_urls)
    complete_data.append(pdf_data)

# write results to file
write_to_json(data=complete_data, filename="result_data")
write_to_json(data=all_failed, filename="result_data_failed")
