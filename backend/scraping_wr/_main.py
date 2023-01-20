import numpy as np

from .api import get_competition_ids, get_by_competition_id, get_by_competition_id_
from .utils_wr import load_json
import requests

import logging

logger = logging.getLogger(__name__)

from . import api
########################################################################################################################
# NOTE:
# This main.py is just for rapid testing
########################################################################################################################
import json
from sys import exit as sysexit


def grab_competition_example(competition_id, out_path='dump.json'):
    comp_data = get_by_competition_id_(comp_ids=[str(competition_id)], parse_pdf=False)
    with open(out_path, "w", encoding='ascii') as fp:
        json.dump(comp_data, fp)


if __name__ == '__main__':
    import argparse

    DEFAULT_COMPETITION = '718b3256-e778-4003-88e9-832c4aad0cc2'

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Available sub-commands', dest='command')
    parser_cgrab = subparsers.add_parser('grabc', help='Grab a competition and save as JSON')
    parser_cgrab.add_argument("-i", "--uuid", help="Scrape competition and save as JSON", default=DEFAULT_COMPETITION)
    parser_cgrab.add_argument("-o", "--out", help="Specify path for output", default="dump.json")

    args = parser.parse_args()
    print(args)

    if args.command == 'grabc':
        grab_competition_example(args.uuid, args.out)
        sysexit()

    ### KEEP FOR TESTING

    #_ids_all = []
    #for y in np.arange(2023, 2024):
    #    _ids_all.extend(get_competition_ids(y))
#
    # ret = api.get_by_competition_id(_ids_all, ['races'])
    #
    #
    # #api.save(ret, '2000_2020.json')
    # # load local json
    # #ret = api.load('2019_2020.json')
    ret = api.load('one_comp_id.json')
    # #
    # tuple_set__rsc_racePhase = set()
    # for race in ret['races']:
    #     rsc = race['RscCode'].split('---')
##
    #     rsc_0 = rsc[0].strip('--')
    #     rsc_1 = rsc[-1].strip('--')
    #     rpdn = ' '.join(race['DisplayName'].split(' ')[-3:-1])
    #     rp = race['racePhase']['DisplayName']
##
    # #     tuple_set__rsc_racePhase.add((rp, rsc_1))
##
    # # tuple_set__rsc_racePhase = sorted(tuple_set__rsc_racePhase)
    # competition_types = api.get_competition_categories()

    comp_categories = api.get_competition_categories()
    comp_types = api.get_competition_types()
    boat_classes = api.get_boatclasses()
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

