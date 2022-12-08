import logging
from typing import Union, Optional, Iterator
from datetime import datetime, date

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
WR_INCLUDE_EVERYTHING = "?include=events.races,events.races.racePhase,events.races.raceStatus,events.races.racePhase,events.races.raceBoats.boat,events.races.raceBoats.raceBoatIntermediates.raceBoat,events.races.raceBoats.raceBoatAthletes.person,events.races.raceBoats.raceBoatIntermediates.distance,events.races.raceBoats.raceBoatIntermediates.distance"


########################################################################################################################


def _extract(nested: iter) -> list:
    """

    @param nested: iter: lazy generator. Used in the loop
    @return:
    """
    _l = []
    for item in list(nested):
        # item is a list itself
        _l.extend(item)

    return _l


def get_by_competition_id(ids: Union[str, list[str]], keys_of_interest: list[str]) -> dict:
    """
    Get the entities of interest (passed by keys_of_interest) for the id's passed.
    @param ids: Union[str, list[str]]: a singe OR a list of competition id's
    @param keys_of_interest: list[str]: a list of keys you are interested in. Possible keys: ['events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates']
    @return: dict[str]:
    """
    allowed_keys = {'events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates'}

    if not set(keys_of_interest).issubset(allowed_keys):
        logger.error(f"Some of the passed keys are not allowed: {set(keys_of_interest) - allowed_keys}")
        raise KeyError()

    if isinstance(ids, str):
        ids = [ids]

    ret_val = {koi: [] for koi in keys_of_interest}

    for id in ids:
        everything = ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + id + WR_INCLUDE_EVERYTHING)
        for koi in keys_of_interest:
            ret_val[koi].extend(
                _extract(
                    ut_wr.get_all(everything, koi)
                )
            )

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
    """ Fetches URLs to pdf files on https://d3fpn4c9813ycf.cloudfront.net/.
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

# def get_races(year: int = None, kind: str = None, kwargs: dict = {}):
#    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_RACE}', **kwargs)
#    return _json_dict
#
#
# def get_events(year: int = None, kind: str = None, kwargs: dict = {}):
#    _json_dict = ut_wr.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_EVENT}', **kwargs)
#    return _json_dict
