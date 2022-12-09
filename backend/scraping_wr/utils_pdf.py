"""
####################################################################################################

Contains utility functions for pandas and the extraction of world rowing data from pdfs.

-------------------------------------

####################################################################################################
"""

import re
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__name__)
from itertools import groupby
from operator import itemgetter

# General constants
COUNTRY_CODES = {
    "AFG": "Afghanistan",
    "ALB": "Albanien",
    "ALG": "Algerien",
    "AND": "Andorra",
    "ANG": "Angola",
    "ANT": "Antigua und Barbuda",
    "ARG": "Argentinien",
    "ARM": "Armenien",
    "ARU": "Aruba",
    "ASA": "Amerikanisch Samoa",
    "AUS": "Australien",
    "AUT": "Österreich",
    "AZE": "Aserbaidschan",
    "BAH": "Bahamas",
    "BAN": "Bangladesch",
    "BAR": "Barbados",
    "BDI": "Burundi",
    "BEL": "Belgien",
    "BEN": "Benin",
    "BER": "Bermuda",
    "BHU": "Bhutan",
    "BIH": "Bosnien und Herzegowina",
    "BIZ": "Belize",
    "BLR": "Belarus",
    "BOL": "Bolivien",
    "BOT": "Botswana",
    "BRA": "Brasilien",
    "BRN": "Bahrain",
    "BRU": "Brunei",
    "BUL": "Bulgarien",
    "BUR": "Burkina Faso",
    "CAF": "Zentralafrikanische Republik",
    "CAM": "Kambodscha",
    "CAN": "Kanada",
    "CAY": "Kaimaninseln",
    "CGO": "Republik Kongo",
    "CHA": "Tschad",
    "CHI": "Chile",
    "CHN": "China",
    "CIV": "Elfenbeinküste",
    "CMR": "Kamerun",
    "COD": "Demokratische Republik Kongo",
    "COK": "Cookinseln",
    "COL": "Kolumbien",
    "COM": "Komoren",
    "CPV": "Kap Verde",
    "CRC": "Costa Rica",
    "CRO": "Kroatien",
    "CUB": "Kuba",
    "CYP": "Zypern",
    "CZE": "Tschechien",
    "DEN": "Dänemark",
    "DJI": "Dschibuti",
    "DMA": "Dominica",
    "DOM": "Dominikanische Republik",
    "ECU": "Ecuador",
    "EGY": "Ägypten",
    "ERI": "Eritrea",
    "ESA": "El Salvador",
    "ESP": "Spanien",
    "EST": "Estland",
    "ETH": "Äthiopien",
    "FIJ": "Fidschi",
    "FIN": "Finnland",
    "FRA": "Frankreich",
    "FSM": "Föderierte Staaten von Mikronesien",
    "GAB": "Gabun",
    "GAM": "Gambia",
    "GBR": "Vereinigtes Königreich",
    "GBS": "Guinea-Bissau",
    "GEO": "Georgien",
    "GEQ": "Äquatorialguinea",
    "GER": "Deutschland",
    "GHA": "Ghana",
    "GRE": "Griechenland",
    "GRN": "Grenada",
    "GUA": "Guatemala",
    "GUI": "Guinea",
    "GUM": "Guam",
    "GUY": "Guyana",
    "HAI": "Haiti",
    "HKG": "Hongkong",
    "HON": "Honduras",
    "HUN": "Ungarn",
    "INA": "Indonesien",
    "IND": "Indien",
    "IRI": "Iran",
    "IRL": "Irland",
    "IRQ": "Irak",
    "ISL": "Island",
    "ISR": "Israel",
    "ISV": "Jungferninseln (US)",
    "ITA": "Italien",
    "IVB": "Jungferninseln (UK)",
    "JAM": "Jamaika",
    "JOR": "Jordanien",
    "JPN": "Japan",
    "KAZ": "Kasachstan",
    "KEN": "Kenia",
    "KGZ": "Kirgisistan",
    "KIR": "Kiribati",
    "KOR": "Südkorea",
    "KOS": "Kosovo",
    "KSA": "Saudi-Arabien",
    "KUW": "Kuwait",
    "LAO": "Laos",
    "LAT": "Lettland",
    "LBA": "Libyen",
    "LBN": "Libanon",
    "LBR": "Liberia",
    "LCA": "St. Lucia",
    "LES": "Lesotho",
    "LIE": "Liechtenstein",
    "LTU": "Litauen",
    "LUX": "Luxemburg",
    "MAD": "Madagaskar",
    "MAR": "Marokko",
    "MAS": "Malaysia",
    "MAW": "Malawi",
    "MDA": "Moldawien",
    "MDV": "Malediven",
    "MEX": "Mexiko",
    "MGL": "Mongolei",
    "MHL": "Marshallinseln",
    "MKD": "Nordmazedonien",
    "MLI": "Mali",
    "MLT": "Malta",
    "MNE": "Montenegro",
    "MON": "Fürstentum Monaco",
    "MOZ": "Mosambik",
    "MRI": "Mauritius",
    "MTN": "Mauretanien",
    "MYA": "Myanmar",
    "NAM": "Namibia",
    "NCA": "Nicaragua",
    "NED": "Niederlande",
    "NEP": "Nepal",
    "NGR": "Nigeria",
    "NIG": "Niger",
    "NOR": "Norwegen",
    "NRU": "Nauru",
    "NZL": "Neuseeland",
    "OMA": "Oman",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PAR": "Paraguay",
    "PER": "Peru",
    "PHI": "Philippinen",
    "PLE": "Palästina",
    "PLW": "Palau",
    "PNG": "Papua-Neuguinea",
    "POL": "Polen",
    "POR": "Portugal",
    "PRK": "Nordkorea",
    "PUR": "Puerto Rico",
    "QAT": "Katar",
    "ROU": "Rumänien",
    "RSA": "Südafrika",
    "RUS": "Russland",
    "RWA": "Ruanda",
    "SAM": "Samoa",
    "SEN": "Senegal",
    "SEY": "Seychellen",
    "SGP": "Singapur",
    "SKN": "St. Kitts und Nevis",
    "SLE": "Sierra Leone",
    "SLO": "Slowenien",
    "SMR": "San Marino",
    "SOL": "Salomonen",
    "SOM": "Somalia",
    "SRB": "Serbien",
    "SRI": "Sri Lanka",
    "STP": "São Tomé und Príncipe",
    "SUD": "Sudan",
    "SUI": "Schweiz",
    "SUR": "Suriname",
    "SVK": "Slowakei",
    "SWE": "Schweden",
    "SWZ": "Eswatini",
    "SYR": "Syrien",
    "TAN": "Tansania",
    "TGA": "Tonga",
    "THA": "Thailand",
    "TJK": "Tadschikistan",
    "TKM": "Turkmenistan",
    "TLS": "Osttimor",
    "TOG": "Togo",
    "TPE": "Taiwan",
    "TTO": "Trinidad und Tobago",
    "TUN": "Tunesien",
    "TUR": "Türkei",
    "TUV": "Tuvalu",
    "UAE": "Vereinigte Arabische Emirate",
    "UGA": "Uganda",
    "UKR": "Ukraine",
    "URU": "Uruguay",
    "USA": "Vereinigte Staaten von Amerika",
    "UZB": "Usbekistan",
    "VAN": "Vanuatu",
    "VEN": "Venezuela",
    "VIE": "Vietnam",
    "VIN": "St. Vincent und die Grenadinen",
    "YEM": "Jemen",
    "ZAM": "Sambia",
    "ZIM": "Simbabwe"
}
# Constants for race_data pdfs
DIST_INTERVALS = ["10", "25", "50"]
RACE_DIST = "2000"

