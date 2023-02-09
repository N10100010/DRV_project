import os
import datetime
import json
from statistics import stdev, median, mean

from flask import Flask
from flask import request
from flask import abort
from flask_cors import CORS

from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload

from model import model
from . import mocks

# app is the main controller for the Flask-Server and will start the app in the main function 
app = Flask(__name__, template_folder=None)

# NOTE that the following line opnes ALL endpoints for cross-origin requests!
# This has to be tied to the actual public frontend domain as soon as a
# serious authentication system is implemented. See docs of flask_cors
CORS(app)

# used similar to a context manager. using the constructor creates a scoped session, bound to its creating function scope 
Scoped_Session = model.Scoped_Session


# Receive JSON via POST in flask: https://sentry.io/answers/flask-getting-post-data/#json-data
# Parameterized route etc.: https://pythonbasics.org/flask-tutorial-routes/
# Route syntax doc: https://flask.palletsprojects.com/en/2.2.x/api/#url-route-registrations
# Multiple Joins: https://docs.sqlalchemy.org/en/14/orm/queryguide.html#chaining-multiple-joins

@app.route('/report', methods=['POST'])
def get_report():
    """
    
    """
    filter_dict = request.json
    data = mocks.generic_get_data(_filter=filter_dict)
    return data


@app.route('/healthcheck')
def healthcheck():
    return "healthy"


@app.route('/competition_category/', methods=['GET', 'POST'])
def get_competition_categories():
    """
    todo: comment
    """
    result = []

    session = Scoped_Session()
    iterator = session.execute(select(model.Competition_Category)).scalars()
    for entity in iterator:
        mapped = {"id": entity.id, "display_name": entity.name}
        result.append(mapped)

    return result


@app.route('/competition/<int:year>/<int:competition_category_id>')
def get_competitions_year_category(year: int, competition_category_id: int) -> dict:
    """
    WHEN?
    This endpoint is used, when the user is on the page for the 'Rennstrukturanalyse' and selected filter for
        - year
        - competition_category
    of interest.
    @param filter_dict: example for filter_dict {  "year": 2008, "competition_category_id": 5  }
    @return: nested dict/json: structure containing competitions, their events and their races respectively.
    See https://github.com/N10100010/DRV_project/blob/api-design/doc/backend-api.md#user-auswahl-jahr-einzeln-und-wettkampfklasse-zb-olympics for mock of return value.

    """
    from datetime import datetime
    session = Scoped_Session()
    result = {}
    statement = (
        select(
            model.Competition.id,
            model.Competition.start_date,
            model.Competition.name,
            model.Competition.venue
        ).where(
            model.Competition_Category == int(competition_category_id)
            and datetime(model.Competition.start_date).year == year
        ).options(
            joinedload(
                model.Competition.events
            ).joinedload(model.Event.races)
        )
    )
    competitions = session.execute(statement)
    return result


@app.route('/race/<int:race_id>/', methods=['GET'])
def get_race(race_id: int) -> dict:
    """
    WHEN? THIS FUNCTION IS CALLED WHEN THE USER SELECTED A RACE 
    Gets the mandatory information to display a race-analysis (Rennstrukturanalyse).
    @race_id: the internal, unique id identifying a race. 
    @return: the information of a race
    """
    session = Scoped_Session()

    # Join relationship fields using "Joined Load" to fetch all-in-one:
    #   https://docs.sqlalchemy.org/en/14/orm/tutorial.html#joined-load
    #   https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#sqlalchemy.orm.joinedload
    statement = (
        select(model.Race)
        .where(model.Race.id == int(race_id))
        .options(
            joinedload(model.Race.race_boats)
            .joinedload(model.Race_Boat.intermediates),
            joinedload(model.Race.event)
            .options(
                joinedload(model.Event.boat_class),
                joinedload(model.Event.competition)
                .joinedload(model.Competition.venue)
                .joinedload(model.Venue.country)
            )
        )
    )

    competitions = session.execute(statement)
    print()
    # TODO: fill remaining fields (api-design.md)

    race = session.execute(statement).scalars().first()
    if race == None:
        abort(404)

    venue = race.event.competition.venue

    result = {
        "raceId": race.id,
        "displayName": race.name,
        "startDate": str(race.date),
        "venue": f"{venue.site}/{venue.city}, {venue.country.name}",
        "boatClass": race.event.boat_class.abbreviation,  # TODO: currrently only abbrev.
        "worldBestTimeBoatClass": "############## TODO ##############",  # fmt: "00:05:58,36"
        "bestTimeBoatClassCurrentOZ": "############## TODO ##############",  # fmt: "00:05:58,36"
        "pdf_urls": {
            "result": race.pdf_url_results,
            "race_data": race.pdf_url_race_data
        }
    }

    return result


