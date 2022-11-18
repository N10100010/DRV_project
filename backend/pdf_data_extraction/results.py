import camelot
import pycountry
import re

from utils import clean
from utils import clean_df
from utils import get_pdf_urls
from utils import get_string_loc
from utils import get_competition_ids
from utils import write_to_json

BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/competition/"
FILTER_STRING = "/?include=pdfUrls.orisCode,events.pdfUrls,events.races.pdfUrls.orisCode,events.boatClass,events.races.racePhase,events.races.photoFinishImage,events.races.raceBoats.raceBoatIntermediates.distance&sortInclude[pdfUrls.created_at]=asc&sortInclude[events.pdfUrls.DisplayName]=desc&sortInclude[events.races.pdfUrls.created_at]=asc"
NO_OF_COMPETITIONS = 40
COUNTRY_CODES_ALPHA_3 = [country.alpha_3 for country in pycountry.countries]
INTERMEDIATE_INTERVAL = 500

# TODO: Instantiate from Scraper and get all Results.pdfs


def extract_result_data(urls) -> list:
    result_data = []

    for url in urls:
        tables = camelot.read_pdf(url, flavor="stream", pages="all")
        df = clean(tables[0].df)

        # identify row idx of rank
        location = get_string_loc(df, rank=True)
        new_df, _ = clean_df(
            df.iloc[location["rank"]["rows"]:].copy())

        # get distance and country locations
        dists = ['500m', '1000m', '1500m', '2000m']
        dist_locs = get_string_loc(new_df, *dists)["str"]["cols"]
        country_locs = get_string_loc(new_df, country=True)[
            "cntry"]

        for cntry in country_locs["rows"]:

            # handle country code
            country_val = new_df.iloc[cntry:cntry + 1, country_locs["cols"]]
            country_name = re.sub(r'[0-9]', '', country_val.values[0])

            # initialize intermediate data dicts
            intermed_dict = {
                "country": country_name,
                "names": [],
                "times": None
            }
            times_dict = {}

            for key, dist in enumerate(dist_locs):
                time_val = new_df.iloc[cntry:cntry+1, dist].values[0]
                # remove all non-numeric stuff except . and :
                time_val = re.sub(r'[^0-9.:]', '', time_val)
                times_dict[(key+1)*INTERMEDIATE_INTERVAL] = time_val

            intermed_dict["times"] = times_dict
            result_data.append(intermed_dict)

    return result_data


competition_ids = get_competition_ids(base_url=BASE_URL)
urls = get_pdf_urls(base_url=BASE_URL, comp_ids=competition_ids,
                    comp_limit=NO_OF_COMPETITIONS, filter_str=FILTER_STRING, pdf_type=1)[74:75]
pdf_data = extract_result_data(urls=urls)

print(urls)
print(pdf_data)

# write result to test file
write_to_json(data=pdf_data, filename="result")
