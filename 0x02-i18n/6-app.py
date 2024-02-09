#!/usr/bin/env python3
"""
Task

6. User user locale

Change your get_locale function to use a user’s preferred local if it is
supported.

The order of priority should be

    1. Locale from URL parameters
    2. Locale rom user settings
    3. Locale from request header
    4. Default locale

Test by logging in as different users
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

    if g.user is not None:
        user_locale = g.user.get('locale', None)
        if user_locale is not None and user_locale in app.config["LANGUAGES"]:
            return user_locale

    request_header_locale = request.accept_languages.best_match(
            app.config["LANGUAGES"])
    if request_header_locale is not None:
        return request_header_locale

    return app.config["BABEL_DEFAULT_LOCALE"]


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("6-index.html", username=g.user)