@app.teardown_appcontext
def shutdown_session(exception=None):
    ''' Enable Flask to automatically remove database sessions at the
    end of the request or when the application shuts down.
    Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
    Ref: https://stackoverflow.com/a/45719168
    '''
    Scoped_Session.remove()


# @app.route('/result', 'POST')
# def get_result(filter_dict: dict):
#     """

#     """
#     data = mocks.generic_get_data(_filter=filter_dict)
#     return data


# @app.route('/analysis', 'POST')
# def get_analysis(filter_dict: dict) -> Union[list, dict]:
#     """
#     When?
#     This endpoint is used, when the user is on the page for the 'Rennstrukturanalyse' and selected filter for
#         - year
#         - competition_category
#     of interest.
#     @param filter_dict: example for filter_dict {  "year": 2008, "competition_category_id": 5  }
#     @return: nested dict/json: structure containing competitions, their events and their races respectively.
# See https://github.com/N10100010/DRV_project/blob/api-design/doc/backend-api.md#user-auswahl-jahr-einzeln-und-wettkampfklasse-zb-olympics for mock of return value.
#     """
#     # data = generic_get_data(_filter=filter_dict)
#     data = mocks.mock_standard_analysis_endpoint()
#     return data


# @app.route('/analysis/<race_id>', 'GET')
# def get_race_analysis(race_id: str):
#     race_id = "bcda473e-f602-4747-a61e-a35963bd7198"
#     # data = generic_get_data(_filter={'id': race_id})
#     data = mocks.mock_race_analysis_endpoint()
#     return data


# @app.route('/get_report_filter_options', 'GET')
# def get_report_filter_options(filter_dict: dict):
#     """
#     todo:
#     """
#     return {}


@app.route('/get_report_boat_class', methods=['POST'])
def get_report_boat_class():
    """
    Delivers the report results for a single boat class.
    """
    # extract data from filter | ignored for now: runs, runs_fine and ranks
    filter_data = request.json["data"]
    filter_keys = ["years", "competition_categories", "boat_classes"]
    years, competition_categories, boat_class = [filter_data.get(key) for key in filter_keys]
    start_year = years.get("start_year")
    end_year = years.get("end_year")

    # read from db
    session = Scoped_Session()
    start_date = func.to_timestamp(func.concat(start_year, "-01-01 00:00:00"), 'YYYY-MM-DD HH24:MI:SS')
    end_date = func.to_timestamp(func.concat(end_year, "-12-31 23:59:59"), 'YYYY-MM-DD HH24:MI:SS')

    statement = (
        select([model.Race, model.Boat_Class])
        .where(and_(
            model.Race.date >= start_date,
            model.Race.date <= end_date,
            model.Event.boat_class_id == model.Boat_Class.id,
            model.Boat_Class.additional_id_ == boat_class,
        ))
        .join(model.Event, model.Race.event_id == model.Event.id)
    )

    races = session.execute(statement).fetchall()
    boat_class_name = races[0][1].abbreviation if races else None

    race_times, race_dates = [], []
    for race in races:
        for race_boat in race[0].race_boats:
            if race_boat.result_time_ms and race[0].date:
                race_times.append(race_boat.result_time_ms)
                date = race[0].date
                race_dates.append(
                    '{:02d}'.format(date.year) + '-{:02d}'.format(date.month) + '-{:02d}'.format(date.day))

    results, mean_speed, mean_time, stdev_race_time, median_race_time = 0, 0, 0, 0, 0
    if race_times:
        results = len(race_times)
        # TODO: Set race length dynamically
        race_distance = 2000
        mean_speed = round(mean([race_distance / (time / 1000) for time in race_times]), 2)
        mean_time = int(mean(race_times))
        stdev_race_time = int(stdev(race_times))
        median_race_time = int(median(race_times))

    # edges, hist = np.histogram(race_times, bins=100)

    return json.dumps({
        "results": results,
        "boat_classes": boat_class_name,
        "start_date": start_year,
        "end_date": end_year,
        "world_best_time_boat_class": None,  # TODO: int
        "best_in_period": None,  # TODO: int
        "mean": {
            "mm:ss,00": mean_time,
            "m/s": mean_speed,
            "pace 500m": None,  # TODO: int
            "pace 1000m": None  # TODO: int
        },
        "std_dev": stdev_race_time,
        "median": median_race_time,
        "gradation_fastest": {
            "results": None,
            "time": None
        },
        "gradation_medium": {
            "results": None,
            "time": None
        },
        "gradation_slow": {
            "results": None,
            "time": None
        },
        "gradation_slowest": {
            "results": None,
            "time": None
        },
        "plot_data": {
            "histogram": {
                "labels": [],
                "data": [],
            },
            "scatter_plot": {
                "labels": race_dates,
                "data": race_times
            },
            "scatter_percentile_75": {
                "labels": [
                    f'{start_year}-01-01', f'{end_year}-12-31'
                ],
                "data": [
                    388360, 388360
                ]
            },
            "scatter_percentile_25": {
                "labels": [
                    f'{start_year}-01-01', f'{end_year}-12-31'
                ],
                "data": [
                    380360, 380360
                ]
            }
        }
    })


