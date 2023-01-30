import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import Bundle
from model import model


def outlier_detection(session, boat_class: model.Boat_Class) -> None:
    logger = logging.getLogger("outlier_detector")

    logger.info(f'Analysing Boat Class "{boat_class.abbreviation}" with id={boat_class.id}')

    # https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.group_by
    # func.xxx ---> https://www.postgresql.org/docs/8.2/functions-aggregate.html
    statement = (
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
        .group_by(model.Intermediate_Time.distance_meter)
    )

    iterator = session.execute(statement)
    
    for row in iterator:
        print(
            f"distance: {row.distance_meter} meter",
            "count:", row.count,
            "mean:", row.arithmetic_mean,
            "stddev:", row.stddev,
            "max:", row.max
        )
    
    # ... do stuff to model.Intermediate_Time.is_outlier