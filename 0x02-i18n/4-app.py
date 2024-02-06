#!/usr/bin/env python3
"""
Task

4. Force locale with URL parameter

In this task, you will implement a way to force a particular locale by passing
the locale=fr parameter to your app’s URLs.

In your get_locale function, detect if the incoming request contains locale
argument and ifs value is a supported locale, return it. If not or if the
parameter is not present, resort to the previous default behavior.

Now you should be able to test different translations by visiting
http://127.0.0.1:5000?locale=[fr|en].
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


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


@babel.localeselector
def get_locale():
    """
    Determines the best locale match for the user with our supported languages
    """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("4-index.html")