@app.route('/get_athlete/<int:athlete_id>', methods=['GET'])
def get_athlete(athlete_id: int):
    """
    Give athlete data for specific athlete
    """
    session = Scoped_Session()
    athlete = session.query(model.Athlete).filter(model.Athlete.id == athlete_id).one()

    return json.dumps({
        "id": athlete.id,
        "name": f"{athlete.last_name__}, {athlete.first_name__}",
        "nation": None,
        "dob": str(athlete.birthdate),
        "gender": None,
        "weight": athlete.weight_kg__,
        "height": athlete.height_cm__
    })


@app.route('/get_athlete_by_name/<search_query>', methods=['GET'])
def get_athlete_by_name(search_query: str):
    """
    Delivers the athlete search result depending on the search query.
    @Params: search_query string (currently only first name)
    # TODO: Convert to post request and include filter params from frontend
    """
    session = Scoped_Session()
    athletes = session.execute(select(
        model.Athlete.first_name__,
        model.Athlete.last_name__,
        model.Athlete.id,
        model.Athlete.birthdate
    ).where(or_(
        model.Athlete.last_name__ == search_query.upper(),
        model.Athlete.first_name__ == search_query
    )))

    return json.dumps([{
        "name": f"{athlete.last_name__}, {athlete.first_name__} ({athlete.birthdate})",
        "id": athlete.id
    } for athlete in athletes])


"""
ENDPOINTS TO GET FILTER SELECTION OPTIONS

"""


