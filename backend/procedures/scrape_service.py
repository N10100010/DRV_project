from ..model import model

""" NOTES
- [SCRAPE] Procedure
    - Scrape from World Rowing API (scrapping_wr/api.py) and write to db (model/dbutils.py)
- [MAINTAIN] Procedure
    - Go through the database that already has much data in it (robust basis for statistics)
    - Parse PDF Data
    - Merge/Assign Data to the right boat
    - Decide what data seems higher quality and write it to the database
"""

def scrape():
    print("[scrape]", "Grab competition 123-asd-123-asd")
    
    print("[scrape]", "Write competition to db")

    # Race Data PDF here or in maintain()


def maintain():
    print("[maintain]", "Find unmaintained competition in db")

    print("[maintain]", "Found")

    print("[maintain]", "Fetch & Parse PDF")

    print("[maintain]", "Check Quality of both Datasets")

    print("[maintain]", "Overwrite in db")


def start_service():
    print("[start_service]")
    for i in range(5):
        scrape()
        maintain()
        # sleep()

if __name__ == '__main__':
    import argparse

    SCRAPE_ID = 'scrape'
    MAINTAIN_ID = 'maintain'

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--procedure", help="Procedure to run", choices=[SCRAPE_ID, MAINTAIN_ID], action="append")
    args = parser.parse_args()
    print(args)

    
    if not args.procedure:
        start_service()
    else:
        if SCRAPE_ID in args.procedure:
            scrape()
        
        if MAINTAIN_ID in args.procedure:
            maintain()
