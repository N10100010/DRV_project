import dataclasses


@dataclasses.dataclass
class DCMeta:
    ## fields
    def __init__(self):
        pass

    def __post_init__(self):
        pass




class BaseScraper:
    """

    """

    TYPE = None

    def __init__(self, type: str = ''):
        TYPE = type
        pass

    def scrape(self, kind, kwargs):
        pass

    def get_id(self) -> dict:
        return {
            'NAME': 'world_rowing',
            'SOURCE': ''
        }