@app.route('/get_athletes_filter_options', methods=['GET'])
def get_athletes_filter_options():
    """
    Delivers the filter options for the athletes page.
    """
    session = Scoped_Session()
    iterator = session.execute(select(model.Athlete)).scalars()
    birth_years = [entity.birthdate.year for entity in iterator]

    return json.dumps([{
        "birth_years": [
            {"start_year": min(birth_years)},
            {"end_year": max(birth_years)}],
        "nations": {entity.country_code: entity.name for entity in
                    session.execute(select(model.Country)).scalars()},
        # TODO: insert global variable for boat class
        "boat_classes": {
            "men": {
                "u19": {
                    "single": {"JM1x": "Junior Men's Single Sculls"},
                    "double": {"JM2x": "Junior Men's Double Sculls"},
                    "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                    "pair": {"JM2-": "Junior Men's Pair"},
                    "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                    "four": {"JM4-": "Junior Men's Four"},
                    "eight": {"JM8-": "Junior Men's Eight"}
                },
                "u23": {
                    "single": {"BM1x": "U23 Men's Single Sculls"},
                    "double": {"BM2x": "U23 Men's Double Sculls"},
                    "quad": {"BM4x": "U23 Men's Quadruple Sculls"},
                    "pair": {"BM2-": "U23 Men's Pair"},
                    "coxed_four": {"BM4+": "U23 Men's Coxed Four"},
                    "four": {"BM4-": "U23 Men's Four"},
                    "eight": {"BM8+": "U23 Men's Eight"},
                    "lw_single": {"BLM1x": "U23 Lightweight Men's Single Sculls"},
                    "lw_double": {"BLM2x": "U23 Lightweight Men's Double Sculls"},
                    "lw_quad": {"BLM4x": "U23 Lightweight Men's Quadruple Sculls"},
                    "lw_pair": {"BLM2-": "U23 Lightweight Men's Pair"},
                },
                "elite": {
                    "single": {"M1x": "Men's Single Sculls"},
                    "double": {"M2x": "Men's Double Sculls"},
                    "quad": {"M4x": "Men's Quadruple Sculls"},
                    "pair": {"M2-": "Men's Pair"},
                    "four": {"M4-": "Men's Four"},
                    "eight": {"M8+": "Men's Eight"},
                    "lw_single": {"LM1x": "Lightweight Men's Single Sculls"},
                    "lw_double": {"LM2x": "Lightweight Men's Double Sculls"},
                    "lw_quad": {"LM4x": "Lightweight Men's Quadruple Sculls"},
                    "lw_pair": {"LM2-": "Lightweight Men's Pair"},
                },
                "para": {
                    "1": {"PR1 M1x": "PR1 Men's Single Sculls"},
                    "2": {"PR2 M1x": "PR2 Men's Single Sculls"},
                    "3": {"PR3 M2-": "PR3 Men's Pair"}
                }
            },
            "women": {
                "u19": {
                    "single": {"JW1x": "Junior Women's Single Sculls"},
                    "double": {"JW2x": "Junior Women's Double Sculls"},
                    "quad": {"JW4x": "Junior Women's Quadruple Sculls"},
                    "pair": {"JW2-": "Junior Women's Pair"},
                    "coxed_four": {"JW4+": "Junior Women's Coxed Four"},
                    "four": {"JW4-": "Junior Women's Four"},
                    "eight": {"JW8-": "Junior Women's Eight"}
                },
                "u23": {
                    "single": {"BW1x": "U23 Women's Single Sculls"},
                    "double": {"BW2x": "U23 Women's Double Sculls"},
                    "quad": {"BW4x": "U23 Women's Quadruple Sculls"},
                    "pair": {"BW2-": "U23 Women's Pair"},
                    "coxed_four": {"BW4+": "U23 Women's Coxed Four"},
                    "four": {"BW4-": "U23 Women's Four"},
                    "eight": {"BW8+": "U23 Women's Eight"},
                    "lw_single": {"BLW1x": "U23 Lightweight Women's Single Sculls"},
                    "lw_double": {"BLW2x": "U23 Lightweight Women's Double Sculls"},
                    "lw_quad": {"BLW4x": "U23 Lightweight Women's Quadruple Sculls"},
                    "lw_pair": {"BLW2-": "U23 Lightweight Women's Pair"},
                },
                "elite": {
                    "single": {"W1x": "Women's Single Sculls"},
                    "double": {"W2x": "Women's Double Sculls"},
                    "quad": {"W4x": "Women's Quadruple Sculls"},
                    "pair": {"W2-": "Women's Pair"},
                    "four": {"W4-": "Women's Four"},
                    "eight": {"W8+": "Women's Eight"},
                    "lw_single": {"LW1x": "Lightweight Women's Single Sculls"},
                    "lw_double": {"LW2x": "Lightweight Women's Double Sculls"},
                    "lw_quad": {"LW4x": "Lightweight Women's Quadruple Sculls"},
                    "lw_pair": {"LW2-": "Lightweight Women's Pair"},
                },
                "para": {
                    "1": {"PR1 W1x": "PR1 Women's Single Sculls"},
                    "2": {"PR2 W1x": "PR2 Women's Single Sculls"},
                    "3": {"PR3 W2-": "PR3 Women's Pair"}
                }
            },
            "mixed": {
                "double_2": {"PR2 Mix2x": "PR2 Mixed Double Sculls"},
                "double_3": {"PR3 Mix2x": "PR3 Mixed Double Sculls"},
                "four": {"PR3 Mix4+": "PR3 Mixed Coxed Four"},
            },
            "all": {
                "all": {"Alle": "Alle"}
            },
        }
    }], sort_keys=False)


@app.route('/get_teams_filter_options', methods=['GET'])
def get_teams_filter_options():
    """
        Delivers the filter options for the teams page.
        """
    session = Scoped_Session()
    min_year, max_year = session.query(func.min(model.Competition.year), func.max(model.Competition.year)).first()

    return json.dumps([{
        "years": [{"start_year": min_year}, {"end_year": max_year}],
        "competition_categories": [{"id": entity.id, "display_name": entity.name} for entity in
                                   session.execute(select(model.Competition_Category)).scalars()],
        "nations": {entity.country_code: entity.name for entity in
                    session.execute(select(model.Country)).scalars()}
    }], sort_keys=False)


