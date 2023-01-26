import logging
import os
from time import sleep
import datetime

from sqlalchemy import select
from sqlalchemy.sql.expression import func
# https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__and__
from sqlalchemy import and_, or_, not_

from model import model
from model import dbutils
from scraping_wr import api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCRAPER_SINGLEPASS = os.environ.get('SCRAPER_SINGLEPASS','').strip() == '1'
SCRAPER_DEV_MODE = os.environ.get('DRV_SCRAPER_DEV_MODE','').strip() == '1'
SCRAPER_YEAR_MIN = int(os.environ.get('SCRAPER_YEAR_MIN', '1900').strip())
SCRAPER_MAINTENANCE_PERIOD_DAYS = int(os.environ.get('SCRAPER_MAINTENANCE_PERIOD_DAYS', '7').strip())

DAY_IN_SECONDS = 60 * 60 * 24
SCRAPER_SLEEP_TIME_SECONDS = 1 * DAY_IN_SECONDS

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

def _scrape_range_half_year_window():
    today = datetime.date.today()
    second_half = today.month > 6
    if today.month > 6:
        return today.year, today.year+1
    return today.year-1, today.year

def _scrape_range_full_year_window():
    today = datetime.date.today()
    return today.year-1, today.year+1

def _detect_wr_scrapes(session):
    # HIGH-PRIO TODO: Introduce a field for source == WorldRowing
    statement = select(model.Competition.id).where(model.Competition.additional_id_ != None) 
    rows = session.execute(statement).first()
    detected = not rows == None
    return detected

def _scrape_competition_heads(session, year_min, year_max, logger=logger):
    if year_min > year_max:
        raise Exception(f"Year range is invalid: {year_min}-{year_max}")
    
    logger.info("Fetch all competition heads and write to db")
    for year in range(year_min, year_max+1):
        logger.info(f"Begin year={year} ---------------")
        competitions_wr = api.get_competition_heads([year], single_fetch=False)
        for competition_data in competitions_wr:
            logger.info(f'''Adding year={year} competition="{competition_data.get('id')}" name="{competition_data.get('DisplayName')}"''')
            dbutils.wr_insert(
                session,
                model.Competition,
                dbutils.wr_map_competition_prescrape,
                competition_data
            )


def prescrape(**kwargs):
    logger = logging.getLogger("prescrape")
    logger.info("Initialize Database")
    dbutils.create_tables(model.engine)

    year_min, year_max = _scrape_range_full_year_window() # smaller window with _scrape_range_half_year_window()

    with model.Scoped_Session() as session:
        logger.info("Trying to detect an earlier World Rowing API prescrape")
        wr_detected = _detect_wr_scrapes(session)
        if not wr_detected:
            logger.info("No World Rowing API scrapes detected: Extending scrape range to maximum")
            year_min = SCRAPER_YEAR_MIN
            # if SCRAPER_DEV_MODE:
            #     year_min = datetime.date.today().year-5
            # TODO: add a full_scrape / rescrape option

        logger.info(f"Final decision for year range selection: {year_min}-{year_max}")

        _scrape_competition_heads(session=session, year_min=year_min, year_max=year_max, logger=logger)
        session.commit()


def _get_competitions_to_scrape(session):
    """Returns tuple: competitions_iterator, number_of_competitions"""
    LEVEL_PRESCRAPED = model.Enum_Maintenance_Level.world_rowing_api_prescraped.value
    LEVEL_SCRAPED = model.Enum_Maintenance_Level.world_rowing_api_scraped.value
    DATA_PROVIDER_ID = model.Enum_Data_Provider.world_rowing.value

    statement = (
        select(model.Competition)
        .where(model.Competition.scraper_data_provider == DATA_PROVIDER_ID)
        .where(model.Competition.scraper_maintenance_level.in_( [LEVEL_PRESCRAPED, LEVEL_SCRAPED] ))
    ) 
    competitions = session.execute(statement).scalars().all()
    N = len(competitions) # TODO: Get rid of all() call and use a count query to get N: https://stackoverflow.com/a/65775282
    return competitions, N


def scrape():
    logger = logging.getLogger("scrape")
    with model.Scoped_Session() as session:
        competitions_iter, num_competitions = _get_competitions_to_scrape(session=session)
        logger.info(f"Competitions that have to be scraped N={num_competitions}")

        for competition in competitions_iter:
            competition_uuid = competition.additional_id_
            if not competition_uuid:
                logger.error(f"Competition with id={competition.id} has no UUID (w.r.t. World Rowing API); Skip")
                continue
            
            # High Prio TODO: introduce check if scraping should actually happen

            logger.info(f'''Fetching competition="{competition_uuid}" date="{competition.start_date}" name="{competition.name}"''')
            competition_data = api.get_by_competition_id_(comp_ids=[competition_uuid], parse_pdf=False)

            logger.info(f"Write competition to database")
            # let's use the mapper func directly since we already have the ORM instance
            competition = dbutils.wr_map_competition_scrape(session, competition, competition_data)
            session.commit()

        session.commit()
        # Race Data PDF here or in maintain()

def _get_competitions_to_maintain(session):
    """Returns tuple: competitions_iterator, number_of_competitions"""
    DATA_PROVIDER_ID = model.Enum_Data_Provider.world_rowing.value
    LEVEL_SCRAPED = model.Enum_Maintenance_Level.world_rowing_api_scraped.value
    LEVEL_POSTPROCESSED = model.Enum_Maintenance_Level.world_rowing_api_postprocessed.value
    scrape_before_date = datetime.datetime.now() - datetime.timedelta(days=int(SCRAPER_MAINTENANCE_PERIOD_DAYS))

    statement = (
        select(model.Competition)
        .where(model.Competition.scraper_data_provider == DATA_PROVIDER_ID)
        .where(
            or_(
                model.Competition.scraper_maintenance_level == LEVEL_SCRAPED,
                and_(
                    model.Competition.scraper_maintenance_level == LEVEL_POSTPROCESSED,
                    model.Competition.scraper_last_scrape < scrape_before_date
                )
            )
        )
    )
    competitions = session.execute(statement).scalars().all()
    return competitions, len(competitions)

def maintain():
    logger = logging.getLogger("postprocessing")
    with model.Scoped_Session() as session:
        logger.info("Find competitions that have to be maintained")
        competitions, N = _get_competitions_to_maintain(session)
        logger.info(f"Found N={N} competitions")
        for competition in competitions:
            competition_uuid = competition.additional_id_
            if not competition_uuid:
                logger.error(f"Competition with id={competition.id} has no UUID (w.r.t. World Rowing API); Skip")
                continue
            logger.info(f"Competition id={competition.additio}")

            # New concept: api.get_by_competition_id_(..., parse_pdf=True)
            #    -> does it make sense to put validation logic (db/model imports) inside api?

            logger.info("Fetch & Parse PDF")

            logger.info("Check Quality of both Datasets")

            logger.info("Overwrite in db")


def scheduler(duration=SCRAPER_SLEEP_TIME_SECONDS):
    logger = logging.getLogger("scheduler")

    logger.info(f"Waiting {duration} seconds ...")
    sleep(duration)


def start_service(singlepass=False):
    logger.info("[start_service]")
    while True:
        prescrape()
        scrape()
        maintain()

        if SCRAPER_SINGLEPASS or singlepass:
            logger.info("Override Scheduler")
            break

        scheduler()


if __name__ == '__main__':
    import argparse

    procedures = {
        "prescrape": prescrape,
        "scrape": scrape,
        "maintain": maintain
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
            func = procedures[procedure_id]
            func()
