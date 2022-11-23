from backend.scraping.world_rowing import WRScraper
from backend.scraping.pdf_results import SOScraper



SCRAPER = [
    WRScraper,
    SOScraper
]

class Orchestrator:


    scrapers: dict

    def __init__(self):
         scrapers =

    def instantiate(self, types: dict[str:str], **kwargs):

        ret_val = {}
        return ''

    def scrape(self):

        for scraper in self.scrapers:
            data = scraper.get('', '' )







