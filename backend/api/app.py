import os
import datetime
import json
from collections import OrderedDict
from statistics import stdev, median, mean

from flask import Flask
from flask import request
from flask import abort
from flask import Response
from flask_cors import CORS

from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload

from model import model
from . import mocks
from common.rowing import propulsion_in_meters_per_stroke

# app is the main controller for the Flask-Server and will start the app in the main function 
app = Flask(__name__, template_folder=None)
app.config['JSON_SORT_KEYS'] = False

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


from flask import request as freq
@app.route('/competition', methods=['GET'])
def get_competitions_year_category() -> dict:
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
    import logging

    year = freq.args.get('year')
    competition_category_id = freq.args.get('competition_category_id')
    

    logging.info(f"Year: {year}, comp cat: {competition_category_id}")

    print(f"Year: {year}, comp cat: {competition_category_id}")

    session = Scoped_Session()

    statement = (
        select(
            model.Race.id, 
            model.Event.id, 
            model.Competition.name
        )
        .join(model.Race.event)
        .join(model.Event.competition)
        .where(
            and_(
            model.Competition.id == 11, 
            model.Competition.year == 2020, 
            )
        )
    )
    

    competitions = session.execute(statement).fetchall()

    def _extract(data: dict, koi: list[str]): 
        ret = {}

        for key in koi: 
            ret[key] = data.get(key, None)
        
        return ret


    result = []
    for comp in competitions: 
        comp = comp['Competition']
        comp_res = _extract(comp.__dict__, ["id", "name", "start_date"])

        comp_events = []

        for event in comp.events: 
            event_res = _extract(event.__dict__, ["id", "name",])

            event_races = []

            for race in event.races: 
                race_res = _extract(race.__dict__, ["id", "name"])

                event_races.append(race_res)
            
            event_res['races'] = event_races
            comp_events.append(event_res)

        comp_res['events'] = event_res
        result.append(comp_res)
                

    result = []
    for comp in competitions: 
        comp = comp['Competition']
        comp_res = _extract(comp.__dict__, ["id", "name", "venue", "start_date"])
        comp_events = []
        for event in comp.events: 
            event_res = _extract(event.__dict__, ["id", "name",])
            event_races = []
            for race in event.races: 
                race_res = _extract(race.__dict__, ["id", "name"])
                event_races.append(race_res)
                print()

            event_res['races'] = event_races

        comp_res['events'] = comp_events

        result.append(comp_res)

    
    return result


