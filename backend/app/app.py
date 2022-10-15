from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

BASE_PATH_TEMPLATE = "/app/templates/"


@app.route('/')
def home():
    return render_template("./NO_TEMPLATE.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

