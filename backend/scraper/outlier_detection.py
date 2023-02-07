
from sqlalchemy import select, update, or_, and_, func
from sqlalchemy.orm.session import Session
from model import model

from tqdm import tqdm 

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def outlier_detection(session:Session, boat_class: model.Boat_Class) -> None:
    adjusted = 0

    logger = logging.getLogger("outlier_detector")
    logger.info(f"Boat Class: {boat_class.abbreviation}")

    # https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.group_by
    # func.xxx ---> https://www.postgresql.org/docs/8.2/functions-aggregate.html
    intermediate_statement = (
        select(
            model.Intermediate_Time.distance_meter,
            model.Competition_Category.id.label('competition_category_id')
        )
        .join(model.Intermediate_Time.race_boat)
        .join(model.Race_Boat.race)
        .join(model.Race.event)
        .join(model.Event.competition)
        .join(model.Competition.competition_category)
        .where(model.Event.boat_class_id == boat_class.id)
        .order_by(model.Intermediate_Time.distance_meter)
        .group_by(
            model.Intermediate_Time.distance_meter,
            model.Competition_Category.id
        )
    )

    wbt_statement = (
        select(
            model.Boat_Class.id, 
            model.Race_Boat.result_time_ms
        )
        .join(model.Race_Boat)
        #.where(model.Boat_Class.id == boat_class.id ) # todo: results in empty list?
    )

    intermediates = session.execute(intermediate_statement).all()

    if len(intermediates) == 0: 
        logger.info(f"Skipping boat class: {boat_class.id}. No intermediates with this boatclass")
        return None

    wbts = session.execute(wbt_statement).all()
    wbt = [wb[1] for wb in wbts if wb[0] == boat_class.id]
    wbt = wbt[0] if len(wbt) > 0 else 0
    longest_distance = intermediates[-1].distance_meter



    for row in tqdm(intermediates):

        logger.debug(f"  Competition Category: {row.competition_category_id}")

        percentiles_statement = (
            select(
                [
                    func.percentile_cont(.001).within_group(model.Intermediate_Time.result_time_ms.desc()),
                    func.percentile_cont(.999).within_group(model.Intermediate_Time.result_time_ms.desc()),
                ],
            )
            .join(model.Intermediate_Time.race_boat)
            .join(model.Race_Boat.race)
            .join(model.Race.event)
            .join(model.Event.competition)
            .join(model.Competition.competition_category)
            .where(
                and_(
                    model.Event.boat_class_id == boat_class.id,
                    model.Intermediate_Time.distance_meter == row.distance_meter,
                    model.Competition_Category.id == row.competition_category_id,
                    model.Intermediate_Time.result_time_ms != 0
                )
            )
        )

        percentiles = sorted(session.execute(percentiles_statement).fetchall()[0])
        if (row.distance_meter < longest_distance and wbt != 0): 
            _min = wbt
            logging.debug("Use WBT for min")
        else: 
            _min = percentiles[0]
        _min = percentiles[0]
        _max = percentiles[1]

        if _min > _max or _min == 0: 
            print()

        to_adjust_statement = (
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
                    ~model.Intermediate_Time.result_time_ms.between(_min, _max),
                    model.Intermediate_Time.distance_meter == row.distance_meter,
                    model.Competition_Category.id == row.competition_category_id
                )
            )
        )
        
        # print(
        #     f"",
        #     f"boatclass: {boat_class.id}",
        #     f"min: {_min}",
        #     f"max: {_max}",
        #     f"meter: {row.distance_meter}",
        #     f"comp cat: #{row.competition_category_id}"
        # )

        to_adjust = session.execute(to_adjust_statement).fetchall()
        adjusted += len(to_adjust)
        # todo: how to do a bulk-update? 
        for intermediate_id, distance_meter in to_adjust: 

            updt = update(model.Intermediate_Time)
            updt = updt.values({'is_outlier': True})
            updt = updt.where(model.Intermediate_Time.race_boat_id == intermediate_id)
            updt = updt.where(model.Intermediate_Time.distance_meter == distance_meter)

            session.execute(updt)
            session.commit()

    statement = (
        select(
            func.count(model.Intermediate_Time.race_boat_id)
        )
        .join(model.Intermediate_Time.race_boat)
        .join(model.Race_Boat.race)
        .join(model.Race.event)
        .where(model.Event.boat_class_id == boat_class.id)
    )
    total_row_count_boat_class = session.execute(statement).scalar()
    
    print(f"adjusted total : {adjusted} of {total_row_count_boat_class}")
    return None
