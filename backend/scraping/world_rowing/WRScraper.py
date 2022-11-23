from backend.scraping.base.baseScraper import BaseScraper


class WRScraper(BaseScraper):
    def __init__(self, type: str = ''):
        super().__init__(type='WorldRowing')

    def scrap(self, kind, kwargs):
        pass
        # do your thing




