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
        r'\s+$',    # one or more whitespaces from end
        r'^\s+',    # one or more whitespaces from start
        r'\n'       # linebreak
    ]
    new_df = df.replace(df_regex, ['' for _ in df_regex], regex=True)
    return new_df


def print_stats(total: int, errors: int, empties: int, rate: str) -> None:
    """ Prints basic statistics for the pdf reading process. """
    # replace by logger.info
    print("{txt:-^25}".format(txt=f"\nRead: {(total)-errors}/{total} PDFs | ({rate}%)"))
    print("{txt:-^25}".format(txt=f" Empty Files: {empties} "))


def clean_convert_to_list(df: pd.DataFrame) -> list:
    """ Removes linebreaks, fills non numeric values with 0, returns: list """
    df = df.replace('\\n', ' ', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce').astype(float).fillna(0)
    return np.concatenate(df.to_numpy()).tolist()


def convert_string_to_sec(string: str) -> int:
    min = re.findall(r"(\d+):", string)[0]
    sec = re.findall(r":(\d+)", string)[0]
    return round(int(60 * int(min) + int(sec)), 2)


'''
################################################################
WorldRowing Utils
################################################################
'''


def get_string_loc(df: pd.DataFrame, *args: str, country: bool = False, rank: bool = False, first: bool = False, column: int = -1, results: bool = 0) -> dict:
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
                occurence = df.loc[contains_code]
                row = int(occurence.index[0]) if occurence.size > 0 else None
                if isinstance(row, int):
                    row_lst.append(row)
            if row_lst:
                locs["cntry"]["row"] = [max(set(row_lst), key=row_lst.count)]

    elif country and results:

        # For for results pdfs we want to find all row-wise occurrences of country codes
        # even if they are in multiple columns
        i, row_idxs, country_codes = 0, [], '|'.join(codes)
        # from col 0 upwards check where country codes can be found
        while len(row_idxs) == 0 and i < df.shape[1]-1:
            find_row_idxs = df[i].str.contains(country_codes) == True
            row_idxs = df.index[find_row_idxs].tolist()
            # only check the following column if there are no athlete names
            next_col = df[i+1].isin([country_codes]).any()
            if next_col:
                locs["cntry"]["col"].extend([i, i+1])
                next_row_idxs = df.index[next_col].tolist()
                locs["cntry"]["row"].extend(next_row_idxs)
            else:
                locs["cntry"]["col"].append(i)
            i += 1
        locs["cntry"]["row"].extend(row_idxs)

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
    Returns: tuple of row indices (start, end) of race data.
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
    * tables:       Table list from camelot-py
    * results:      0 = race_data.pdf, 1 = results.pdf
    ----------
    Returns: Single pd.DataFrame
    """
    df = pd.DataFrame()
    # store interval and previous table end to keep track of how to merge the data
    interval = tab_end = 0
    # edge case check, only keep useful dataframes
    checked_dfs = []
    for idx, tab in enumerate(tables):
        checked_df = handle_edge_cases(tab.df, results=results)
        if not checked_df.empty:
            checked_dfs.append(checked_df)
        elif tables[idx].df.equals(tables[idx-1].df):
            checked_dfs.append(tables[idx])

    for idx, table in enumerate(checked_dfs):
        # When there is only one table the df can just be appended to main df
        if idx == 0:
            first_df = table
            # if edge case error, empty df is returned only continue if df is not empty
            if not first_df.empty:
                if results == 0:  # only apply on race data pdfs
                    # get distance interval, e.g. 25, 50 depending on scale
                    first_tab = first_df.apply(pd.to_numeric, errors='coerce')
                    interval = first_tab[0].diff().mode()[0].astype("int")
                    # set table_end to current last value of df
                    tab_end_data = first_df.iat[last_num_idx(first_df), 0]
                    tab_end = int(tab_end_data)
                df = pd.concat([df, first_df], ignore_index=True)
                # TODO: Handle linebreaks
                '''
                tab_end_data = re.sub(r"\d*\.\d+", "", tab_end_data)
                tab_end_data = re.sub(r"\n", "", tab_end_data)
                '''

        # When there are more tables (and for race data pdfs final value for table_end (2000) is not reached)
        elif idx > 0 if results else (idx > 0 and tab_end != int(RACE_DIST)):
            next_df = table
            if not next_df.empty:
                if results == 0:
                    next_start = tab_end + interval
                    next_loc = get_data_loc(
                        df=next_df, cust_str=str(next_start))
                    # set table_end to current last value of df
                    tab_end = int(next_df.iat[last_num_idx(next_df), 0])
                    next_df = next_df.iloc[next_loc[0]:next_loc[1]+1]
                    # append next_df part to main df
                    df = pd.concat([df, next_df], ignore_index=True)
                else:
                    rank_row = get_string_loc(next_df, rank=True, column=0)[
                        "rank"]["row"]
                    # remove everything above the rank row
                    next_df = next_df.iloc[rank_row:].copy()
                    df = pd.concat([df, next_df], ignore_index=True)

    return df


def apply_regex_sub(regexs: list, repl: str = '', input: str = ''):
    """ applies regex sub on input string and returns resulting string. """
    new_str = input
    for regex in regexs:
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
        "name": [r"[0-9.:]", r"\(.*?\)", r"[A-Z]{3}$"],
        "country": [r"\(.*?\)", r"[0-9]", r"[A-Z]{1,2}[a-z]+", r"[A-Z]{4,}"],
        "number": [r"\d+$", r"\D"],
        "dist": [r"\d*\.\d+", r"\n", r"[^0-9,]", r"\n.*"]
    }
    final = []
    for el in str_list:
        final.append(apply_regex_sub(
            regexs=type_dict.get(style), repl='', input=str(el)))
    filter_list = [None, "0", ""]
    final_list = list(filter(lambda el: el not in filter_list, final))
    if style == "dist":
        final_list = list(map(int, final_list))
    return final_list


def handle_edge_cases(df: pd.DataFrame, results=0) -> pd.DataFrame:
    """ This function handles edge cases, e.g. dataframe contains no race data.
    Takes dataframe and returns corrected df. In error cases empty df.should be returned.
    Parameters:
    * results:     0 = race_data.pdf | 1 = results.pdf
    """
    cnty_idx = get_string_loc(df, country=True)["cntry"]["row"]
    rank_idx = get_string_loc(df, rank=True, column=0)["rank"]["row"]

    # Edge Case 1: Dataframe contains no country and no rank (often the table head)
    # if no country found and no rank found discard table by returning empty dataframe
    if cnty_idx and (rank_idx if results else True):
        return df
    return pd.DataFrame()


'''
################################################################
Pandas Utils
################################################################
'''


def last_num_idx(df: pd.DataFrame, col: int = 0) -> int:
    """ Finds and returns index of last numeric value in DataFrame."""
    df = df[col].str.split('\n', expand=True)
    values = list(reversed(df[col].values))
    for idx, el in enumerate(values):
        if el.isdigit() and len(el) > 2:
            return (len(values)-1)-idx
    return 0


def clean_df(df: pd.DataFrame):
    """ Returns cleaned DataFrame and a list with indices of columns, that
        were removed because no relevant information was contained.
    """
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    # store names of empty columns
    df = df.dropna(axis=1, how='all')
    df = df.fillna(0)
    df = df.set_axis(list(np.arange(0, df.shape[1])), axis=1)
    df = df.set_axis(list(np.arange(0, df.shape[0])), axis=0)
    return df  # empties_list


def reset_axis(df: pd.DataFrame, axes: list) -> pd.DataFrame:
    for el in axes:
        df.set_axis(list(np.arange(0, df.shape[el])), axis=el)
    return df
