import datetime
from collections import OrderedDict
import itertools
import statistics

from sqlalchemy import select, or_, and_, func

from model import model

COND_VALID_2000M_RESULTS = and_(
    model.Intermediate_Time.distance_meter == 2000,
    model.Intermediate_Time.result_time_ms != None,
    model.Intermediate_Time.invalid_mark_result_code_id == None,
    or_(
        model.Intermediate_Time.is_outlier == False,
        model.Intermediate_Time.is_outlier == None
    )
)

def result_time_best_of_year_interval(session, boat_class_id, year_start,
                                      year_end=datetime.date.today().year):
    """returns result time as flot in ms"""

    statement = (
        select(
            func.min(model.Intermediate_Time.result_time_ms).label("shortest_result")
        )
        .join(model.Intermediate_Time.race_boat)
        .join(model.Race_Boat.race)
        .join(model.Race.event)
        .join(model.Event.boat_class)
        .join(model.Event.competition)
        .where(model.Boat_Class.id == boat_class_id)
        .where(model.Competition.year >= year_start)
        .where(model.Competition.year <= year_end)
        .where(COND_VALID_2000M_RESULTS)
    )

    result_time = session.execute(statement).one_or_none().shortest_result
    if not result_time == None:
        result_time = float(result_time)

    return result_time


def _transpose_boatclass_intermediates(race_boats) -> OrderedDict:
    transposed = dict()
    race_boat: model.Race_Boat
    for race_boat in race_boats:
        intermediate: model.Intermediate_Time
        for intermediate in race_boat.intermediates:
            dist = intermediate.distance_meter
            if not dist in transposed:
                transposed[dist] = []
            transposed[dist].append(intermediate)
    return transposed

def _skipping_non_int(values):
    """iterates only ints"""
    return ( val for val in values if isinstance(val,int) )

def _find_min_difference(values):
    min_diff = None
    last_val = None
    for idx, val in enumerate(_skipping_non_int(values)):
        first_loop = idx == 0
        if first_loop:
            last_val = val
            continue

        diff = val - last_val
        min_diff = diff if min_diff == None else min(diff, min_diff)
        last_val = val
    return min_diff

def compute_intermediates_figures(race_boats):
    """ returns: dict[race_boat_id][distance] each containing {"pace":..., ...}
    """
    dict_key = lambda i: i[0]
    lookup = _transpose_boatclass_intermediates(race_boats)
    lookup = OrderedDict( sorted(lookup.items(), key=dict_key ) )
    time_resolution = _find_min_difference(lookup.keys())
    if time_resolution == None:
        return []

    for distance, intermediates in lookup.items():
        best_time = ...
        deficit = ... # relative to best boat

        relDiffToAvgSpeed = ...
        rank  = ... #?

        pace = ... # None if diff to last_distance != time_resolution
        pass

    raise NotImplementedError


if __name__ == '__main__':
    from sys import exit as sysexit

    with model.Scoped_Session() as session:
        stmt = (select(model.Race))
        iterator = session.execute(stmt).scalars()
        for race in iterator:
            compute_intermediates_figures(race.race_boats)
            break

    sysexit()

    with model.Scoped_Session() as session:
        for boat_class in session.scalars(select(model.Boat_Class)):
            res = result_time_best_of_year_interval(
                session=session,
                boat_class_id=boat_class.id,
                year_start=2020
            )
            print('result_time_best_of_last_n_years', res)