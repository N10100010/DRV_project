from typing import Union
import os

from flask import Flask, render_template
from flask import request
from flask import jsonify

import backend.scraping_wr.api as api
import backend.app.mocks as mocks

app = Flask(__name__, template_folder='web/templates')

@app.route('/')
def home():
    return render_template("./NO_TEMPLATE.html")


@app.route('/report', methods=['POST'])
def get_report():
    # Receive JSON via POST in flask: https://sentry.io/answers/flask-getting-post-data/#json-data
    filter_dict = request.json
    data = mocks.generic_get_data(_filter=filter_dict)
    return data


@app.route('/test')
def test():
    return "This is not a asdtest 123 :)"


# @app.route('/result', 'POST')
# def get_result(filter_dict: dict):
#     """

#     """
#     data = mocks.generic_get_data(_filter=filter_dict)
#     return data


# @app.route('/get_competition_category', 'POST')
# def get_competition_categories():
#     """
#     todo: check, and make sure that the result matches the expected return-value
#     returns somewhat static list of competition categories
#     """
#     return api.get_competition_categories()


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
