'''
####################################################################################################

This module extracts race data (speed[m/s] and stroke[1/m]) for each country per race and writes them to a json file.
Those files for which the extraction process fails, the corresponding URLs are written to a failed_requests.json file.

Basic stats:
* For the 1000 competition IDs provided by the API, there are approximately 11.700 race data pdfs.
* Processing time per pdf: approx. 1.8 - 2.5s
* Time to process 11.7k pdfs: approx. 7 hours
* Last test - successful extractions: 11092/11509 PDFs | (96,38%)

-------------------------------------
# TODO: Fix line break errors --> about 200 files contain non-visible '\n's.
Since the data extraction for these fails, the URLs are contained in the failed_requests.json file.
If 2000m is the only value on the second page for the 50m interval there are also weird line breaks.

# TODO: Edge case: If there are two identical tables, the second one can be discarded.
(affects functions handle_edge_cases/handle_edge_cases)
####################################################################################################
'''

import traceback
import json
from typing import Tuple
import requests
import pycountry
import camelot  # on Mac via 'pip install camelot-py[cv]'
from tqdm import tqdm
import jsbeautifier
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

# CONSTANTS
BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/competition/"
FILTER_STRING = "/?include=pdfUrls.orisCode,events.pdfUrls,events.races.pdfUrls.orisCode,events.boatClass,events.races.racePhase,events.races.photoFinishImage&sortInclude[pdfUrls.created_at]=asc&sortInclude[events.pdfUrls.DisplayName]=desc&sortInclude[events.races.pdfUrls.created_at]=asc"
COUNTRY_CODES_ALPHA_3 = [country.alpha_3 for country in pycountry.countries]
JSON_INDENT_SIZE = 4
# INFO: API seems to give only 1000 Competitions, so this would be max there
NO_OF_COMPETITIONS = 50  # 1000
DIST_INTERVALS = ["10", "25", "50"]
RACE_DIST = "2000"


def write_to_json(data: list, filename: str) -> None:
    '''
    Takes a list and writes to .json file.
    '''
    options = jsbeautifier.default_options()
    options.indent_size = JSON_INDENT_SIZE
    file = open(f"{filename}.json", "w")
    file.write(jsbeautifier.beautify(json.dumps(data), options))
    file.close()


def print_stats(total: int, errors: int, empties: int, rate: str) -> None:
    ''''
    Prints basic statistics for the pdf reading process.
    '''
    print("{txt:-^25}".format(txt=f"\nRead: {(total)-errors}/{total} PDFs | ({rate}%)"))
    print("{txt:-^25}".format(txt=f"Empty Files: {empties}"))


def get_competition_ids() -> list:
    competitions = requests.get(BASE_URL).json()["data"]
    return [competition["id"] for competition in competitions]


def fetch_race_data_urls(comp_ids: list) -> list:
    """
    Takes list of competition id's and returns
    list of corresponding race data pdf URLs.
    """
    # INFO: Slicing is done for test reasons here, so we don't check 11k pdfs everytime :D
    comp_ids = comp_ids[0:NO_OF_COMPETITIONS]
    urls = []
    for comp_id in comp_ids:
        query = BASE_URL + comp_id + FILTER_STRING
        events = requests.get(query).json()["data"]["events"]
        for event in events:
            races = event["races"]
            for race in races:
                pdfs = race["pdfUrls"]
                for pdf in pdfs:
                    if pdf["title"] == "Race Data":
                        urls.append(pdf["url"])
    print(f"{len(urls)} PDFs found...")
    return urls


def get_idx_of_string(df: pd.DataFrame, search_str: str, col: int = 0) -> int:
    '''
    Finds and returns index of string in df.
    '''
    if search_str in df.values:
        return df.index[df[col] == search_str].values[0]
    return -1


def last_num_idx(df: pd.DataFrame, idx: int = -1, col: int = 0) -> int:
    '''
    Finds the Index of the last numeric value in DataFrame.
    '''
    last_val = df[col].iat[idx]
    last_numeric = last_val if last_val.isnumeric() else str(last_num_idx(df, idx=idx-1))
    return get_idx_of_string(df, last_numeric)


