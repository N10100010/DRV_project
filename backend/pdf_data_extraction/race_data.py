"""
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

####################################################################################################
"""

import traceback
import camelot  # on Mac via 'pip install camelot-py[cv]'
from tqdm import tqdm
import numpy as np
import pandas as pd

from utils import get_pdf_urls
from utils import handle_table_partitions
from utils import get_competition_ids
from utils import get_data_loc
from utils import print_stats
from utils import clean_df
from utils import write_to_json
from utils import get_string_loc
from utils import clean_convert_to_list
from utils import reset_axis_0

# CONSTANTS
BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/competition/"
FILTER_STRING = "/?include=pdfUrls.orisCode,events.pdfUrls,events.races.pdfUrls.orisCode,events.boatClass,events.races.racePhase,events.races.photoFinishImage&sortInclude[pdfUrls.created_at]=asc&sortInclude[events.pdfUrls.DisplayName]=desc&sortInclude[events.races.pdfUrls.created_at]=asc"
JSON_INDENT_SIZE = 4
NO_OF_COMPETITIONS = 100  # INFO: API gives only max. 1000


def df_to_json(df: pd.DataFrame) -> list:
    """
    Extracts data (countries, ranks, data) from final dataframe and return json-like structure.
    """
    # Handle top part with countries and ranks
    cnty_idx = get_string_loc(df, country=True)["cntry"]["row"]
    cnty_idx = cnty_idx[0] if cnty_idx else None
    rank_found = bool(get_string_loc(df, rank=True)["rank"]["row"])
    top_part = df.iloc[cnty_idx:cnty_idx+(2 if rank_found else 1)]
    top_df = reset_axis_0(top_part)
    countries = [x for x in np.concatenate(
        top_df.iloc[0:1, 1:].to_numpy()) if x]

    if rank_found:
        ranks = [x for x in np.concatenate(
            top_df.iloc[1:2, 1:].to_numpy()) if x]

    # Handle data part
    data_range = get_data_loc(df)
    data_df = reset_axis_0(df.iloc[data_range[0]:data_range[1]+1])
    data_df, deleted_cols = clean_df(data_df)

    # Handle countries with empty data colums.
    for num in deleted_cols:
        if num % 2 != 0:
            idx = ((num+1)//2)-1
            if idx < len(countries) and num+1 in deleted_cols:
                countries.pop(idx)

    # Create dict with relevant data and return as list of dicts.
    data, offset = [], 0
    dist = [int(el) for el in data_df[0].values]

    for idx, country in enumerate(countries):
        speed = data_df.iloc[:, (idx + 1) + offset: (idx + 2) + offset]
        stroke = data_df.iloc[:, (idx + 2) + offset: (idx + 3) + offset]
        data.append({
            "country": country,
            "rank": ranks[idx] if rank_found else None,
            "data": {
                "dist [m]": dist,
                "speed [m/s]": clean_convert_to_list(speed),
                "stroke": clean_convert_to_list(stroke)
            }
        })
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

    json_lst, failed_requests = [], []
    errors, empty_files = 0, 0

    for url in tqdm(pdf_urls):
        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")
            df = handle_table_partitions(tables=tables, results=0)
            json_data = None if df.empty else df_to_json(df)

            if json_data:
                json_lst.append(json_data)
                print(f"Extract of {url.split('/').pop()} successful.")
            else:
                empty_files += 1
                print(f"Empty file found: {url.split('/').pop()}.")

        except Exception:
            errors += 1
            failed_requests.append(url)
            print(
                f"Error extracting {url}:\n{traceback.print_exc()}.\nErrors so far: {errors}.")

    # create extraction statistics
    total = len(pdf_urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors,
                empties=empty_files, rate=rate)

    return json_lst, failed_requests


competition_ids = get_competition_ids(base_url=BASE_URL, year=2010)

urls = get_pdf_urls(base_url=BASE_URL, comp_ids=competition_ids,
                    comp_limit=NO_OF_COMPETITIONS, filter_str=FILTER_STRING, results=0)[0:10]

print(urls)
race_data, failed_req = extract_table_data(pdf_urls=urls)

write_to_json(data=race_data, filename="race_data")
write_to_json(data=failed_req, filename="race_data_failed")