@app.route('/get_race/<int:race_id>/', methods=['GET'])
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

    race: model.Race
    race = session.execute(statement).scalars().first()
    if race == None:
        abort(404)

    venue = race.event.competition.venue

    world_best_race_boat = race.event.boat_class.world_best_race_boat
    world_best_time_ms = None
    if world_best_race_boat:
        world_best_time_ms = world_best_race_boat.result_time_ms

    result = {
        "race_id": race.id,
        "display_name": race.name,
        "start_date": str(race.date),
        "venue": f"{venue.site}/{venue.city}, {venue.country.name}",
        "boat_class": race.event.boat_class.abbreviation,  # long name?
        "result_time_world_best": world_best_time_ms,
        "result_time_best_of_current_olympia_cycle": "############## TODO ##############",  # int in ms
        "progression_code": race.progression,
        "pdf_urls": {
            "result": race.pdf_url_results,
            "race_data": race.pdf_url_race_data
        },
        "race_boats": []
    }

    race_boat: model.Race_Boat
    for race_boat in race.race_boats:
        rb_result = {
            "name": race_boat.name, # e.g. DEU2
            "lane": race_boat.lane,
            "rank": race_boat.rank,
            "athletes": [],
            "intermediates": OrderedDict(),
            "race_data": OrderedDict()
        }
        result['race_boats'].append(rb_result)

        # athletes
        athlete_assoc: model.Association_Race_Boat_Athlete
        for athlete_assoc in race_boat.athletes:
            athlete: model.Athlete = athlete_assoc.athlete
            rb_result['athletes'].append({
                "id": athlete.id,
                "first_name": athlete.first_name__,
                "last_name": athlete.last_name__,
                "full_name": athlete.name,
                "boat_position": athlete_assoc.boat_position
            })

        # race_data aka gps data
        race_data: model.Race_Data
        for race_data in race_boat.race_data:
            propulsion = propulsion_in_meters_per_stroke(race_data.stroke, race_data.speed_meter_per_sec)
            rb_result['race_data'][str(race_data.distance_meter)] = {
                "speed [m/s]": race_data.speed_meter_per_sec,
                "stroke [1/min]": race_data.stroke,
                "propulsion [m/stroke]": propulsion
            }

        # intermediates
        intermediate: model.Intermediate_Time
        for intermediate in race_boat.intermediates:
            result_time_ms = intermediate.result_time_ms
            if intermediate.is_outlier:
                continue
            if intermediate.invalid_mark_result_code:
                result_time_ms = intermediate.invalid_mark_result_code.id
            
            rb_result['intermediates'][str(intermediate.distance_meter)] = {
                "time [t]": result_time_ms
            }
            # relative difference to average time at this mark

    return Response(json.dumps(result, sort_keys=False), content_type='application/json')


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
    Filter conditions are sent via request body:
    {
        "years": {"start_year": 2019, "end_year": 2024},
        "competition_categories": [1, 2, 4, 6, 10, 12, 3, 11, 8, 5, 9, 7, 13],
        "boat_classes": "JW1x",
        "runs": [0, 1, 2],
        "runs_fine": ["fa", "fb", "fc", "fd", "f...", "sa/b, sa/b/c", "sc/d, sd/e/f", "s...", "q1-4"],
        "ranks": ["1", "2", "3", "4-6"]
    }
    """
    # extract data from filter | ignored for now: runs, runs_fine and ranks
    filter_data = request.json["data"]
    filter_keys = ["years", "competition_categories", "boat_classes"]
    years, competition_categories, boat_classes = [filter_data.get(key) for key in filter_keys]
    start_year = years.get("start_year")
    end_year = years.get("end_year")
    # read from db
    session = Scoped_Session()
    start_date = func.to_timestamp(func.concat(start_year, "-01-01 00:00:00"), 'YYYY-MM-DD HH24:MI:SS')
    end_date = func.to_timestamp(func.concat(end_year, "-12-31 23:59:59"), 'YYYY-MM-DD HH24:MI:SS')
    statement = (
        select([model.Race, model.Event])
        .where(and_(
            model.Race.date >= start_date,
            model.Race.date <= end_date,
            model.Event.boat_class_id == int(boat_classes)
        ))
        .join(model.Event, model.Race.event)
    )
    races = session.execute(statement).fetchall()

    boat_class_id = int(set([race[0].event.boat_class_id for race in races for _ in race[0].race_boats]).pop())
    race_times, race_dates = [], []
    for race in races:
        for race_boat in race[0].race_boats:
            if race_boat.result_time_ms and race[0].date:
                race_times.append(race_boat.result_time_ms)
                date = race[0].date
                race_dates.append('{:02d}'.format(date.year)+'-{:02d}'.format(date.month)+'-{:02d}'.format(date.day))

    # TODO: correct calc of mean speed?
    mean_speed = round(mean([2000/(time/1000) for time in race_times]), 4)

    return json.dumps({
        "results": len(race_times),
        "boat_class": boat_class_id,
        "start_date": start_year,
        "end_date": end_year,
        "world_best_time_boat_class": None,  # TODO: int
        "best_in_period": None,  # TODO: int
        "mean": {
            "mm:ss,00": int(mean(race_times)),
            "m/s": mean_speed,
            "pace 500m": None,  # TODO: int
            "pace 1000m": None  # TODO: int
        },
        "std_dev": int(stdev(race_times)),
        "median": median(race_times),
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
                "data": []
            },
            "scatter_plot": {
                "labels": race_dates,
                "data": race_times
            }
        }
    })


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
