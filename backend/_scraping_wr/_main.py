from utils_wr import load_json
import requests

import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    year = 2010
    year_filter = f"?filter[Year]={year}"

    filter_dict = {'year': 2010}
    filter_dict = {'year': [2010, 2011]}
    filter_str = build_filter_string(filter_dict)
    j = load_json(url='https://world-rowing-api.soticcloud.net/stats/api/competition/' + filter_str)['data']
    j = [comp['id'] for comp in j]

    ids = get_competition_ids('https://world-rowing-api.soticcloud.net/stats/api/competition/', 2010)
    ids.extend(get_competition_ids('https://world-rowing-api.soticcloud.net/stats/api/competition/', 2011))

    print()