"""
####################################################################################################

Contains utility functions for pandas and the extraction of world rowing data from pdfs.

-------------------------------------
# TODO: Edge case: If there are two identical tables, the second one can be discarded.
(affects functions handle_edge_cases/handle_edge_cases)

####################################################################################################
"""


import traceback
import re
import json
import pandas as pd
import numpy as np
import requests
import pycountry
import jsbeautifier

# General constants
JSON_INDENT_SIZE = 4
COUNTRY_CODES_ALPHA_3 = [country.alpha_3 for country in pycountry.countries]
# Add individual Country Codes that are missing
COUNTRY_CODES_ALPHA_3 += ["NED", "GER",
                          "DEN", "SUI", "CHI", "GRE", "POR", "BUL"]
DF_REGEX = [
    r'\s+$',    # one or more whitespaces from end
    r'^\s+',    # one or more whitespaces from start
    r'\n'       # linebreak
]

# Constants for race_data pdfs
DIST_INTERVALS = ["10", "25", "50"]
RACE_DIST = "2000"


"""
################################################################
General Utils
################################################################
"""


def clean(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.replace(DF_REGEX, ['' for _ in DF_REGEX], regex=True)
    return new_df


def write_to_json(data: list, filename: str) -> None:
    """ Takes a list and writes to .json file. """
    options = jsbeautifier.default_options()
    options.indent_size = JSON_INDENT_SIZE
    file = open(f"{filename}.json", "w")
    file.write(jsbeautifier.beautify(json.dumps(data), options))
    file.close()


def print_stats(total: int, errors: int, empties: int, rate: str) -> None:
    """ Prints basic statistics for the pdf reading process. """
    print("{txt:-^25}".format(txt=f"\nRead: {(total)-errors}/{total} PDFs | ({rate}%)"))
    print("{txt:-^25}".format(txt=f"Empty Files: {empties}"))


def clean_convert_to_list(df: pd.DataFrame) -> list:
    """
    Removes linebreaks, fills non numeric values with 0
    Returns: list
    """
    df = df.replace('\\n', ' ', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
    return np.concatenate(df.to_numpy()).tolist()


'''
################################################################
WorldRowing Utils
################################################################
'''


def get_competition_ids(base_url: str) -> list:
    """
    Fetches all competition Ids from WorldRowing.com
    # TODO: Add functionality to get comp ids per year?
    ---------
    Parameters:
    * base_url:    https://world-rowing-api.soticcloud.net/stats/api/competition/
    """
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


def get_string_loc(df: pd.DataFrame, *args: str, country: bool = False, rank: bool = False, first: bool = False) -> dict:
    """
    Returns: dict with string locations
    # TODO: Add row functionality for search_str and col for country.
    ------------
    Parameters:
    * df:           pandas DataFrame
    * *args:        option to search for arbitrary number of strings
    * country:      true/false if country row should be identified
    * rank:         true/false if rank row should be identified
    * first_loc:    true/false whether only the first occurrence should be checked (only relevant for random str and Rank)
    ------------
    Return: dict with row, col indices for string args, country and rank
    """
    cntry_str, rank_str = "Country", "Rank"
    locs: dict = {
        "str": {"row": [], "col": []},
        "cntry": {"row": [], "col": []},
        "rank": {"row": [], "col": []}
    }

    if args:
        col_list = []
        for search_str in args:
            for col in df.columns:
                if df[col].str.contains(search_str).any():
                    col_list.append(col)
        col_list = list(set(col_list))  # remove duplicates
        col_list.sort()
        locs["str"]["col"] = col_list[0] if first else col_list

    if country:
        cntry_str_found = df.isin([cntry_str]).any().any()
        if cntry_str_found:
            locs["cntry"]["row"] = [df.index[df[0] == cntry_str].values[0]]
        else:
            # find column with most country code occurrences
            # TODO: START - Check how this affects the two PDF types.
            row_lst = []
            for col_idx in range(df.shape[1]):
                row = df.loc[df[col_idx].isin(COUNTRY_CODES_ALPHA_3)].index
                idx_found = int(row[0]) if row.size > 0 else None
                if isinstance(idx_found, int):
                    row_lst.append(idx_found)
            if len(row_lst):
                locs["cntry"]["row"].append(int(
                    max(set(row_lst), key=row_lst.count)))
            # TODO: END - Check how this affects the two PDF types.

            # find all row-wise occurrences of country codes for results.pdf
            country_codes = '|'.join(COUNTRY_CODES_ALPHA_3)
            counter, row_idxs = 0, []
            # from col 0 upwards check where country codes can be found
            while len(row_idxs) == 0 and counter < df.shape[1]-1:
                find_row_idxs = df[counter].str.contains(country_codes) == True
                row_idxs = df.index[find_row_idxs].tolist()
                locs["cntry"]["col"] = counter
                counter += 1
            locs["cntry"]["row"] = row_idxs

    if rank and not df.empty:
        col = 0
        # INFO: it is assumed that the rank keyword is always in the first col
        # some pdfs have second rank column at the end --> ignored so far
        ranks_contained = df[col].str.contains(rank_str, na=False)
        ranks_str_found = ranks_contained.any()
        if ranks_str_found:
            rank_row = df.index[ranks_contained][0]
            locs["rank"]["row"] = rank_row
            locs["rank"]["col"] = 0

    return locs


def get_data_loc(df: pd.DataFrame, cust_str: str = '') -> tuple[int, int]:
    """
    Find indices of race data (only speed and stroke in the table).
    --------------
    Parameters:
    * cust_str:     If provided: Search for individual start and end.
    *               If not provided: Final data value is expected to be at 2000.
    -------------
    Returns: tuple of row indices (start, end) of race data.
    """
    start, end = 0, 0
    interval_10, interval_25, interval_50 = DIST_INTERVALS

    try:
        if cust_str:
            if cust_str in df.values:
                start = get_idx_of_string(df, search_str=cust_str)
                end = last_num_idx(df)
        else:
            if interval_10 in df.values:
                start = get_idx_of_string(df, search_str=interval_10)
                end = last_num_idx(df)
            elif interval_25 in df.values:
                start = get_idx_of_string(df, search_str=interval_25)
                end = last_num_idx(df)
            elif interval_50 in df.values:
                start = get_idx_of_string(df, search_str=interval_50)
                end = last_num_idx(df)

    except Exception as ex:
        print(f"Error while checking for start/end point of data: {ex}")
        traceback.print_exc()

    return start, end


def handle_table_partitions(tables, doc_type: bool = False) -> pd.DataFrame:
    """
    Camelot may create multiple table objects, e.g. when data is spread across multiple pages.
    This function should aggregate all tables to a single df.
    ----------
    Parameters:
    * tables:       Table list from camelot-py
    * doc_type:     False = race_data.pdf, True = results.pdf
    ----------
    Returns: Single pd.DataFrame
    """
    df = pd.DataFrame()
    # store interval and previous table end to keep track of how to merge the data
    interval = tab_end = 0
    # edge case check, only keep useful dataframes
    checked_dfs = []
    for tab in tables:
        checked_df = handle_edge_cases(tab.df, doc_type=doc_type)
        if not checked_df.empty:
            checked_dfs.append(checked_df)

    for idx, table in enumerate(checked_dfs):
        # When there is only one table the df can just be appended to main df
        if idx == 0:
            first_df = table
            # if edge case error, empty df is returned only continue if df is not empty
            if not first_df.empty:

                if doc_type == False:  # only apply on race data pdfs
                    first_loc = get_data_loc(first_df)
                    # distance interval, e.g. 25, 50 depending on scale
                    interval = get_dist_interval(first_df, row_range=first_loc)
                    df = df.append(first_df, ignore_index=True)
                    # set table_end to current last value of df
                    tab_end = int(first_df.iat[first_loc[1], 0])
                else:
                    df = df.append(first_df, ignore_index=True)

            # When there are more tables (and for race data pdfs final value for table_end (2000) is not reached)
            cond = idx > 0 if doc_type else (
                idx > 0 and tab_end != int(RACE_DIST))

        elif cond:
            next_df = table
            if not next_df.empty:
                next_start = tab_end + interval
                next_loc = get_data_loc(df=next_df, cust_str=str(next_start))
                # set table_end to current last value of df
                tab_end = int(next_df.iat[next_loc[1], 0])
                next_df = next_df.iloc[next_loc[0]:next_loc[1]]
                # append next_df part to main df
                df = df.append(next_df, ignore_index=True)

    return df


def get_dist_interval(df, row_range: tuple, col: int = 0) -> int:
    """
    Finds and returns most frequent Interval in specified column of df.
    ----------------
    Parameters:
    * row_range: contains start/end of relevant rows.
    * col: column index to check for interval (basically always zero because dist is always in first colum)
    ----------------
    Returns: Number for interval, e.g. 50, 25 etc.
    """
    dist_cols = df[col].iloc[row_range[0]:row_range[1]+1]
    diffs = dist_cols.astype('int32').diff().to_numpy()
    values, counts = np.unique(diffs, return_counts=True)

    return int(values[np.argmax(counts)])


def clean_str(string: str, str_type: str):
    """
    Handles all regular expressions to filter for specific data formats regarding results.pdf.
    -----------
    Parameters:
    * string:   string to use the regex for
    * str_type:     time/name/country/number depending on the desired format
    -----------
    Returns:    Filtered string
    """
    if str_type == "time":
        # remove content in between ()
        time = re.sub(r"\(.*?\)", "()", string)
        # remove non-numeric vals and . and :
        time = re.sub(r'[^0-9.:]', '', time)
        return time
    if str_type == "name":
        name_str = re.sub(r'[0-9.:]', '', string)
        if name_str:
            return re.sub(r'[0-9.:]', '', string)
    if str_type == "country":
        cnty_str = re.sub(r"\(.*?\)", "", string)
        return re.sub(r'[0-9]', "", cnty_str)
    if str_type == "number":
        # remove numbers after country code
        num_str = re.sub(r'\d+$', "", string)
        # only keep numbers
        num_str = re.sub(r'\D', "", num_str)
        return num_str
    else:
        return None


def handle_edge_cases(df: pd.DataFrame, doc_type=False) -> pd.DataFrame:
    """
    This function should handle edge cases, e.g. dataframe contains no race data.
    Takes dataframe and returns corrected df. In error cases empty df.should be returned.
    Parameters:
    * doc_type:     False = race_data.pdf | True = results.pdf
    """
    cnty_idx = get_string_loc(df, country=True)["cntry"]["row"]
    rank_idx = get_string_loc(df, rank=True)["rank"]["row"]

    # Edge Case 1: Dataframe contains no country and no rank (often the table head)
    # if no country found and no rank found discard table by returning empty dataframe

    if cnty_idx and (rank_idx if doc_type else True):
        return df
    return pd.DataFrame()


def handle_dist_edge_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles explicit edge cases for result PDFs when race distance
    columns are not identified as separate columns.
    ------------------
    Returns: fixed dataframe
    """
    comb_lists = [
        # --> split to 2 cols
        ["500m1000m", "1500m2000m", "Name500m1000m", "1000m1500m"],
        # --> split to 3 cols
        ["500m1000m1500m", "Name500m1000m1500m"],
        # --> split to 4 cols
        ["500m1000m1500m2000m"]
    ]
    for idx, col_list in enumerate(comb_lists):
        values = df.iloc[0].values
        loc, found_str = 0, ''

        for i, el in enumerate(values):
            if el in col_list:
                loc, found_str = i, el

        if loc and idx == 0:
            comb_col = df[loc].squeeze()
            # add one extra column
            df.insert(loc+1, loc+.1, 0)
            names = [float(loc), loc+.1]
            df[names] = comb_col.str.split(r'\(\d?\)', n=1, expand=True)
            df.set_axis(
                list(np.arange(0, df.shape[1])), axis=1, inplace=True)
            # set new col names
            if found_str == comb_lists[idx][0]:
                df.at[0, loc] = "Name500m"
                df.at[0, loc+1] = "Name1000m"
            elif found_str == comb_lists[idx][1]:
                df.at[0, loc] = "1500m"
                df.at[0, loc+1] = "2000m"
            elif found_str == comb_lists[idx][2]:
                df.at[0, loc] = "Name500m"
                df.at[0, loc+1] = "Name1000m"
            elif found_str == comb_lists[idx][3]:
                df.at[0, loc] = "1000m"
                df.at[0, loc+1] = "1500m"

        elif loc and idx == 1:
            comb_col = df[loc].squeeze()
            # add two extra cols
            df.insert(loc+1, loc+.1, 0)
            df.insert(loc+2, loc+.2, 0)
            names = [float(loc), loc+.1, loc+.2]
            df[names] = comb_col.str.split(r'\(\d?\)', n=2, expand=True)
            df.set_axis(
                list(np.arange(0, df.shape[1])), axis=1, inplace=True)
            # set new col names
            df.at[0, loc] = "Name500m"
            df.at[0, loc+1] = "Name1000m"
            df.at[0, loc+2] = "Name1500m"

        elif loc and idx == 2:
            # Placeholder for edge case when there are four columns to split.
            print("Not implemented yet. Data needs to be split to four columns.")
    return df


'''
################################################################
Pandas Utils
################################################################
'''


def get_idx_of_string(df: pd.DataFrame, search_str: str, col: int = 0) -> int:
    """
    # TODO: Might be removed because get_string_loc has similar functionality.
    Finds and returns index of string in df.
    """
    if search_str in df.values:
        return df.index[df[col] == search_str].values[0]
    return -1


def last_num_idx(df: pd.DataFrame, col: int = 0) -> int:
    """
    Finds and returns index of last numeric value in DataFrame.
    """
    values = list(reversed(df[col].values))
    for idx, el in enumerate(values):
        if el.isdigit():
            return (len(values)-1)-idx
    return 0


def clean_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Returns cleaned DataFrame and a list with indices of columns, that
    were removed because no relevant information was contained.
    """
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    # store names of empty columns
    empties_list = [df[col].name for col in df if df[col].dropna().empty]
    df.dropna(axis=1, how="all", inplace=True)
    df.set_axis(list(np.arange(0, df.shape[1])), axis=1, inplace=True)
    df.set_axis(list(np.arange(0, df.shape[0])), axis=0, inplace=True)
    df = df.fillna(0)

    return df, empties_list


def reset_axis_0(df: pd.DataFrame) -> pd.DataFrame:
    return df.set_axis(list(np.arange(0, df.shape[0])), axis=0)
