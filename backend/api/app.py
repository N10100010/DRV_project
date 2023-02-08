import os
import datetime
import json
import collections

from flask import Flask
from flask import request
from flask import abort

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from model import model
from . import mocks

# app is the main controller for the Flask-Server and will start the app in the main function 
app = Flask(__name__, template_folder=None)

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


@app.route('/competition_category/', methods=['GET'])
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


@app.route('/get_athlete_by_name/<search_query>', methods=['GET'])
def get_athlete_by_name(search_query: str):
    """
    Delivers the athlete search result depending on the search query.
    @Params: search_query string (currently only first name)
    """
    session = Scoped_Session()
    athletes = session.execute(select(
        model.Athlete.first_name__,
        model.Athlete.last_name__,
        model.Athlete.id
    ).where(model.Athlete.first_name__ == search_query))

    return json.dumps([{
        "name": str(athlete.first_name__ + " " + athlete.last_name__),
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
        "boat_classes": {
            "men": {
                "junior": {
                    "single": {"JM1x": "Junior Men's Single Sculls"},
                    "double": {"JM2x": "Junior Men's Double Sculls"},
                    "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                    "pair": {"JM2-": "Junior Men's Pair"},
                    "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                    "four": {"JM4-": "Junior Men's Four"},
                    "eight": {"JM8-": "Junior Men's Eight"}
                },
                "u19": {},
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
                "junior": {
                    "single": {"JW1x": "Junior Women's Single Sculls"},
                    "double": {"JW2x": "Junior Women's Double Sculls"},
                    "quad": {"JW4x": "Junior Women's Quadruple Sculls"},
                    "pair": {"JW2-": "Junior Women's Pair"},
                    "coxed_four": {"JW4+": "Junior Women's Coxed Four"},
                    "four": {"JW4-": "Junior Women's Four"},
                    "eight": {"JW8-": "Junior Women's Eight"}
                },
                "u19": {},
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
        "boat_classes": {
            "men": {
                "junior": {
                    "single": {"JM1x": "Junior Men's Single Sculls"},
                    "double": {"JM2x": "Junior Men's Double Sculls"},
                    "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                    "pair": {"JM2-": "Junior Men's Pair"},
                    "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                    "four": {"JM4-": "Junior Men's Four"},
                    "eight": {"JM8-": "Junior Men's Eight"}
                },
                "u19": {},
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
                "junior": {
                    "single": {"JW1x": "Junior Women's Single Sculls"},
                    "double": {"JW2x": "Junior Women's Double Sculls"},
                    "quad": {"JW4x": "Junior Women's Quadruple Sculls"},
                    "pair": {"JW2-": "Junior Women's Pair"},
                    "coxed_four": {"JW4+": "Junior Women's Coxed Four"},
                    "four": {"JW4-": "Junior Women's Four"},
                    "eight": {"JW8-": "Junior Women's Eight"}
                },
                "u19": {},
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
            "men": {
                "junior": {
                    "single": {"JM1x": "Junior Men's Single Sculls"},
                    "double": {"JM2x": "Junior Men's Double Sculls"},
                    "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                    "pair": {"JM2-": "Junior Men's Pair"},
                    "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                    "four": {"JM4-": "Junior Men's Four"},
                    "eight": {"JM8-": "Junior Men's Eight"}
                },
                "u19": {},
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
                "junior": {
                    "single": {"JW1x": "Junior Women's Single Sculls"},
                    "double": {"JW2x": "Junior Women's Double Sculls"},
                    "quad": {"JW4x": "Junior Women's Quadruple Sculls"},
                    "pair": {"JW2-": "Junior Women's Pair"},
                    "coxed_four": {"JW4+": "Junior Women's Coxed Four"},
                    "four": {"JW4-": "Junior Women's Four"},
                    "eight": {"JW8-": "Junior Women's Eight"}
                },
                "u19": {},
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
