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

    #_ids_all = []
    #for y in np.arange(2010, 2024):
    #    _ids_all.extend(get_competition_ids(y))
    ##
    #ret = api.get_by_competition_id(_ids_all, ['races'])

    #api.save(ret, './races_2010_2024.json')

    ret = api.load('./races_2010_2024.json')

    #
    #
    # #api.save(ret, '2000_2020.json')
    # # load local json
    # #ret = api.load('2019_2020.json')
    # ret = api.load('one_comp_id.json')
    # #
    tuple_set__rsc_racePhase = set()
    for race in ret['races']:
        boat_class, phase = api.process_rsc_code(race['RscCode'])
        # rsc = race['RscCode'].split('---')
        ##
        #rsc_0 = rsc[0].strip('--')
        #rsc_1 = rsc[-1].strip('--')
        rpdn = ' '.join(race['DisplayName'].split(' ')[-3:-1])
        rp = race['racePhase']['DisplayName']
        ##
        tuple_set__rsc_racePhase.add((rp, phase))
    ##
    tuple_set__rsc_racePhase = sorted(tuple_set__rsc_racePhase)
##
    # # tuple_set__rsc_racePhase = sorted(tuple_set__rsc_racePhase)
    # competition_types = api.get_competition_categories()

    #comp_categories = api.get_competition_categories()
    #comp_types = api.get_competition_types()
    #boat_classes = api.get_boatclasses()
    print()
    #
    # # extract race phases
    # race_phases = set()
    # race_statuses = set()
    # race_genders = set()  # races have gender? --> ofcourse they have gender ids. the races are separated by gender
    # for race in ret['races']:
    #     race_status = race['raceStatus']
    #     race_phase = race['racePhase']
    #     race_phases.add((race_phase['DisplayName'], race_phase['id']))
    #     race_statuses.add((race_status['DisplayName'], race_status['id']))
    #     race_genders.add(race['genderId'])
    #


    #ret = api.get_by_competition_id('718b3256-e778-4003-88e9-832c4aad0cc2', 'everything')
    #ret = api.load('./one_comp_id.json')


    print()  # breakpoint me