"""
################################################################
General Utils
################################################################
"""


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df_regex = [
        r'\s+$',  # one or more whitespaces from end
        r'^\s+',  # one or more whitespaces from start
        r'\n'  # linebreak
    ]
    new_df = df.replace(df_regex, ['' for _ in df_regex], regex=True)
    return new_df


def print_stats(total: int, errors: int, empties: int, rate: str) -> None:
    """ Prints basic statistics for the pdf reading process. """
    # replace by logger.info
    print("{txt:-^25}".format(txt=f"\nRead: {total - errors}/{total} PDFs | ({rate}%)"))
    print("{txt:-^25}".format(txt=f" Empty Files: {empties} "))


def check_speed_stroke(df: pd.DataFrame, lb: float = 0.0, ub: float = float('inf')) -> list:
    """ Removes linebreaks, fills non numeric values with 0, returns: list """
    df = df.replace('\\n', ' ', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
    return [x if (lb <= x <= ub) else 0 for x in list(np.concatenate(np.array(df)))]


def convert_string_to_sec(string: str) -> int:
    if ':' in string:
        minutes = re.findall(r"(\d+):", string)[0]
        seconds = re.findall(r"(\d+)\.", string)[0]
        return round(int(60 * int(minutes) + int(seconds)), 2)
    else:
        return int(re.findall(r"(\d+)\.", string)[0])


'''
################################################################
WorldRowing Utils
################################################################
'''


def get_string_loc(df: pd.DataFrame, *args: str, country: bool = False, rank: bool = False, first: bool = False,
                   column: int = -1, results: bool = 0) -> dict:
    """ Returns: dict with string locations
    ------------
    Parameters:
    * df:           pandas DataFrame
    * *args:        option to search for arbitrary number of strings
    * country:      true/false if country row should be identified
    * rank:         true/false if rank row should be identified
    * first_loc:    true/false whether only the first occurrence should be checked (only relevant for random str and Rank)
    * column:       option to specify column
    * results:      0 = race_data.pdf | 1 = results.pdf
    ------------
    Return: dict with row, col indices for string args, country and rank
    """
    cntry_str, rank_str = "Country", "Rank"
    codes = COUNTRY_CODES.keys()

    locs: dict = {
        "str": {"row": [], "col": []},
        "cntry": {"row": [], "col": []},
        "rank": {"row": [], "col": []}
    }

    if args:
        if column == -1:
            col_list = []
            for search_str in args:
                for col in df.columns:
                    if df[col].str.contains(search_str).any():
                        col_list.append(col)
            col_list = list(set(col_list))  # remove duplicates
            col_list.sort()
            if col_list:
                locs["str"]["col"] = col_list[0] if first else col_list
        else:
            assert args[0] in df.values, "First arg not in DataFrame"
            locs["str"]["row"] = df.index[df[column] == args[0]].values[0]

    if country and not results:
        # For race data pdfs we want to find either the row that contains the word "Country"
        # or the row that has most country code occurrences.
        cntry_str_found = df.isin([cntry_str]).any().any()
        if cntry_str_found:
            locs["cntry"]["row"] = [df.index[df[0] == cntry_str].values[0]]
        else:
            row_lst = []
            for col in df.columns:
                contains_code = df[col].str.contains('|'.join(codes), na=False)
                occurrence = df.loc[contains_code]
                row = int(occurrence.index[0]) if occurrence.size > 0 else None
                if isinstance(row, int):
                    row_lst.append(row)
            if row_lst:
                locs["cntry"]["row"] = [max(set(row_lst), key=row_lst.count)]

    elif country and results:
        # for results pdfs find all row-wise occurrences of country codes even if in multiple columns
        country_rows, country_codes = [], '|'.join(codes)
        for row in range(df.shape[0]):
            row_data = df.iloc[row].values.reshape(-1)
            data_el = list(filter(None, [re.findall(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", str(data)) for data in row_data]))
            if any([str(el[0]) in country_codes for el in data_el if el]):
                country_rows.append(row)
        locs["cntry"]["row"] = country_rows

    if rank and not column == -1 and not df.empty:
        ranks_contained = df[column].str.contains(rank_str, na=False)
        ranks_str_found = ranks_contained.any()
        if ranks_str_found:
            rank_row = df.index[ranks_contained][0]
            locs["rank"]["row"] = rank_row
            locs["rank"]["col"] = 0

    country_row_data = locs["cntry"]["row"]
    country_row_data = list(set(country_row_data))
    country_row_data.sort()
    locs["cntry"]["row"] = country_row_data

    return locs


def get_data_loc(df: pd.DataFrame, cust_str: str = '') -> tuple[int, int]:
    """ Find indices of race data (only speed and stroke in the table).
    --------------
    Parameters:
    * cust_str:     If provided: Search for individual start and end.
    *               If not provided: Final data value is expected to be at 2000.
    -------------
    Returns:        tuple of row indices (start, end) of race data.
    """
    start, end = 0, 0
    first_column = df[0].values.flatten().tolist()
    dists = [re.sub(r"\n.*", "", str(x)) for x in first_column]

    try:
        if cust_str and cust_str in df.values:
            start = get_string_loc(df, cust_str, column=0)["str"]["row"]
        elif cust_str and cust_str in dists:
            start = dists.index(cust_str)
        else:
            for i in DIST_INTERVALS:
                if i in df.values:
                    start = get_string_loc(df, i, column=0)["str"]["row"]
                    break
            if start == 0 and end == 0:
                for i in DIST_INTERVALS:
                    if i in dists:
                        start = dists.index(i)
                        break
        end = last_num_idx(df)

    except Exception as e:
        logging.error(f"Error finding data start/end: \n{e}")

    return start, end


def handle_table_partitions(tables, results: bool = 0):
    """ Camelot may create multiple table objects, e.g. when data is spread across multiple pages.
    This function should aggregate all tables to a single df.
    ----------
    Parameters:
    * tables:       table list from camelot-py
    * results:      0 = race_data.pdf, 1 = results.pdf
    ----------
    Returns:        pd.DataFrame containing all subframes
    """
    df = pd.DataFrame()
    # store interval and previous table end to keep track of where to join the data frames
    interval = tab_end = 0
    # edge case check, only keep dataframes that contain relevant data
    checked_dfs = []
    for idx, tab in enumerate(tables):
        checked_df = handle_edge_cases(tab.df, results=results)
        if not checked_df.empty:
            checked_dfs.append(checked_df)
        # if consecutive dataframes contain the same data, only the last one is appended
        elif idx > 0 and tables[idx].df.equals(tables[idx - 1].df):
            checked_dfs.append(tables[idx])

    # if no relevant data is extracted return empty dataframe
    if not checked_dfs:
        return df

    raw_dataframes = [split_column_at_string(dataframe) for dataframe in checked_dfs]

    # iterate over dataframes and apply merging logic
    for idx, table in enumerate(raw_dataframes):
        # first table
        if idx == 0:
            first_df = table
            # if edge case error, empty df is returned only continue if df is not empty
            if not first_df.empty:
                # handle race data pdfs; result pdfs can just be appended
                if results == 0:
                    # get distance interval, e.g. 25, 50 depending on scale
                    first_tab = first_df.apply(pd.to_numeric, errors='coerce')
                    interval = first_tab[0].diff().mode()[0].astype("int")
                    last_dist_index = last_num_idx(first_df)
                    # set table_end to current last value of df
                    tab_end_data = first_df.iat[last_dist_index, 0]
                    tab_end = int(tab_end_data)
                    # drop rows below
                    first_df = first_df.drop(first_df.index[last_dist_index + 1:])
                    # remove columns that contain no data
                    data_start = get_data_loc(first_df)[0]
                    data_row_len = first_df[0].shape[0]
                    empty_cols = []
                    for col in first_df.columns:
                        if set(first_df[col].iloc[data_start:data_row_len].values).issubset(["", None]):
                            empty_cols.append(col)
                    for k, g in groupby(enumerate(empty_cols), lambda x: x[0] - x[1]):
                        group = list(map(int, (map(itemgetter(1), g))))
                        new_cols = first_df.iloc[:, group[0]:group[-1]+1]
                        first_df[group[0]-1] = first_df[group[0]-1].str.cat(new_cols, na_rep=" ")
                    first_df = reset_axis(first_df.drop(empty_cols, axis=1), axes=[1])
                df = pd.concat([df, first_df], ignore_index=True)

        # when there are more tables (and for race data pdfs final value for table_end (2000) is not reached)
        elif idx > 0 if results else (idx > 0 and tab_end != int(RACE_DIST)):
            next_df = table
            if not next_df.empty:
                if results == 0:
                    next_start = tab_end + interval
                    next_loc = get_data_loc(df=next_df, cust_str=str(next_start))
                    last_dist_idx = last_num_idx(next_df)
                    # set table_end to current last value of df
                    tab_end = int(next_df.iat[last_dist_idx, 0])
                    next_df = next_df.drop(next_df.index[last_dist_idx + 1:])
                    next_df = next_df.dropna(how='all', axis=1)
                    next_df = next_df.iloc[next_loc[0]:next_loc[1] + 1]
                    # append next_df part to main df
                    df = pd.concat([df, next_df], ignore_index=True)
                else:
                    rank_row = get_string_loc(next_df, rank=True, column=0)["rank"]["row"]
                    # remove everything above the rank row
                    next_df = next_df.iloc[rank_row:].copy()
                    df = pd.concat([df, next_df], ignore_index=True)
    return df


def apply_regex_sub(regular_expressions: list, repl: str = '', input_string: str = ''):
    """ applies regex sub on input string and returns resulting string. """
    new_str = input_string
    for regex in regular_expressions:
        new_str = re.sub(regex, repl, new_str)
    return new_str


def clean_str(str_list: list, style: str):
    """ Handles regular expressions to filter for specific data formats.
    -----------
    Parameters:
    * string:   input string
    * style:    time/name/country/number depending on the desired format
    -----------
    Returns:    Filtered string
    """
    type_dict = {
        "time": [r"\(.*?\)", r"[^0-9.:]"],
        "name": [r"[0-9.:]", r"\(.*?\)", r"[A-Z]{3}$", r"^\s[A-Z][a-z]+"],
        "country": [r"\(.*?\)", r"[0-9]", r"[A-Z]{1,2}[a-z]+", r"[A-Z]{4,}"],
        "number": [r"\d+$", r"\D"],
        "dist": [r"\d*\.\d+", r"\n", r"[^0-9,]", r"\n.*"]
    }
    final = []
    for el in str_list:
        final.append(apply_regex_sub(regular_expressions=type_dict.get(style), repl='', input_string=str(el)))
    filter_list = [None, "0", ""]
    final_list = list(filter(lambda x: x not in filter_list, final))
    if style == "dist":
        final_list = list(map(int, final_list))
    if style == "country":
        codes = '|'.join(COUNTRY_CODES.keys())
        final_list = [country for country in final_list if country in codes]
    if style == "name":
        final_list = list(filter(lambda x: x not in [None, 0, "0", "", " "], final_list))
    return final_list


def handle_edge_cases(df: pd.DataFrame, results=0) -> pd.DataFrame:
    """ This function handles edge cases, e.g. dataframe contains no race data.
    Takes dataframe and returns corrected df. In error cases empty df.should be returned.
    Parameters:
    * results:     0 = race_data.pdf | 1 = results.pdf
    """
    country_row_idx = get_string_loc(df, country=True)["cntry"]["row"]
    rank_row_idx = get_string_loc(df, rank=True, column=0)["rank"]["row"]
    data_row_idx = get_data_loc(df)

    # Edge Case 1: Dataframe contains no country and no rank (often the table head)
    # if no country found and no rank found discard table by returning empty dataframe
    if results and country_row_idx and rank_row_idx:
        return df
    elif not results and country_row_idx and data_row_idx[0] != 0:
        return df
    return pd.DataFrame()


'''
################################################################
Pandas Utils
################################################################
'''


def last_num_idx(df: pd.DataFrame, col: int = 0) -> int:
    """ Finds and returns index of last numeric value in DataFrame."""
    values = list(reversed(df[col].values))
    for idx, el in enumerate(values):
        if el.isdigit() and len(el) > 2:
            return (len(values) - 1) - idx
    return 0


def reset_axis(df: pd.DataFrame, axes: list) -> pd.DataFrame:
    for axis in axes:
        df = df.set_axis(list(np.arange(0, df.shape[axis])), axis=axis)
    return df


def clean_df(df: pd.DataFrame):
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    df = df.dropna(axis=1, how='all')
    df = df.fillna(0)
    df = reset_axis(df, axes=[0, 1])
    return df


def split_column_at_string(df: pd.DataFrame, split_str: str = '\n'):
    placeholder_df = pd.DataFrame()

    for col in df.columns:
        # find indices of linebreak ('\n') occurrences
        lb_idx = df.index[df[col].str.contains(split_str, regex=False)].to_numpy()
        if lb_idx.any():
            row_indices = [x for x in range(len(df.index)) if x not in lb_idx]
            df.iloc[row_indices, col] = split_str + df.iloc[row_indices, col].astype(str)

        if isinstance(df[col], pd.Series) and df[col].astype(str).str.contains(split_str).any():
            new_cols = df[col].astype(str).str.split(split_str, expand=True)
        else:
            new_cols = df[col]

        placeholder_df = pd.concat([placeholder_df, new_cols], axis=1)
    new_df = reset_axis(df=placeholder_df, axes=[1])
    return new_df
