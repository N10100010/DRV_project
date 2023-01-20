import logging
from typing import Union, Optional, Iterator
from datetime import datetime, date
import json as jsn


import numpy as np
tqdm = lambda i : i #from tqdm import tqdm

from . import utils_wr as ut_wr
from . import pdf_race_data as pdf_race_data
from . import pdf_result as pdf_result_data


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

########################################################################################################################
# GLOBALS:
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"
WR_ENDPOINT_COMPETITION_CATEGORIES = "competitionCategory/"
WR_ENDPOINT_COMPETITION_TYPES = "competitionType/"
WR_ENDPOINT_STATS = "statistic/"
WR_ENDPOINT_VENUE = "venue/"
WR_ENDPOINT_BOATCLASSES = "boatClass/"
WR_ENDPOINT_COUNTIRES = "country/"
WR_INCLUDE_EVERYTHING = "?include=" + ",".join(
    [
        "competitionType",
        "competitionType.competitionCategory",
        "venue",
        "venue.country",
        "events.gender",
        "events.boatClass",
        "events.pdfUrls",
        "events.races",
        "events.races.raceStatus",
        "events.races.racePhase",
        "events.races.raceBoats.boat",
        "events.races.raceBoats.invalidMarkResultCode",
        "events.races.raceBoats.country",
        "events.races.raceBoats.raceBoatAthletes.person",
        "events.races.raceBoats.raceBoatAthletes.person.country",
        "events.races.raceBoats.raceBoatIntermediates.distance",
        "events.races.pdfUrls.orisCode",
        "pdfUrls.orisCode"
    ]
)

# SELECTION FILTERS
OLYMPIC_BOATCLASSES = [
    "M1x",
    "LM2x",
    "W1x",
    "M2x",
    "M2-",
    "LW2x",
    "M4-",
    "W1x",
    "W2x",
    "W2-",
    "M4x",
    "M8+",
    "W4x",
    "W8+",
    "W4-",
]

