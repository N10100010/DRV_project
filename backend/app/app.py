from typing import Union
import os

from flask import Flask, render_template
from flask import request
from flask import jsonify

from sqlalchemy import select

from backend.model import model
import backend.scraping_wr.api as api
import backend.app.mocks as mocks

app = Flask(__name__, template_folder='web/templates')

Scoped_Session = model.Scoped_Session

@app.route('/')
def home():
    return render_template("./NO_TEMPLATE.html")


# Receive JSON via POST in flask: https://sentry.io/answers/flask-getting-post-data/#json-data
@app.route('/report', methods=['POST'])
def get_report():
    filter_dict = request.json
    data = mocks.generic_get_data(_filter=filter_dict)
    return data


@app.route('/test')
def test():
    return "This is not a asdtest 123 :)"


@app.route('/get_competition_category', methods=['GET'])
def get_competition_categories():
    result = []

    session = Scoped_Session()
    entities = session.scalars(select(model.Competition_Category)).all()
    for entity in entities:
        mapped = { "id": entity.id, "display_name": entity.name }
        result.append(mapped)

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
#     See https://github.com/N10100010/DRV_project/blob/api-design/doc/backend-api.md#user-auswahl-jahr-einzeln-und-wettkampfklasse-zb-olympics for mock of return value.
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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    print()
