#!/usr/bin/env python3
"""
Task

8. Display the current time

Based on the inferred time zone, display the current time on the home page in
the default format. For example:

Jan 21, 2020, 5:55:39 AM or 21 janv. 2020 à 05:56:28

Use the following translations

msgid	            English             French
current_time_is	"The current time       "Nous sommes le %(current_time)s."
                is %(current_time)s."

"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from datetime import datetime


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


@babel.timezoneselector
def get_timezone():
    """
    """
    timezone = request.args.get("timezone")

    user_timezone = None
    if g.user is not None:
        user_timezone = g.user.get("timezone", None)

    try:
        if timezone is not None:
            pytz.timezone(timezone)
            return timezone
        if user_timezone is not None:
            pytz.timezone(user_timezone)
            return user_timezone
    except pytz.exceptions.UnknownTimeZoneError:
        pass

    return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    user_timezone = get_timezone()
    current_time_utc = datetime.utcnow()

    if user_timezone:
        user_timezone_obj = pytz.timezone(user_timezone)
        current_time = current_time_utc.astimezone(user_timezone_obj)
    return render_template("index.html", username=g.user,
                           current_time=current_time)
