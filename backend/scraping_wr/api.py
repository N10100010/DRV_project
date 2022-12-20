import logging
from typing import Union, Optional, Iterator
from datetime import datetime, date
import json as jsn


import numpy as np

import utils_wr as ut_wr

logger = logging.getLogger(__name__)

########################################################################################################################
# GLOBALS:
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"
WR_ENDPOINT_COMPETITION_CATEGORY = "competitionCategory/"
WR_ENDPOINT_COMPETITIONTYPE = "competitionType/"
WR_ENDPOINT_STATS = "statistic/"
WR_ENDPOINT_VENUE = "venue/"
WR_ENDPOINT_BOATCLASSES = "boatClass/"
WR_ENDPOINT_COUNTIRES = "country/"
WR_INCLUDE_EVERYTHING = "?include=" + ','.join([
    "events.pdfUrls",
    "events.races",
    "events.races.pdfUrls.orisCode",
    "events.races.racePhase",
    "events.races.raceStatus",
    "events.races.racePhase",
    "events.races.raceBoats.boat",
    "events.races.raceBoats.raceBoatIntermediates.raceBoat",
    "events.races.raceBoats.raceBoatAthletes.person",
    "events.races.raceBoats.raceBoatIntermediates.distance",
    "events.races.raceBoats.raceBoatIntermediates.distance"
    ])

# SELECTION FILTERS
OLYMPIC_BOATCLASS = [
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
    with open(fn, 'w') as file:
        jsn.dump(jsn.dumps(data), file)


def load(fn: str) -> dict:
    with open(fn, 'r') as file:
        j = jsn.loads(jsn.load(file))

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
            _l.extend(item)

    return _l


def get_by_competition_id(comp_ids: Union[str, list[str]], keys_of_interest: Union[str, list[str]], verbose: bool = False) -> dict:
    """
    Get the entities of interest (passed by keys_of_interest) for the id's passed.
    @param verbose: if or if not verbose
    @param comp_ids: Union[str, list[str]]: a singe OR a list of competition id's
    @param keys_of_interest: Union[str, list[str]]: a string = 'everything' OR a list of keys you are interested in.
        Possible keys: ['events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates']
    @return: dict[str]:
    """

    allowed_keys = {'events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates'}

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

    for i, _id in enumerate(comp_ids):
        everything = ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + _id + WR_INCLUDE_EVERYTHING)
        for koi in keys_of_interest:
            ret_val[koi].extend(
                _extract(
                    ut_wr.get_all(everything, koi)
                )
            )
        # verbose will break the condition before _len could not be defined
        if verbose and _len % (_len / 5):
            logger.info(f"Scraped {i / _len * 100} %")

    return ret_val


def get_competition_ids(years: Optional[Union[list, int]] = None) -> list[str]:
    """
    TODO: can we ask ONLY for the comp id, without overhead
    Gets the competition ids - optional by year.
    IF years is None aka not passed, the returned competition ids will be over the entire timeframe.
    --
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


def get_pdf_urls(comp_ids: list, results: bool, comp_limit: Optional[int] = None) -> list:
    """
     todo: rewrite to not having to use the endpoint....
     Fetches URLs to pdf files on https://d3fpn4c9813ycf.cloudfront.net/.
    ---------
    Parameters:
    * base_url:     for world rowing this is https://world-rowing-api.soticcloud.net/stats/api/competition/
    * comp_ids:     list of competition ids
    * comp_limit:   limit amount of competitions
    * filter_str:   filter parameter and values as string, e.g. '?include=events.races<...>'
    * results:      0 = "Race Data" | 1 = "Results"
    ---------
    Returns: list of urls for specified criteria
    """
    include_str = '/?include=pdfUrls.orisCode,events.pdfUrls,events.races.pdfUrls.orisCode'

    if comp_limit:
        comp_ids = comp_ids[0:comp_limit]

    urls = []
    doc_type = "Results" if results else "Race Data"

    for comp_id in comp_ids:
        url = WR_BASE_URL + WR_ENDPOINT_COMPETITION + comp_id + include_str
        events = ut_wr.load_json(url)["events"]
        pdfs = _extract(ut_wr.get_all(events, "pdfUrls"))
        for pdf in pdfs:
            if pdf["title"] == doc_type:
                urls.append(pdf["url"])

    return urls


def get_competitiontype(kwargs: dict = {}):
    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITIONTYPE}', **kwargs)
    return _json_dict


def get_countries(kwargs: dict = {}):
    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COUNTIRES}', **kwargs)
    return _json_dict


def get_boatclasses(kwargs: dict = {}):
    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_BOATCLASSES}', **kwargs)
    return _json_dict


def get_statistics(kwargs: dict = {}):
    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_STATS}', **kwargs)
    return _json_dict


def get_venues(kwargs: dict = {}):
    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_VENUE}', **kwargs)
    return _json_dict