@app.route('/get_medals_filter_options', methods=['GET'])
def get_medals_filter_options():
    """
    Delivers the filter options for the medals page.
    """
    session = Scoped_Session()
    min_year, max_year = session.query(func.min(model.Competition.year), func.max(model.Competition.year)).first()

    return json.dumps([{
        "years": [{"start_year": min_year}, {"end_year": max_year}],
        "competition_categories": [{"id": entity.id, "display_name": entity.name} for entity in
                                   session.execute(select(model.Competition_Category)).scalars()],
        "medal_types": [
            {"display_name": "Gesamt", "id": "0"},
            {"display_name": "Olympisch", "id": "1"},
            {"display_name": "Nicht-Olympisch", "id": "2"}
        ],
        "nations": {entity.country_code: entity.name for entity in
                    session.execute(select(model.Country)).scalars()},
        "boat_classes": {  # TODO: insert global variable here
            "men": {
                "u19": {
                    "single": {"JM1x": "Junior Men's Single Sculls"},
                    "double": {"JM2x": "Junior Men's Double Sculls"},
                    "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                    "pair": {"JM2-": "Junior Men's Pair"},
                    "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                    "four": {"JM4-": "Junior Men's Four"},
                    "eight": {"JM8-": "Junior Men's Eight"}
                },
                "u23": {
                    "single": {"BM1x": "U23 Men's Single Sculls"},
                    "double": {"BM2x": "U23 Men's Double Sculls"},
                    "quad": {"BM4x": "U23 Men's Quadruple Sculls"},
                    "pair": {"BM2-": "U23 Men's Pair"},
                    "coxed_four": {"BM4+": "U23 Men's Coxed Four"},
                    "four": {"BM4-": "U23 Men's Four"},
                    "eight": {"BM8+": "U23 Men's Eight"},
                    "lw_single": {"BLM1x": "U23 Lightweight Men's Single Sculls"},
                    "lw_double": {"BLM2x": "U23 Lightweight Men's Double Sculls"},
                    "lw_quad": {"BLM4x": "U23 Lightweight Men's Quadruple Sculls"},
                    "lw_pair": {"BLM2-": "U23 Lightweight Men's Pair"},
                },
                "elite": {
                    "single": {"M1x": "Men's Single Sculls"},
                    "double": {"M2x": "Men's Double Sculls"},
                    "quad": {"M4x": "Men's Quadruple Sculls"},
                    "pair": {"M2-": "Men's Pair"},
                    "four": {"M4-": "Men's Four"},
                    "eight": {"M8+": "Men's Eight"},
                    "lw_single": {"LM1x": "Lightweight Men's Single Sculls"},
                    "lw_double": {"LM2x": "Lightweight Men's Double Sculls"},
                    "lw_quad": {"LM4x": "Lightweight Men's Quadruple Sculls"},
                    "lw_pair": {"LM2-": "Lightweight Men's Pair"},
                },
                "para": {
                    "1": {"PR1 M1x": "PR1 Men's Single Sculls"},
                    "2": {"PR2 M1x": "PR2 Men's Single Sculls"},
                    "3": {"PR3 M2-": "PR3 Men's Pair"}
                }
            },
            "women": {
                "u19": {
                    "single": {"JW1x": "Junior Women's Single Sculls"},
                    "double": {"JW2x": "Junior Women's Double Sculls"},
                    "quad": {"JW4x": "Junior Women's Quadruple Sculls"},
                    "pair": {"JW2-": "Junior Women's Pair"},
                    "coxed_four": {"JW4+": "Junior Women's Coxed Four"},
                    "four": {"JW4-": "Junior Women's Four"},
                    "eight": {"JW8-": "Junior Women's Eight"}
                },
                "u23": {
                    "single": {"BW1x": "U23 Women's Single Sculls"},
                    "double": {"BW2x": "U23 Women's Double Sculls"},
                    "quad": {"BW4x": "U23 Women's Quadruple Sculls"},
                    "pair": {"BW2-": "U23 Women's Pair"},
                    "coxed_four": {"BW4+": "U23 Women's Coxed Four"},
                    "four": {"BW4-": "U23 Women's Four"},
                    "eight": {"BW8+": "U23 Women's Eight"},
                    "lw_single": {"BLW1x": "U23 Lightweight Women's Single Sculls"},
                    "lw_double": {"BLW2x": "U23 Lightweight Women's Double Sculls"},
                    "lw_quad": {"BLW4x": "U23 Lightweight Women's Quadruple Sculls"},
                    "lw_pair": {"BLW2-": "U23 Lightweight Women's Pair"},
                },
                "elite": {
                    "single": {"W1x": "Women's Single Sculls"},
                    "double": {"W2x": "Women's Double Sculls"},
                    "quad": {"W4x": "Women's Quadruple Sculls"},
                    "pair": {"W2-": "Women's Pair"},
                    "four": {"W4-": "Women's Four"},
                    "eight": {"W8+": "Women's Eight"},
                    "lw_single": {"LW1x": "Lightweight Women's Single Sculls"},
                    "lw_double": {"LW2x": "Lightweight Women's Double Sculls"},
                    "lw_quad": {"LW4x": "Lightweight Women's Quadruple Sculls"},
                    "lw_pair": {"LW2-": "Lightweight Women's Pair"},
                },
                "para": {
                    "1": {"PR1 W1x": "PR1 Women's Single Sculls"},
                    "2": {"PR2 W1x": "PR2 Women's Single Sculls"},
                    "3": {"PR3 W2-": "PR3 Women's Pair"}
                }
            },
            "mixed": {
                "double_2": {"PR2 Mix2x": "PR2 Mixed Double Sculls"},
                "double_3": {"PR3 Mix2x": "PR3 Mixed Double Sculls"},
                "four": {"PR3 Mix4+": "PR3 Mixed Coxed Four"},
            },
            "all": {
                "all": {"Alle": "Alle"}
            },
        }
    }], sort_keys=False)


