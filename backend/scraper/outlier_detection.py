import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from sqlalchemy import select, update, or_, and_, func
from sqlalchemy.orm.session import Session
from model import model


def outlier_detection(session:Session, boat_class: model.Boat_Class) -> None:

    logger = logging.getLogger("outlier_detector")
    logger.info(f"Boat Class: {boat_class.abbreviation} - labeling outliers")


    #logger.info(f'Analysing Boat Class "{boat_class.abbreviation}" with id={boat_class.id}')

    # https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.group_by
    # func.xxx ---> https://www.postgresql.org/docs/8.2/functions-aggregate.html
    intermediate_statement = (
        select(
            func.count(model.Intermediate_Time.result_time_ms),
            func.avg(model.Intermediate_Time.result_time_ms).label("arithmetic_mean"),
            func.stddev(model.Intermediate_Time.result_time_ms),
            func.max(model.Intermediate_Time.result_time_ms),
            model.Intermediate_Time.distance_meter
        )
        .join(model.Intermediate_Time.race_boat)
        .join(model.Race_Boat.race)
        .join(model.Race.event)
        .where(model.Event.boat_class_id == boat_class.id)
        .order_by(model.Intermediate_Time.distance_meter)
        .group_by(model.Intermediate_Time.distance_meter)
    )

    wbt_statement = (
        select(
            model.Boat_Class.id, 
            model.Race_Boat.result_time_ms
        )
        .join(model.Race_Boat)
        # .where(model.Boat_Class.id == boat_class.id ) # todo: results in empty list?
    )

    intermediates = session.execute(intermediate_statement).all()
    wbts = session.execute(wbt_statement).all()
    wbt = [wb[1] for wb in wbts if wb[0] == boat_class.id]
    wbt = wbt[0] if len(wbt) > 0 else 10000000


    factor = 3

    from tqdm import tqdm 

    for row in intermediates:
        # print(
        #     #f"distance: {row.distance_meter} meter",
        #     "count:", row.count,
        #     "mean:", row.arithmetic_mean,
        #     "stddev:", row.stddev,
        #     #"max:", row.max,
        # )
        _min, _max = row.arithmetic_mean - factor * row.stddev, row.arithmetic_mean + factor * row.stddev

        statement = (
            select(
                model.Intermediate_Time.race_boat_id,
                model.Intermediate_Time.distance_meter
            )
            .join(model.Intermediate_Time.race_boat)
            .join(model.Race_Boat.race)
            .join(model.Race.event)
            .where(
                and_(
                    model.Event.boat_class_id == boat_class.id,
                    or_(
                        model.Intermediate_Time.result_time_ms.between(_min, _max),
                        model.Intermediate_Time.result_time_ms < wbt
                    )
                )
            )
        )


        to_adjust = session.execute(statement).fetchall()
        for intermediate_id, distance_meter in to_adjust: 

            updt = update(model.Intermediate_Time)
            updt = updt.values({'is_outlier': True})
            updt = updt.where(model.Intermediate_Time.race_boat_id == intermediate_id)
            updt = updt.where(model.Intermediate_Time.distance_meter == distance_meter)

            session.execute(updt)
            session.commit()




    return None



    
    # ... do stuff to model.Intermediate_Time.is_outlier