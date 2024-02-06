#!/usr/bin/env python3
"""
Task

2. Get locale from request

Create a get_locale function with the babel.localeselector decorator. Use
request.accept_languages to determine the best match with our supported
languages.
"""
from flask import Flask, render_template, g, request
from flask_babel import Babel


class Config:
    """
    Configuration class to keep track of the list of supported languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Determines the best locale match for the user with our supported languages
    """
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("1-index.html")