def get_dist_interval(df, row_range: list, col: int = 0) -> int:
    '''
    Finds and returns most frequent Interval in specified column of df.
    Params:
    * row_range: contains start/end of relevant rows.
    * col: column index to check for interval 
    (basically always zero because dist is always in first colum)
    '''
    dist_cols = df[col].iloc[int(row_range[0]):int(row_range[1]+1)]
    diffs = dist_cols.astype('int32').diff().to_numpy()
    values, counts = np.unique(diffs, return_counts=True)
    return int(values[np.argmax(counts)])


def get_data_loc(df: pd.DataFrame, cust_str: str = '') -> list:
    """
    If cust_str is provided: Search for individual start and end.
    If no cust_str is provided: Final data value is expected to be at 2000.
    Returns: list of row indices [start, end] of actual race data.
    """
    start_end = [0, 0]
    interval_10, interval_25, interval_50 = DIST_INTERVALS
    try:
        if cust_str:
            if cust_str in df.values:
                start_end[0] = get_idx_of_string(df, search_str=cust_str)
                start_end[1] = last_num_idx(df)
        else:
            if interval_10 in df.values:
                start_end[0] = get_idx_of_string(df, search_str=interval_10)
                start_end[1] = last_num_idx(df)
            elif interval_25 in df.values:
                start_end[0] = get_idx_of_string(df, search_str=interval_25)
                start_end[1] = last_num_idx(df)
            elif interval_50 in df.values:
                start_end[0] = get_idx_of_string(df, search_str=interval_50)
                start_end[1] = last_num_idx(df)

    except Exception as ex:
        print(f"Error while checking for start/end point of data: {ex}")
        traceback.print_exc()
    return start_end


def get_country_ranks_loc(df, cnty: str = "Country", rank: str = "Rank") -> Tuple[int, bool]:
    '''
    Returns: Tuple (Row Idx of country string, rank row was found / not found)
    '''
    ranks_str_found: bool = df.isin([rank]).any().any()
    country_str_found: bool = df.isin([cnty]).any().any()
    if country_str_found:
        cnty_idx: int = df.index[df[0] == cnty].values[0]
    else:
        cnty_idx: -1
    if not country_str_found:
        cntry_row_lst = []
        for col_idx in range(df.shape[1]):
            cntry_row = df.loc[df[col_idx].isin(COUNTRY_CODES_ALPHA_3)].index
            idx_found = int(cntry_row[0]) if cntry_row.size > 0 else None
            if isinstance(idx_found, int):
                cntry_row_lst.append(idx_found)
        if len(cntry_row_lst) > 0:
            cnty_idx = int(max(set(cntry_row_lst), key=cntry_row_lst.count))
        else:
            cnty_idx = -1
    return (cnty_idx, ranks_str_found)


