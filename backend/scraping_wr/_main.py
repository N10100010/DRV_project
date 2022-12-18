import numpy as np

from backend.scraping_wr.api import get_competition_ids, get_by_competition_id
from utils_wr import load_json
import requests

import logging

logger = logging.getLogger(__name__)

import utils_wr as ut_wr
import api as api
########################################################################################################################
# NOTE:
# This main.py is just for rapid testing
########################################################################################################################
import json as jsn



if __name__ == '__main__':
    ### KEEP FOR TESTING
    # todo: write tests for the functions below?
    # the current result is always 1000 rows long. Why is that?
    #races = api.get_races()
    #events = api.get_events()
    #comps = api.get_competitions(kwargs={'extend_by': {'venue': True, 'country': True}})
    #comps = api.get_competitions()
    #stats = api.get_statistics()
    #comp_types = api.get_competitiontype()
    #boat_classes = api.get_boatclasses()
    #venues = api.get_venues()
    #countries = api.get_countries()
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


    # SMALL TEST FOR THE GET_PDF_URLS FUNCTION

    #ids_2010 = api.get_competition_ids(years=2022)
    #result_urls = api.get_pdf_urls(comp_ids=ids_2010, results=True)

    #ids = ['b56cf9a5-a7d3-4e64-9571-38218f39413b']

    #ids_with_urls = ['718b3256-e778-4003-88e9-832c4aad0cc2', '6f177182-6b70-49b7-8e81-abfe36f1ba04', '14747dc9-c824-4866-9bad-ff9162b931c4', 'b56cf9a5-a7d3-4e64-9571-38218f39413b', 'c5baea20-06b5-41c8-87bf-b1d98b778bce', '7ee519e5-288d-4585-bab4-bf916dca49b8', '28608aee-911f-48a2-9598-36949cbc0169']


    # TODO: NOTE: check the different occuring tuples of race_pases and race.rscCodes
    # _ids_all = []
    # for y in np.arange(1990, 2020):
    #     _ids_all.extend(get_competition_ids(y))
    #
    # ret = api.get_by_competition_id(_ids_all, ['events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates'])
    #
    # tup_set = set()
    # l = list()
    # for race in ret['races']:
    #     rsc = race['RscCode'].split('---')
    #
    #     rsc_0 = rsc[0].strip('--')
    #     rsc_1 = rsc[-1].strip('--')
    #     rpdn = ' '.join(race['DisplayName'].split(' ')[-3:-1])
    #     rp = race['racePhase']['DisplayName']
    #
    #     tup_set.add((rp, rsc_1))
    #     l.append((rp, rsc_1))
    #
    # tup_set = sorted(tup_set)

    # _ids_all = []
    # for y in np.arange(2019, 2020):
    #     _ids_all.extend(get_competition_ids(y))
    # ret = api.get_by_competition_id(_ids_all, ['events', 'races', 'raceBoats', 'raceBoatAthletes', 'raceBoatIntermediates'], )
    #
    # save(ret, '2000_2020.json')
    # # load local json
    # #ret = load('2019_2020.json')
    # ret = load('2000_2020.json')
    #
    # # extract race phases
    # race_phases = set()
    # race_statuses = set()
    # race_genders = set()  # races have gender? --> ofcourse they have gender ids. the races are separated by gender
    # for race in ret['races']:
    #     race_status = race['raceStatus']
    # #    race_phase = race['racePhase']
    # #    race_phases.add((race_phase['DisplayName'], race_phase['id']))
    #     #race_statuses.add((race_status['DisplayName'], race_status['id']))
    #     race_genders.add(race['genderId'])

    #races = api.get_races()

    comp_types = api.get_competitiontype()
    countries = api.get_countries()
    boat_classes = api.get_boatclasses()
    stats = api.get_statistics()
    venueues = api.get_venues()


    print()

