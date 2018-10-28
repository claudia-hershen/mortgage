"""Mortgage Calculatot app."""
from flask import Flask

from blueprints.mortgage_blueprint import mortgage_blueprint
from blueprints.run_wrapper_blueprint import run_wrapper_blueprint

app = Flask(__name__)
# app.secret_key = 'any secret string'

app.register_blueprint(mortgage_blueprint)
app.register_blueprint(run_wrapper_blueprint)


@app.route('/')
def index():
    """Index route."""
    html = "<b>Mortgage Calculator !</b>"
    return html

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