BOATCLASSES_BY_GENDER_AGE_WEIGHT = {
    'men': {
        'junior': {
            'single': ("JM1x", "Junior Men's Single Sculls"),
            'double': ("JM2x", "Junior Men's Double Sculls"),
            'quad': ("JM4x", "Junior Men's Quadruple Sculls"),
            'pair': ("JM2-", "Junior Men's Pair"),
            'coxed_four': ("JM4+", "Junior Men's Coxed Four"),
            'four': ("JM4-", "Junior Men's Four") ,
            'eight': ("JM8-", "Junior Men's Eight")
        },
        'u19': {},
        'u23': {
            'single': ("BM1x", "U23 Men's Single Sculls"),
            'double': ("BM2x", "U23 Men's Double Sculls"),
            'quad': ("BM4x", "U23 Men's Quadruple Sculls"),
            'pair': ("BM2-", "U23 Men's Pair"),
            'coxed_four': ("BM4+", "U23 Men's Coxed Four"),
            'four': ("BM4-", "U23 Men's Four"),
            'eight': ("BM8+", "U23 Men's Eight"),
            'lw_single': ("BLM1x", "U23 Lightweight Men's Single Sculls"),
            'lw_double': ("BLM2x", "U23 Lightweight Men's Double Sculls"),
            'lw_quad': ("BLM4x", "U23 Lightweight Men's Quadruple Sculls"),
            'lw_pair': ("BLM2-", "U23 Lightweight Men's Pair"),
        },
        'adult': {
            'single': ("M1x", "Men's Single Sculls"),
            'double': ("M2x", "Men's Double Sculls"),
            'quad': ("M4x", "Men's Quadruple Sculls"),
            'pair': ("M2-", "Men's Pair"),
            'four': ("M4-", "Men's Four"),
            'eight': ("M8+", "Men's Eight"),
            'lw_single': ("LM1x", "Lightweight Men's Single Sculls"),
            'lw_double': ("LM2x", "Lightweight Men's Double Sculls"),
            'lw_quad': ("LM4x", "Lightweight Men's Quadruple Sculls"),
            'lw_pair': ("LM2-", "Lightweight Men's Pair"),
        },
        'pr': {
            '1': ("PR1 M1x", "PR1 Men's Single Sculls"),
            '2': ("PR2 M1x", "PR2 Men's Single Sculls"),
            '3': ("PR3 M2-", "PR3 Men's Pair")
        }
    },
    'women': {
        'junior': {
            'single': ("JW1x", "Junior Women's Single Sculls"),
            'double': ("JW2x", "Junior Women's Double Sculls"),
            'quad': ("JW4x", "Junior Women's Quadruple Sculls"),
            'pair': ("JW2-", "Junior Women's Pair"),
            'coxed_four': ("JW4+", "Junior Women's Coxed Four"),
            'four': ("JW4-", "Junior Women's Four") ,
            'eight': ("JW8-", "Junior Women's Eight")
        },
        'u19': {},
        'u23': {
            'single': ("BW1x", "U23 Women's Single Sculls"),
            'double': ("BW2x", "U23 Women's Double Sculls"),
            'quad': ("BW4x", "U23 Women's Quadruple Sculls"),
            'pair': ("BW2-", "U23 Women's Pair"),
            'coxed_four': ("BW4+", "U23 Women's Coxed Four"),
            'four': ("BW4-", "U23 Women's Four"),
            'eight': ("BW8+", "U23 Women's Eight"),
            'lw_single': ("BLW1x", "U23 Lightweight Women's Single Sculls"),
            'lw_double': ("BLW2x", "U23 Lightweight Women's Double Sculls"),
            'lw_quad': ("BLW4x", "U23 Lightweight Women's Quadruple Sculls"),
            'lw_pair': ("BLW2-", "U23 Lightweight Women's Pair"),
        },
        'adult': {
            'single': ("W1x", "Women's Single Sculls"),
            'double': ("W2x", "Women's Double Sculls"),
            'quad': ("W4x", "Women's Quadruple Sculls"),
            'pair': ("W2-", "Women's Pair"),
            'four': ("W4-", "Women's Four"),
            'eight': ("W8+", "Women's Eight"),
            'lw_single': ("LW1x", "Lightweight Women's Single Sculls"),
            'lw_double': ("LW2x", "Lightweight Women's Double Sculls"),
            'lw_quad': ("LW4x", "Lightweight Women's Quadruple Sculls"),
            'lw_pair': ("LW2-", "Lightweight Women's Pair"),
        },
        'pr': {
            '1': ("PR1 W1x", "PR1 Women's Single Sculls"),
            '2': ("PR2 W1x", "PR2 Women's Single Sculls"),
            '3': ("PR3 W2-", "PR3 Women's Pair")
        }
    },
    'mixed': {
        'double_2': ("PR2 Mix2x", "PR2 Mixed Double Sculls"),
        'double_3': ("PR3 Mix2x", "PR3 Mixed Double Sculls"),
        'four': ("PR3 Mix4+", "PR3 Mixed Coxed Four"),
    }
}


RACE_PHASES = {
    'Test Race': '92b34c4e-af58-4e91-8f4a-22c09984a006',
    'RoundOf16': 'ef6a596d-7de4-4646-81a7-7dbeaf515cfd',
    'Heat': 'cd3d5ca1-5aed-4146-b39b-a192ae6533f1',
    'Final': 'e0fc3320-cd66-43af-a5b5-97afd55b2971',
    'Preliminary': '92b34c4e-af58-4e91-8f4a-22c09984a006',
    'Seeding': '6c281206-2291-41bc-b9cd-5ecd82b1638c',
    'Repechage': '0959f5e8-f85a-40fb-93ab-b6c477f6aade',
    'Semifinal': 'e6693585-d2cf-464c-9f8e-b2e531b26400',
    'Quarterfinal': 'a0b6ffd8-92b8-427b-a667-ac2ff640031a'
}

RACE_STATUSES = {
    'Unofficial': 'd168a581-658d-40ad-8537-e3a07470b20a',
    'Cancelled': '3e5b4b12-4610-4f75-8b23-5f878e8ffc54',
    'Scheduled': 'f89cc288-076b-4bb6-9776-96e66820e1b8',
    'Official': '182f6f15-8e78-41c3-95b3-8b006af2c6a1'
}
########################################################################################################################


def save(data: dict, fn: str):
    with open(fn, 'w', encoding='ascii') as file:
        jsn.dump(data, file)


def load(fn: str) -> dict:
    with open(fn, 'r', encoding='ascii') as file:
        j = jsn.load(file)

    return j


