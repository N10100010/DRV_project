import logging
import os
from time import sleep

from model import model

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__SCRAPER_DEV_MODE = os.environ.get('DRV_SCRAPER_DEV_MODE','').strip() == '1'
__SCRAPER_SLEEP_TIME_SECONDS = 5

""" NOTES
- [SCRAPE] Procedure
    - Scrape from World Rowing API (scrapping_wr/api.py) and write to db (model/dbutils.py)
- [MAINTAIN] Procedure
    - Go through the database that already has much data in it (robust basis for statistics)
    - Parse PDF Data
    - Merge/Assign Data to the right boat
    - Decide what data seems higher quality and write it to the database

TODO
- print() -> Logger
"""

def prescrape():
    logger = logging.getLogger("prescrape")

    logger.info("Fetch all competition heads and write to db")


def scrape():
    logger = logging.getLogger("scrape")

    logger.info("Grab competition 123-asd-123-asd")
    
    logger.info("Write competition to db")

    # Race Data PDF here or in maintain()


def maintain():
    logger = logging.getLogger("maintain")

    logger.info("Find unmaintained competition in db")

    logger.info("Found")

    logger.info("Fetch & Parse PDF")

    logger.info("Check Quality of both Datasets")

    logger.info("Overwrite in db")


def scheduler(duration=__SCRAPER_SLEEP_TIME_SECONDS):
    logger = logging.getLogger("scheduler")

    logger.info(f"Waiting {duration} seconds ...")
    sleep(duration)


def start_service():
    logger.info("[start_service]")
    while True:
        prescrape()
        scrape()
        maintain()

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
    args = parser.parse_args()
    logger.info(args)

    
    if not args.procedure:
        start_service()
    else:
        for procedure_id in args.procedure:
            func = procedures[procedure_id]
            func()
