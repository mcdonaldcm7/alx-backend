#!/usr/bin/env python3
"""
Task

5. Mock logging in

Creating a user login system is outside the scope of this project. To emulate a
similar behavior, copy the following user table in 5-app.py.

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

This will mock a database user table. Logging in will be mocked by passing
login_as URL parameter containing the user ID to log in as.

Define a get_user function that returns a user dictionary or None if the ID
cannot be found or if login_as was not passed.

Define a before_request function and use the app.before_request decorator to
make it be executed before all other functions. before_request should use
get_user to find a user if any, and set it as a global on flask.g.user.

In your HTML template, if a user is logged in, in a paragraph tag, display a
welcome message otherwise display a default message as shown in the table
below.

msgid	        English	                    French
logged_in_as	"You are logged             "Vous êtes connecté en
                in as %(username)s."	    tant que %(username)s."
not_logged_in	"You are not logged in."    "Vous n'êtes pas connecté."
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class to keep track of the list of supported languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.before_request
def before_request():
    """
    Retrieves the user information based on id before each request
    """
    g.user = get_user()


def get_user():
    """
    Fecthes the user details from the mocking database user table
    """
    user_id = request.args.get("login_as")
    if user_id is not None and int(user_id) in users:
        return users.get(int(user_id))
    return None


@babel.localeselector
def get_locale():
    """
    Determines the best locale match for the user with our supported languages
    """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("5-index.html", username=g.user)