def _extract(nested: iter, successor_filter: str = None) -> list:
    """
    Helper function extracting nested iterators
    @param nested: iter: lazy generator. Used in the loop
    @return: list: unpacked version of nested.
    """
    _l = []
    if successor_filter:
        for item in list(nested):
            _l.extend([_item[successor_filter] for _item in item])
    else:
        for item in list(nested):
            if isinstance(item, dict):
                _l.append(item)
            else:
                _l.extend(item)

    return _l



def select_pdf_(pdfUrls: list, title: str) -> Union[dict, None]:
    for pdf_info in pdfUrls:
        if pdf_info['title'].lower() == title.lower():
            return pdf_info

    return None # or raise error?



# Following functions are kinde of deprecated:
# PDF-Scrape, Parsing and Merge will be implemented in a second pass (aka background/cron process)
"""
def merge_intermediates(race, race_data):
    mappings = []
    '''mappings is a list of tuples of the form (race_idx, extra_data_idx)
    mappings = [ (1,0), (0,1) ]
    '''

    # TODO: Consider the case where raceBoats is empty but there is PDF data available
    for race_boat_idx, race_boat in enumerate(race.get('raceBoats', [])):
        for rd_idx, rd_item in race_data:
            if rd_item.get('boat_name','').strip().upper() == race_boat.get('DisplayName','').strip().upper():
                mappings.append( (race_boat_idx, rd_idx) )

    # apply the mapping
    for mapping in mappings:
        race_idx, race_data_idx = mapping
        race[race_idx]['pdf_parsed_intermediates'] = race_data[race_data_idx]


def merge_race_data(race, race_data):
    mappings = []
    '''mappings is a list of tuples of the form (race_idx, extra_data_idx)
    mappings = [ (1,0), (0,1) ]
    '''

    # TODO: Consider the case where raceBoats is empty but there is PDF data available
    for race_boat_idx, race_boat in enumerate(race.get('raceBoats', [])):
        for rd_idx, rd_item in race_data:
            if rd_item.get('boat_name','').strip().upper() == race_boat.get('DisplayName','').strip().upper():
                mappings.append( (race_boat_idx, rd_idx) )

    # apply the mapping
    for mapping in mappings:
        race_idx, race_data_idx = mapping
        race[race_idx]['pdf_parsed_race_data'] = race_data[race_data_idx]
"""

def get_by_competition_id_(comp_ids: Union[str, list[str]], verbose: bool = False, parse_pdf=False) -> dict:
    """
    Stripped down version of get_by_competition_id()
    """

    comp_id = comp_ids if isinstance(comp_ids, str) else comp_ids[0]

    comp_data = ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + comp_id + WR_INCLUDE_EVERYTHING)

    for event_idx, event in tqdm( enumerate(comp_data.get('events', [])) ):
        for race_idx, race in enumerate(event.get('races', [])):
            logger.info(f"event_idx {event_idx} race_idx {race_idx}")

            pdf_info_race_data = select_pdf_(race.get('pdfUrls', []), 'race data')
            pdf_info_results = select_pdf_(race.get('pdfUrls', []), 'results')

            if parse_pdf and pdf_info_results:
                pdf_url = pdf_info_results.get('url')
                logger.info(f"pdf_info_results {pdf_url}")
                # trigger parsing
                results_data = pdf_result_data.extract_table_data_from_pdf([pdf_url])[0]

                # TODO: merge using merge_intermediates()

                # write all at race level TODO: rem
                race['raceIntermediates_'] = results_data

            if parse_pdf and pdf_info_race_data:
                pdf_url = pdf_info_race_data.get('url')
                logger.info(f"pdf_info_race_data {pdf_url}")
                race_data = pdf_race_data.extract_table_data_from_pdf([pdf_url])[0]

                # TODO: merge using merge_race_data()
                # merge_race_data(race, race_data[0])

                race['raceData_'] = race_data

            # print("race_data_pdf_info", race_data_pdf_info['url'])

    return comp_data


