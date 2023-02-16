import logging
import os
from time import sleep
import datetime
from contextlib import suppress

from sqlalchemy import select
from sqlalchemy.sql.expression import func
# https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__and__
from sqlalchemy import func, desc, and_, or_, not_
from sqlalchemy.orm import joinedload

from model import model
from model import dbutils
from scraper_procedures import postprocessing
from scraping_wr import api, pdf_race_data
from common import rowing
from common.helpers import Timedelta_Parser, get_

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from scraper_procedures.config import *
from scraper_procedures.prescraping import prescrape
from scraper_procedures.scraping import scrape

""" NOTES
- [SCRAPE] Procedure
    - Scrape from World Rowing API (scrapping_wr/api.py) and write to db (model/dbutils.py)
- [MAINTAIN] Procedure
    - Go through the database that already has much data in it (robust basis for statistics)
    - Parse PDF Data
    - Merge/Assign Data to the right boat
    - Decide what data seems higher quality and write it to the database

TODO

"""









# def _get_competitions_to_maintain(session):
#     """Returns tuple: competitions_iterator, number_of_competitions"""
#     DATA_PROVIDER_ID = model.Enum_Data_Provider.world_rowing.value
#     LEVEL_SCRAPED = model.Enum_Maintenance_Level.world_rowing_api_scraped.value
#     LEVEL_POSTPROCESSED = model.Enum_Maintenance_Level.world_rowing_api_postprocessed.value
#     scrape_before_date = datetime.datetime.now() - datetime.timedelta(days=int(SCRAPER_MAINTENANCE_PERIOD_DAYS))

#     statement = (
#         select(model.Competition)
#         .where(model.Competition.scraper_data_provider == DATA_PROVIDER_ID)
#         .where(
#             or_(
#                 model.Competition.scraper_maintenance_level == LEVEL_SCRAPED,
#                 and_(
#                     model.Competition.scraper_maintenance_level == LEVEL_POSTPROCESSED,
#                     model.Competition.scraper_last_scrape < scrape_before_date
#                 )
#             )
#         )
#     )
#     competitions = session.execute(statement).scalars().all()
#     return competitions, len(competitions)


def postprocess():
    logger = logging.getLogger("postprocessing")
    with model.Scoped_Session() as session:
        logger.info(f"Fetch & write world best times")
        postprocessing.refresh_world_best_times(session=session, logger=logger)

        logger.info("Outlier Marking")
        postprocessing.mark_outliers(session=session, logger=logger)


"""
        logger.info("Find competitions that have to be maintained")
        competitions, N = _get_competitions_to_maintain(session)
        logger.info(f"Found N={N} competitions")
        for competition in competitions:
            competition_uuid = competition.additional_id_
            if not competition_uuid:
                logger.error(f"Competition with id={competition.id} has no UUID (w.r.t. World Rowing API); Skip")
                continue
            logger.info(f"Competition id={competition.additional_id_}")

            # New concept: api.get_by_competition_id_(..., parse_pdf=True)
            #    -> does it make sense to put validation logic (db/model imports) inside api?

            logger.info("Fetch & Parse PDF")

            logger.info("Check Quality of both Datasets")

            # logger.info("Mark maintenance state in db") # Deprecated (?)
"""

def scheduler(duration=SCRAPER_SLEEP_TIME_SECONDS):
    logger = logging.getLogger("scheduler")

    logger.info(f"Waiting {duration} seconds ...")
    sleep(duration)


def start_service(singlepass=False):
    logger.info("[start_service]")
    while True:
        prescrape()
        scrape(parse_pdf=True)
        postprocess()

        if SCRAPER_SINGLEPASS or singlepass:
            logger.info("Override Scheduler")
            break

        scheduler()


if __name__ == '__main__':
    import argparse

    procedures = {
        "prescrape": prescrape,
        "scrape": scrape,
        "postprocess": postprocess
    }

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--procedure", help="Procedure to run",
        choices=list(procedures.keys()), action="append"
    )
    parser.add_argument("-s", "--singlepass", help="Ignore the scheduler. Script exits after one pass.", action="store_true")
    args = parser.parse_args()
    logger.info(args)

    
    if not args.procedure:
        start_service(singlepass=args.singlepass)
    else:
        for procedure_id in args.procedure:
            function = procedures[procedure_id]
            function()
