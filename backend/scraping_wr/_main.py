from utils_wr import load_json
import requests

import logging

logger = logging.getLogger(__name__)

import utils_wr as ut_wr

########################################################################################################################
# NOTE:
# This main.py is just for rapid testing
########################################################################################################################

if __name__ == '__main__':
    ### KEEP FOR TESTING
    # todo: write tests for the functions below?
    # the current result is always 1000 rows long. Why is that?
    # races = api.get_races()
    # events = api.get_events()
    ##comps = api.get_competitions(kwargs={'extend_by': {'venue': True, 'country': True}})
    # comps = api.get_competitions()
    # stats = api.get_statistics()
    # comp_types = api.get_competitiontype()
    # boat_classes = api.get_boatclasses()
    # venues = api.get_venues()
    # countries = api.get_countries()
    ## --> countries can
    # merged = api.merge_race_event_competitions(races, events, comps)

    # _json_dict = ut.load_json(url=f'{api.WR_BASE_URL}{api.WR_ENDPOINT_STATS}')

    #year = 2010
    #year_filter = f"?filter[Year]={year}"
    #
    #filter_dict = {'year': 2010}
    #filter_dict = {'year': [2010, 2011]}
    #filter_str = ut_wr.build_filter_string(filter_dict)
    #j = load_json(url='https://world-rowing-api.soticcloud.net/stats/api/competition/' + filter_str)['data']
    #j = [comp['id'] for comp in j]
    #
    #ids = get_competition_ids('https://world-rowing-api.soticcloud.net/stats/api/competition/', 2010)
    #ids.extend(get_competition_ids('https://world-rowing-api.soticcloud.net/stats/api/competition/', 2011))

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
