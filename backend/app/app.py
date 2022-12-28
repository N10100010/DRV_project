from typing import Union

from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='web/templates')

BASE_PATH_TEMPLATE = "/app/templates/"


@app.route('/')
def home():
    return render_template("./NO_TEMPLATE.html")


@app.route('/report', 'POST')
def get_report(filter_dict: dict):
    """

    """
    data = generic_get_data(_filter=filter_dict)
    return data


@app.route('/result', 'POST')
def get_result(filter_dict: dict):
    """

    """
    data = generic_get_data(_filter=filter_dict)
    return data


@app.route('/competitionCategory', 'GET')
def get_competition_category():
    """
    returs somewhat static list of competition categories
    """
    pass


@app.route('/analysis', 'POST')
def get_analysis(filter_dict: dict):
    """

    """
    data = generic_get_data(_filter=filter_dict)
    return data


@app.route('/analysis/<race_id>', 'GET')
def get_race_analysis(race_id: str):
    return {}


def generic_get_data(_filter: dict) -> dict:
    return {}



if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    print()
