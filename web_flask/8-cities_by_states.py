#!/usr/bin/python3
"""
Flask web application that displays a list of all States and their Cities.

Route:
    /cities_by_states: Displays all states and their linked cities
    listed in alphabetical order using a Jinja2 template.

The application connects to a storage engine and ensures the session
is closed after each request using the teardown function.
"""

from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Handles the route '/cities_by_states'.

    Retrieves all State objects from the storage engine and renders
    them along with their linked City objects in a Jinja2 template.
    """
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Handles application context teardown.

    This function is automatically called after each request to
    remove the current SQLAlchemy session and avoid memory leaks.
    """
    storage.close()


if __name__ == '__main__':
    # Starts the Flask application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
