import os

from flask import Flask
from flask import request
from flask import abort

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from model import model


# app is the main controller for the Flask-Server and will start the app in the main function 
app = Flask(__name__, template_folder='web/templates')

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
        mapped = { "id": entity.id, "display_name": entity.name }
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
        "boatClass": race.event.boat_class.abbreviation, # TODO: currrently only abbrev.
        "worldBestTimeBoatClass": "############## TODO ##############", # fmt: "00:05:58,36"
        "bestTimeBoatClassCurrentOZ": "############## TODO ##############", # fmt: "00:05:58,36"
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
     #See https://github.com/N10100010/DRV_project/blob/api-design/doc/backend-api.md#user-auswahl-jahr-einzeln-und-wettkampfklasse-zb-olympics for mock of return value.
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


# TODO: Remove the following lines or move app.py to parent folder (/backend)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    print()