@app.route('/get_report_filter_options', methods=['GET'])
def get_report_filter_options():
    """
    Delivers the filter options for the report page.
    # TODO: Which parts will stay hardcoded and which will be read from the db?
    """
    session = Scoped_Session()
    min_year, max_year = session.query(func.min(model.Competition.year), func.max(model.Competition.year)).first()
    competition_categories = [{"id": entity.id, "display_name": entity.name} for entity in
                              session.execute(select(model.Competition_Category)).scalars()]
    # note: preserving the order of the key's important for rendering in the frontend
    return json.dumps([{
        "years": [{"start_year": min_year}, {"end_year": max_year}],
        "boat_classes": {
            'men': {
                'u19': {
                    'single': ("JM1x", "Junior Men's Single Sculls", "079e71bb-98cd-47f4-8ca4-e3fd0cdbc538"),
                    'double': ("JM2x", "Junior Men's Double Sculls", "78f004f6-cadd-4d0f-804b-21cf26458355"),
                    'quad': ("JM4x", "Junior Men's Quadruple Sculls", "dc9439cd-36d9-47fd-a205-bc2612f4f83b"),
                    'pair': ("JM2-", "Junior Men's Pair", "5851b9f9-5240-4fea-a19e-43b24eb99a10"),
                    'coxed_four': ("JM4+", "Junior Men's Coxed Four", "1797cb82-0ced-4fb3-9acd-4a6646f824cb"),
                    'four': ("JM4-", "Junior Men's Four", "8661c474-9506-473a-9784-d00ecfa2167f"),
                    'eight': ("JM8+", "Junior Men's Eight", "bed56642-164b-4ea5-93ce-1fcadd0ef017")
                },
                'u23': {
                    'single': ("BM1x", "U23 Men's Single Sculls", "6b7c0445-c065-49cd-90b3-4c56317e4346"),
                    'double': ("BM2x", "U23 Men's Double Sculls", "74864b35-be40-431a-a48c-f1b605a6759e"),
                    'quad': ("BM4x", "U23 Men's Quadruple Sculls", "be5a6d89-d55b-4316-9366-7ed1ef0f307b"),
                    'pair': ("BM2-", "U23 Men's Pair", "3830f652-0963-4d75-a081-a4ef4553a10c"),
                    'coxed_four': ("BM4+", "U23 Men's Coxed Four", "e784fbb3-b45f-45d5-be67-0699cdba4553"),
                    'four': ("BM4-", "U23 Men's Four", "2fc7bcd7-3ccc-49eb-ab18-50ab09ae501d"),
                    'eight': ("BM8+", "U23 Men's Eight", "2a2a5aa7-8592-4684-99ce-4f02679061e6"),
                    'lw_single': (
                        "BLM1x", "U23 Lightweight Men's Single Sculls", "2a2a5aa7-8592-4684-99ce-4f02679061e6"),
                    'lw_double': (
                        "BLM2x", "U23 Lightweight Men's Double Sculls", "cc8022e2-3ee1-463a-bddf-aa115d68e704"),
                    'lw_quad': (
                        "BLM4x", "U23 Lightweight Men's Quadruple Sculls", "8df04fba-76af-40c4-ac38-73f377bfb258"),
                    'lw_pair': ("BLM2-", "U23 Lightweight Men's Pair", "3830f652-0963-4d75-a081-a4ef4553a10c"),
                },
                'elite': {
                    'single': ("M1x", "Men's Single Sculls", "3f0d0a7d-92a6-4c53-90f5-7c8f01972964"),
                    'double': ("M2x", "Men's Double Sculls", "9cb5d841-32a6-4388-8a30-6d7f51bdfdbc"),
                    'quad': ("M4x", "Men's Quadruple Sculls", "d4140064-67dc-47d0-957a-a42e90bf8433"),
                    'pair': ("M2-", "Men's Pair", "02316e75-fdf2-4660-af40-48dda1867e1f"),
                    'four': ("M4-", "Men's Four", "27d5614e-6530-49d1-acf5-da132b71a45d"),
                    'eight': ("M8+", "Men's Eight", "532b264c-47e1-4d35-928a-85d9733928d0"),
                    'lw_single': ("LM1x", "Lightweight Men's Single Sculls", "182d0aae-7e73-4900-ae8e-f1aafbe5c48a"),
                    'lw_double': ("LM2x", "Lightweight Men's Double Sculls", "4458faa3-d55b-495f-8018-51250f82e5ba"),
                    'lw_quad': ("LM4x", "Lightweight Men's Quadruple Sculls", "ba397032-a5c6-466a-ba1b-23e521237048"),
                    'lw_pair': ("LM2-", "Lightweight Men's Pair", "46564a8c-b4b3-4bb3-bbf4-cd96bb4ee4f5"),
                },
                'para': {
                    '1': ("PR1 M1x", "PR1 Men's Single Sculls", "d7365b40-b544-480b-aa99-b0ffad7a13e9"),
                    '2': ("PR2 M1x", "PR2 Men's Single Sculls", "731e3206-45c5-4596-b48e-5a21b1675918"),
                    '3': ("PR3 M2-", "PR3 Men's Pair", "15e1ef74-79c6-4227-96f1-86d793efbf5b"),
                }
            },
            'women': {
                'u19': {
                    'single': ("JW1x", "Junior Women's Single Sculls", "683b227a-51fd-4c09-a6a0-460ca3711b08"),
                    'double': ("JW2x", "Junior Women's Double Sculls", "26af8860-5146-422d-bb10-3eef8b28d883"),
                    'quad': ("JW4x", "Junior Women's Quadruple Sculls", "6edc9d42-edda-4f32-9469-91d54e0eaeb1"),
                    'pair': ("JW2-", "Junior Women's Pair", "4bbcf35e-b424-4000-9f4f-048f2edce263"),
                    'coxed_four': ("JW4+", "Junior Women's Coxed Four", "5911da97-fe4a-42ce-8431-7f3aa9cdfb20"),
                    'four': ("JW4-", "Junior Women's Four", "ff2aa19c-db81-4c8e-a523-b7a3ef50ce31"),
                    'eight': ("JW8+", "Junior Women's Eight", "d97e6295-e55a-4235-abc3-e986dead5137"),
                },
                'u23': {
                    'single': ("BW1x", "U23 Women's Single Sculls", "e22e0fe4-66bc-42f1-82f4-162bb1cc384b"),
                    'double': ("BW2x", "U23 Women's Double Sculls", "5a308214-114a-4b49-b985-fdc6e0b7b319"),
                    'quad': ("BW4x", "U23 Women's Quadruple Sculls", "ba9814b9-0243-445c-979d-189da9ad8407"),
                    'pair': ("BW2-", "U23 Women's Pair", "3304a580-b3b1-4b4e-b51f-e4f63d2e5853"),
                    'coxed_four': ("BW4+", "U23 Women's Coxed Four", "e972ad8f-b73e-41ef-a30b-dee4a391a734"),
                    'four': ("BW4-", "U23 Women's Four", "c5810370-41ac-45c2-aeff-01dcb1d6d078"),
                    'eight': ("BW8+", "U23 Women's Eight", "871abbbb-2413-45b5-b83c-03619c6f0ee5"),
                    'lw_single': (
                        "BLW1x", "U23 Lightweight Women's Single Sculls", "60cecbef-919c-47c0-9f16-0a8edd105d82"),
                    'lw_double': (
                        "BLW2x", "U23 Lightweight Women's Double Sculls", "aee5f04d-6939-4173-a829-999dfb77f159"),
                    'lw_quad': (
                        "BLW4x", "U23 Lightweight Women's Quadruple Sculls", "c18403e0-53cf-4b6b-a1f1-60ad2b220c5a"),
                    'lw_pair': ("BLW2-", "U23 Lightweight Women's Pair", "0f218eeb-6f65-48c7-941c-97f0901cb8cd"),
                },
                'elite': {
                    'single': ("W1x", "Women's Single Sculls", "8a078108-6741-4ad1-ab5a-704194538227"),
                    'double': ("W2x", "Women's Double Sculls", "16946db9-72f2-4375-a797-a26fd485dd26"),
                    'quad': ("W4x", "Women's Quadruple Sculls", "7249e207-5c76-4c58-9c7c-b7e2a4c74b50"),
                    'pair': ("W2-", "Women's Pair", "5e834702-14c3-4a85-b38d-9afb419f5294"),
                    'four': ("W4-", "Women's Four", "2b2bfa01-a902-4ad8-be87-4527c9ba7e6d"),
                    'eight': ("W8+", "Women's Eight", "b834436f-4378-4825-aaa0-f9905959abdb"),
                    'lw_single': ("LW1x", "Lightweight Women's Single Sculls", "43b5679c-8f9e-45f9-8111-fca22bdc02cc"),
                    'lw_double': ("LW2x", "Lightweight Women's Double Sculls", "61be8c32-b56d-4cac-bf56-46246fb1c349"),
                    'lw_quad': ("LW4x", "Lightweight Women's Quadruple Sculls", "c47c6b93-dd0d-4645-9545-2ee853db284c"),
                    'lw_pair': ("LW2-", "Lightweight Women's Pair", "7b8c2fd0-0286-4bd3-a5c3-0f17a4bc3bd0"),
                },
                'para': {
                    '1': ("PR1 W1x", "PR1 Women's Single Sculls", "b61f430f-d4ee-48e0-a632-95b9194ccb16"),
                    '2': ("PR2 W1x", "PR2 Women's Single Sculls", "dd434535-b9eb-4b38-9ecf-f3fd6dc9cadf"),
                    '3': ("PR3 W2-", "PR3 Women's Pair", "15e1ef74-79c6-4227-96f1-86d793efbf5b"),
                }
            },
            'mixed': {
                'double_2': ("PR2 Mix2x", "PR2 Mixed Double Sculls", "843310e2-f28c-41a7-90e9-b6f8c289b154"),
                'double_3': ("PR3 Mix2x", "PR3 Mixed Double Sculls", "e23cc24f-4a62-4de3-ab99-50a40c8416f0"),
                'four': ("PR3 Mix4+", "PR3 Mixed Coxed Four", "b6bcf280-a57c-4a6a-96fb-91e6a1355002"),
            },
            "all": {
                "all": ("Alle", "Alle")
            },
        },
        "competition_categories": competition_categories,
        "runs": {
            "final": [
                {"display_name": "fa"},
                {"display_name": "fb"},
                {"display_name": "fc"},
                {"display_name": "fd"},
                {"display_name": "f..."}
            ],
            "semifinal": [
                {"display_name": "sa/b, sa/b/c"},
                {"display_name": "sc/d, sd/e/f"},
                {"display_name": "s..."}
            ],
            "quarterfinal": [
                {"display_name": "q1-4"},
            ],
            "hoffnungslauf": None,  # what is the correct english wording for hoffnungslauf?
            "preliminary": None,
        },
        "ranks": ["1", "2", "3", "4-6"]
    }], sort_keys=False)


@app.route('/calendar/', methods=['GET'])
def get_calendar():
    """
    TODO: If the db is complete there will be many competitions; perhaps we need some kind of pagination here.
    This route delivers calendar data for all competitions.
    @return: key (relevant for frontend), title, dates for competition
    """
    result = []
    session = Scoped_Session()
    iterator = session.execute(select(model.Competition)).scalars()
    for entity in iterator:
        # only include competitions that have a start and end date
        if entity.start_date and entity.end_date:
            result.append({
                "key": entity.id,
                "customData": {
                    "title": entity.name
                },
                "dates": {
                    "start": datetime.datetime.strptime(str(entity.start_date),
                                                        '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y %H:%M:%S GMT'),
                    "end": datetime.datetime.strptime(str(entity.end_date),
                                                      '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y %H:%M:%S GMT')
                }
            })
    return result