def clean_convert_to_list(df: pd.DataFrame) -> list:
    '''
    Removes linebreaks, fills non numeric values with 0
    Returns: list
    '''
    df = df.replace('\\n', ' ', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
    return np.concatenate(df.to_numpy()).tolist()


def clean_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
    '''
    Returns cleaned DataFrame and a list with indices of columns, that
    were removed because no race data information was contained.
    '''
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    empties_list = [df[col].name for col in df if df[col].dropna().empty]
    df.dropna(axis=1, how="all", inplace=True)
    df.set_axis(list(np.arange(0, df.shape[1])), axis=1, inplace=True)
    df.set_axis(list(np.arange(0, df.shape[0])), axis=0, inplace=True)
    return df, empties_list


def reset_axis(df: pd.DataFrame) -> pd.DataFrame:
    return df.set_axis(list(np.arange(0, df.shape[0])), axis=0)


def df_to_json(df: pd.DataFrame) -> list:
    '''
    Extracts data (countries, ranks, data) from
    final dataframe and return json-like structure.
    '''
    # Handle top part with countries and ranks
    cnty_idx, ranks_found = get_country_ranks_loc(df)
    top_df = reset_axis(df.iloc[cnty_idx:cnty_idx+(2 if ranks_found else 1)])
    countr = [x for x in np.concatenate(top_df.iloc[0:1, 1:].to_numpy()) if x]
    if ranks_found:
        ranks = [x for x in np.concatenate(
            top_df.iloc[1:2, 1:].to_numpy()) if x]

    # Handle data part
    data_range = get_data_loc(df)
    data_df = reset_axis(df.iloc[data_range[0]:data_range[1]])
    data_df, deleted_cols = clean_dataframe(data_df)

    # Handle countries with empty data colums.
    for num in deleted_cols:
        if num % 2 != 0:
            idx = ((num+1)//2)-1
            if idx < len(countr) and num+1 in deleted_cols:
                countr.pop(idx)

    # Create dict with relevant data and return as list of dicts.
    data = []
    offset = 0
    dist = [int(el) for el in data_df.iloc[:, 0].values]

    for idx, country in enumerate(countr):
        if country:
            speed = data_df.iloc[:, (idx + 1) + offset: (idx + 2) + offset]
            stroke = data_df.iloc[:, (idx + 2) + offset: (idx + 3) + offset]
            race_data_obj = {
                "country": countr[idx],
                "rank": ranks[idx] if ranks_found else None,
                "speed": {
                    "dist_in_m": dist,
                    "speed_val": clean_convert_to_list(speed)
                },
                "stroke": {
                    "dist_in_m": dist,
                    "stroke_val": clean_convert_to_list(stroke),
                }
            }
            data.append(race_data_obj)
            offset += 1
    return data


def handle_edge_cases(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function should handle edge cases, e.g. dataframe contains no race data.
    Takes dataframe and returns corrected df. In error cases empty df.should be returned.
    '''
    new_df = pd.DataFrame()
    # Edge Case 1: Dataframe contains no countries and therefore no relevant data
    cnty_idx, _ = get_country_ranks_loc(df)
    if cnty_idx == -1:
        return new_df
    return df


def handle_table_partitions(tables) -> pd.DataFrame:
    '''
    Camelot may create multiple table objects, e.g. when data is spread across multiple pages.
    This function should aggregate all tables to a single df.
    Return: Single pd.DataFrame
    '''
    df = pd.DataFrame()
    # store interval and previous table end to keep track of how to merge the data
    interval = table_end = 0
    # edge case check
    checked_dfs = []
    for tab in tables:
        checked_df = handle_edge_cases(tab.df)
        if not checked_df.empty:
            checked_dfs.append(checked_df)

    for idx, table in enumerate(checked_dfs):
        # When there is only one table the df can just be appended to main df
        if idx == 0:
            first_df = table
            # if edge case error, empty df is returned
            # only continue if df is not empty
            if not first_df.empty:
                first_loc = get_data_loc(first_df)
                # distance interval, e.g. 25, 50 depending on scale
                interval = get_dist_interval(first_df, row_range=first_loc)
                df = df.append(first_df, ignore_index=True)
                # set table_end to current last value of df
                table_end = int(first_df.iat[first_loc[1], 0])

        # When there are more tables and final value for table_end (2000) is not reached
        elif idx > 0 and table_end != int(RACE_DIST):
            next_df = table
            print(next_df)
            if not next_df.empty:
                next_start = table_end + interval
                print(next_start)
                next_loc = get_data_loc(df=next_df, cust_str=str(next_start))
                # set table_end to current last value of df
                table_end = int(next_df.iat[next_loc[1], 0])
                next_df = next_df.iloc[next_loc[0]:next_loc[1]]
                # append next_df part to main df
                df = df.append(next_df, ignore_index=True)

    return df


def extract_table_data(pdf_urls: list) -> Tuple[list, list]:
    '''
    Extracts data from given pdf urls using Camelot.
    --------------------------------
    Returns:
    * List with json-like objects (final structure needs to be discussed) for each team per race
    * List containing the urls of all failed requests
    '''
    json_lst = failed_requests = []
    errors: int = 0
    empty_files: int = 0

    for url in tqdm(pdf_urls):
        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")
            df = handle_table_partitions(tables=tables)
            json_data = None if df.empty else df_to_json(df)

            if not json_data:
                empty_files += 1
            else:
                json_lst.append(json_data)
            print(f"Extract of {url.split('/').pop()} successful.")

        except Exception as e:
            errors += 1
            failed_requests.append(url)
            print(f"Error extracting {url}: {e}.\nErrors so far: {errors}.")
            traceback.print_exc()

    total = len(pdf_urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors, empties=empty_files, rate=rate)

    return json_lst, failed_requests


competition_ids = get_competition_ids()
urls = fetch_race_data_urls(comp_ids=competition_ids)

data, failed_requests = extract_table_data(pdf_urls=urls)

write_to_json(data=data, filename="output")
write_to_json(data=failed_requests, filename="failed_requests")
