import pandas as pd
import numpy as np
import requests
import pycountry
import jsbeautifier
import json

# Constants
JSON_INDENT_SIZE = 4
COUNTRY_CODES_ALPHA_3 = [country.alpha_3 for country in pycountry.countries]
DF_REGEX = [
    r'\s+$',    # one or more whitespaces from end
    r'^\s+',    # one or more whitespaces from start
    r'\n'       # linebreak
]

'''
################################################################
General Utils
################################################################
'''


def clean(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.replace(DF_REGEX, ['' for i in DF_REGEX], regex=True)
    return new_df


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


'''
################################################################
WorldRowing Utils
################################################################
'''


def get_competition_ids(base_url: str) -> list:
    '''
    Fetches all competition Ids from WorldRowing.com
    # TODO: Add functionality to get comp ids per year?
    ---------
    Parameters:
    * base_url:    https://world-rowing-api.soticcloud.net/stats/api/competition/
    '''
    competitions = requests.get(base_url).json()["data"]
    ids_list = [comp["id"] for comp in competitions]
    return ids_list


def get_pdf_urls(base_url: str, comp_ids: list, comp_limit: int, filter_str: str, pdf_type: bool) -> list:
    """
    Fetches URLs to pdf files hosted on https://d3fpn4c9813ycf.cloudfront.net/.
    ---------
    Parameters:
    * base_url:     for world rowing this is https://world-rowing-api.soticcloud.net/stats/api/competition/
    * comp_ids:     list of competition ids
    * comp_limit:   limit amount of competitions
    * filter_str:   filter parameter and values as string, e.g. '?include=events.races<...>'
    * pdf_type:     0 = "Race Data" | 1 = "Results"
    ---------
    Returns: list of urls for specified criteria
    """
    competition_ids = comp_ids[0:comp_limit]
    urls = []
    doc_type = "Results" if pdf_type else "Race Data"

    for comp_id in competition_ids:
        query = base_url + comp_id + filter_str
        events = requests.get(query).json()["data"]["events"]

        for event in events:
            races = event["races"]
            for race in races:
                for pdf in race["pdfUrls"]:
                    if pdf["title"] == doc_type:
                        urls.append(pdf["url"])
    return urls


def get_string_loc(df: pd.DataFrame, *args: str, country: bool = False, rank: bool = False) -> dict:
    '''
    Returns: dict with string locations
    # TODO: Check which way is better to find strings df.isin([]).any().any() or str.contains.
    # TODO: Add row functionality for search_str and col for country.
    # TODO: For countries, one should also check for Numbers 1-9 behind the country codes.
    ------------
    Parameters:
    * df:       pandas DataFrame
    * country:  true/false if country row should be identified
    * rank:     true/false if rank row should be identified
    ------------
    Return: dict with row, col indices; -1 indicates that strings were not found
    '''
    cntry_str: str = "Country"
    rank_str: str = "Rank"
    locs: dict = {
        "str": {"rows": [], "cols": []},
        "cntry": {"rows": [], "cols": []},
        "rank": {"rows": []}
    }

    if args:
        col_list = []
        for search_str in args:
            for col in df.columns:
                if df[col].str.contains(search_str).any():
                    col_list.append(col)
        col_list = list(set(col_list))
        col_list.sort()
        locs["str"]["cols"] = col_list

    if country:
        country_str_found = df.isin([cntry_str]).any().any()
        if country_str_found:
            print("Country string found")
            locs["cntry"]["rows"] = [
                df.index[df[0] == cntry_str].values[0]]
        else:
            print("No country string found")
            # find column with most country code occurrences
            # TODO: Prüfen, inwiefern das mit den zwei PDF Typen interferriert.
            row_lst = []
            for col_idx in range(df.shape[1]):
                row = df.loc[df[col_idx].isin(COUNTRY_CODES_ALPHA_3)].index
                idx_found = int(row[0]) if row.size > 0 else None
                if isinstance(idx_found, int):
                    row_lst.append(idx_found)
            if len(row_lst):
                locs["cntry"]["rows"].append(int(
                    max(set(row_lst), key=row_lst.count)))

            # TODO: Matcht z.B. GER nicht, weil kein offizieller ISO-Code
            # FOR Results.pdf --> find all row-wise occurrences of country codes
            country_codes = '|'.join(COUNTRY_CODES_ALPHA_3)
            counter = 0
            row_idxs = []
            # from col 0 upwards check where country codes can be found
            while len(row_idxs) == 0:
                find_row_idxs = df[counter].str.contains(country_codes) == True
                row_idxs = df.index[find_row_idxs].tolist()
                locs["cntry"]["cols"] = counter
                counter += 1
            locs["cntry"]["rows"] = row_idxs

    if rank:
        # for the rank it is assumed that it is always in the first column
        ranks_contained = df[0].str.contains(rank_str)
        ranks_str_found: bool = ranks_contained.any()
        if ranks_str_found:
            locs["rank"]["rows"] = df.index[ranks_contained][0]
    return locs


'''
################################################################
Pandas Utils
################################################################
'''


def clean_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    '''
    Returns cleaned DataFrame and a list with indices of columns, that
    were removed because no relevant information was contained.
    '''
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    empties_list = [df[col].name for col in df if df[col].dropna().empty]
    df.dropna(axis=1, how="all", inplace=True)
    df.set_axis(list(np.arange(0, df.shape[1])), axis=1, inplace=True)
    df.set_axis(list(np.arange(0, df.shape[0])), axis=0, inplace=True)
    df = df.fillna(0)

    return df, empties_list
