from world_rowing import api
from world_rowing import utils as ut

# TODO: what about this website? http://wrmr2022.rowtiming.com/

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
    comps = api.get_competitions(kwargs={'extend_by': {'venue': True, 'country': True}})
    comps_1 = api.get_competitions()
    stats = api.get_statistics()
    comp_types = api.get_competitiontype()
    boat_classes = api.get_boatclasses()
    venues = api.get_venues()
    countries = api.get_countries()
    # --> countries can
    merged = api.merge_race_event_competitions(races, events, comps)

    _json_dict = ut.load_json(url=f'{api.WR_BASE_URL}{api.WR_ENDPOINT_STATS}')


    print()

if __name__ == "__main__":
    main()