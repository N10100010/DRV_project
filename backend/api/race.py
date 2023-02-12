import datetime

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


def __debuggin_find_zero_result_times():
    with model.Scoped_Session() as session:
        stmt = (
            select(model.Intermediate_Time)
            .where(COND_VALID_2000M_RESULTS)
            .where(model.Intermediate_Time.result_time_ms == 0)
        )
        r = session.execute(stmt).scalars().all()
        for int_time in r:
            print(int_time.data_source)

if __name__ == '__main__':
    from sys import exit as sysexit

    from common.helpers import Timedelta_Parser
    print(Timedelta_Parser.to_millis("00:07:26.020"))
    print(Timedelta_Parser.to_millis("00:07:26.02"))

    __debuggin_find_zero_result_times() ; sysexit()

    with model.Scoped_Session() as session:
        for boat_class in session.scalars(select(model.Boat_Class)):
            res = result_time_best_of_year_interval(
                session=session,
                boat_class_id=boat_class.id,
                year_start=2020
            )
            print('result_time_best_of_last_n_years', res)