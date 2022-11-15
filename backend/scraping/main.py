from world_rowing import api
import pandas as pd
from world_rowing import utils as ut

import logging

logging_level = logging.INFO
main_logger = logging.getLogger()
main_logger.setLevel(logging_level)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_level)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
stream_handler.setFormatter(formatter)

main_logger.addHandler(stream_handler)


def main():
    # the current result is always 1000 rows long. Why is that?
    races = api.get_races()
    events = api.get_events()
    comps = api.get_competitions()

    #stats = api.get_statistics()
    #comp_types = api.get_competitiontype()
    #boat_classes = api.get_boatclasses()

    merged = api.merge_race_event_competitions(races, events, comps)


    print()

if __name__ == "__main__":
    main()