from typing import Union, Optional
from datetime import datetime, date

import numpy as np

import utils_general as ut_general
import utils_wr as ut_wr
import utils_pdf as ut_pdf

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
########################################################################################################################


def get_competition_ids(years: Optional[Union[list, int]] = None) -> list[str]:
    """
    Gets the competition ids - optional by year.
    IF years is None aka not passed, the returned competition ids will be over the entire timeframe.
    --
    @param years: list or int, filtering the result
    @return:
    """
    # current year + 5
    #  This is to make sure we get planned comps as well
    future_year = date.today().year + 5
    if years:
        filter_strings = [ut_wr.build_filter_string({'year': years})]
    else:
        filter_strings = [ut_wr.build_filter_string({'year': y}) for y in np.arange(start=1900, stop=future_year, step=1)]

    comp_ids = []
    for fs in filter_strings:
        comp_ids.extend(
            ut_wr.extract_competition_ids(
                ut_wr.load_json(WR_BASE_URL + WR_ENDPOINT_COMPETITION + fs)
            )
        )

    return comp_ids


def get_pdf_urls(comp_ids: list,  results: bool, comp_limit: Optional[int] = None) -> list:
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

        for event in events:
            races = event["races"]
            for race in races:
                for pdf in race["pdfUrls"]:
                    if pdf["title"] == doc_type:
                        urls.append(pdf["url"])
    return urls


if __name__ == '__main__':

    # SMALL TEST FOR THE GET_COMPETITION_IDS FUNCTION
    #ids_all = get_competition_ids()
    #
    #_ids_all = []
    #for y in np.arange(1900, 2030):
    #    _ids_all.extend(get_competition_ids(y))

    # SMALL TEST FOR THE GET_PDF_URLS FUNCTION
    #ids_2010 = get_competition_ids(years=2010)
    #result_urls = get_pdf_urls(comp_ids=ids_2010, results=True)


    print()