def get_by_competition_id(comp_ids: Union[str, list[str]], keys_of_interest: Union[str, list[str]], verbose: bool = False) -> dict:
    """
    Get the entities of interest (passed by keys_of_interest) for the id's passed.
    @param verbose: if or if not verbose
    @param comp_ids: Union[str, list[str]]: a singe OR a list of competition id's
    @param keys_of_interest: Union[str, list[str]]: a string = 'everything' OR a list of keys you are interested in.
        Possible keys are denoted blow
    @return: dict[str]: list[dict]
    """

    allowed_keys = {
        'events', 'races', 'pdfs',
        'raceBoats', 'raceBoatAthletes',
        'raceBoatIntermediates',
        'venue', 'boatClass'
    }

    if isinstance(keys_of_interest, str) and keys_of_interest == 'everything':
        keys_of_interest = list(allowed_keys)
    else:
        logger.error("The passed string for 'keys_of_interest' does not match the string 'everything'. Check fct-call.")

    if not set(keys_of_interest).issubset(allowed_keys):
        logger.error(f"Some of the passed keys are not allowed: {set(keys_of_interest) - allowed_keys}")
        raise KeyError()

    if isinstance(comp_ids, str):
        comp_ids = [comp_ids]

    if verbose:
        _len = len(comp_ids)

    ret_val = {koi: [] for koi in keys_of_interest}

    for i, _id in tqdm(enumerate(comp_ids), desc='Aggregating WR endpoint data'):
        everything = ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + _id + WR_INCLUDE_EVERYTHING)
        for koi in keys_of_interest:
            ret_val[koi].extend(
                _extract(
                    ut_wr.get_all(everything, koi)
                )
            )

    # if race and pdfs is in the koi's, we want to aggregate the data from the pdf
    if 'races' in keys_of_interest and 'pdfs' in keys_of_interest:
        races = []
        for race in tqdm(ret_val['races'], desc='Aggregating PDF data'):
            race['pdfUrls'] = extract_pdf_urls(race['pdfUrls'])

            results_data = pdf_result_data.extract_data_from_pdf_urls(race['pdfUrls']['results'])[0]
            race_data = pdf_race_data.extract_data_from_pdf_url(race['pdfUrls']['race_data'])[0]
            race['results_data'] = results_data
            race['race_data'] = race_data
            races.append(race)

        ret_val['races'] = races

    return ret_val


def get_competition_ids(years: Optional[Union[list, int]] = None) -> list[str]:
    """
    TODO: can we ask ONLY for the comp id, without overhead
    Gets the competition ids - optional by year.
    IF years is None aka not passed, the returned competition ids will be over the entire timeframe.
    @param years: list or int, filtering the result
    @return: list[str] - a list of strings containing the competition ids for the years contained in the years argument
    """
    # current year + 5
    #  This is to make sure we get planned comps as well
    future_year = date.today().year + 5
    if years:
        filter_strings = [ut_wr.build_filter_string({'year': years})]
    else:
        filter_strings = [ut_wr.build_filter_string({'year': y}) for y in
                          np.arange(start=1900, stop=future_year, step=1)]

    comp_ids = []
    for fs in filter_strings:
        comp_ids.extend(
            ut_wr.extract_competition_ids(
                ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + fs)
            )
        )

    return comp_ids


def extract_pdf_urls(race_urls: list[dict]) -> dict:
    """
    Fetches URLs to pdf files on https://d3fpn4c9813ycf.cloudfront.net/
    @param race_urls: child-dict of the races result
    @return: dict of urls for 'race_data' and 'results'
    """

    ret_val = {
        'results': [],
        'race_data': []
    }

    for race_url in race_urls:
        if race_url['title'] == 'Results':
            ret_val['results'].append(race_url.get('url', None))
        elif race_url['title'] == 'Race Data':
            ret_val['race_data'].append(race_url.get('url', None))

    # sanity checking
    if len(ret_val['race_data']) != len(ret_val['results']):
        # todo: do we have to do smth about that?
        logger.warning("\nUnequal number of pdf-urls for race data and results data")

    return ret_val


def get_competition_categories(kwargs: dict = {}):
    ret_val = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITION_CATEGORIES}', **kwargs)
    return ret_val


def get_competition_types(kwargs: dict = {}):
    ret_val = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITION_TYPES}', **kwargs)
    return ret_val


def get_countries(kwargs: dict = {}):
    ret_val = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COUNTIRES}', **kwargs)
    return ret_val


def get_statistics(kwargs: dict = {}):
    ret_val = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_STATS}', **kwargs)
    return ret_val


def get_boatclasses(kwargs: dict = {}):
    ret_val = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_BOATCLASSES}', **kwargs)
    return ret_val
