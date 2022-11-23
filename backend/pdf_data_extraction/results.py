"""
####################################################################################################

This module extracts the data from results pdf files.

Example file:
https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/JWCH_2014/JWCH_2014_ROWWSCULL1--J---------SFNL000100--_C73X4443.pdf

Basic stats:
* Extraction time per file: approx. 1.2 - 1.6s

-------------------------------------
# TODO: Add multi-page functionality.
# TODO: Add delta times.
# TODO: Add intermediate ranks.

####################################################################################################
"""

import traceback
import camelot
from tqdm import tqdm

from utils import clean
from utils import clean_df
from utils import get_pdf_urls
from utils import get_string_loc
from utils import get_competition_ids
from utils import write_to_json
from utils import handle_dist_edge_case
from utils import handle_table_partitions
from utils import clean_str
from utils import print_stats

BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/competition/"
# To be replaced by call to generic scraper class
FILTER_STRING = "/?include=pdfUrls.orisCode,events.pdfUrls,events.races.pdfUrls.orisCode,events.boatClass,events.races.racePhase,events.races.photoFinishImage,events.races.raceBoats.raceBoatIntermediates.distance"
SORT_STRING = "&sortInclude[pdfUrls.created_at]=asc&sortInclude[events.pdfUrls.DisplayName]=desc&sortInclude[events.races.pdfUrls.created_at]=asc"
NO_OF_COMPETITIONS = 300
INTERMED_INTERVAL = 500
DISTS = ['500m', '1000m', '1500m', '2000m']


def extract_result_data(urls: list) -> list:
    """
    This function extracts relevant data from the result data pdfs.
    --------------
    Parameters:
    * urls: list of urls to pdfs
    --------------
    Returns: list with extracted data
    """
    result_data, failed_requests, errors, empty_files = [], [], 0, 0

    for url in tqdm(urls):

        try:
            tables = camelot.read_pdf(url, flavor="stream", pages="all")

            # prepare df
            df = clean(handle_table_partitions(tables=tables, results=1))
            rank_row = get_string_loc(df, rank=True, column=0)["rank"]["row"]
            new_df = df.iloc[rank_row:].copy()
            new_df, _ = clean_df(new_df)

            # get distance and country locations
            dist_locs = get_string_loc(new_df, *DISTS)["str"]["col"]
            if len(dist_locs) < 4:  # edge case dist cols combined
                new_df = handle_dist_edge_case(new_df)
                dist_locs = get_string_loc(new_df, *DISTS)["str"]["col"]

            # get rank and lane locations
            rank_col = get_string_loc(new_df, rank=True, first=True, column=0)[
                "rank"]["col"]

            # currently there are two terms for lane: lane & order
            lane_col = get_string_loc(new_df, "Lane", "Order", first=True)[
                "str"]["col"]

            # get country locations
            cntry_locs = get_string_loc(
                new_df, country=True, results=1)["cntry"]
            cntry_row, cntry_col = cntry_locs["row"], cntry_locs["col"]

            # get names column index
            name_locs = get_string_loc(new_df, "Name")["str"]["col"]

            for idx, cntry in enumerate(cntry_row):
                rank = new_df.iloc[cntry:cntry + 1, rank_col].values[0]
                lane = new_df.iloc[cntry:cntry+1, lane_col].values[0]

                # handle edge case, when rank, lane and country code are in first col
                if rank_col == lane_col == cntry_col == 0:
                    rank_lane = new_df.iloc[cntry:cntry+1, 0].values[0]
                    rank_lane = clean_str(rank_lane, str_type="number")
                    if len(rank_lane) == 2:
                        rank, lane = rank_lane[0], rank_lane[1]
                    else:
                        rank, lane = None, None

                # handle country code
                country = new_df.iloc[cntry:cntry+1, cntry_col].values[0]
                country_name = clean_str(country, str_type="country")

                # handle athlete name(s)
                next_cntry = cntry_row[idx+1] if idx + \
                    1 < len(cntry_row) else new_df.shape[0]
                athletes = new_df.iloc[cntry:next_cntry, name_locs[0]].copy()
                athletes = list(filter(None, athletes))
                athletes = [clean_str(name, str_type='name')
                            for name in athletes]
                athletes = list(filter(None, athletes))

                # handle intermediate times
                times = {}
                for key, dist in enumerate(dist_locs):
                    time = new_df.iloc[cntry:cntry+1, dist].values[0]
                    if isinstance(time, str):
                        times[(key+1) *
                              INTERMED_INTERVAL] = clean_str(time, str_type='time')

                result_data.append({
                    "country": country_name,
                    "rank": rank,
                    "lane": lane,
                    "athletes": athletes,
                    "times": times
                })
            if not result_data:
                empty_files += 1
            else:
                print(f"Extract of {url.split('/').pop()} successful.")

        except Exception as exc:
            errors += 1
            failed_requests.append(url)
            print(f"Error extracting {url}: {exc}.")
            traceback.print_exc()

    total = len(urls) - empty_files
    rate = "{:.2f}".format(100 - ((errors / total if total else 0) * 100))
    print_stats(total=total, errors=errors, empties=empty_files, rate=rate)

    return result_data, failed_requests


competition_ids = get_competition_ids(base_url=BASE_URL, year=2020)
pdf_urls = get_pdf_urls(base_url=BASE_URL, comp_ids=competition_ids,
                        comp_limit=NO_OF_COMPETITIONS, filter_str=FILTER_STRING+SORT_STRING, results=1)[0:10]

print(f"Extracting data from {pdf_urls} pdfs.")
pdf_data, failed_req = extract_result_data(urls=pdf_urls)

# write results to file
write_to_json(data=pdf_data, filename="result_data")
write_to_json(data=failed_req, filename="result_data_failed")
