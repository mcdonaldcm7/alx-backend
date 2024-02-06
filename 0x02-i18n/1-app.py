#!/usr/bin/env python3
"""
Task

1. Basic Basic setup

Then instantiate the Babel object in your app. Store it in a module-level
variable named babel.

In order to configure available languages in our app, you will create a Config
class that has a LANGUAGES class attribute equal to ["en", "fr"].

Use Config to set Babel’s default locale ("en") and timezone ("UTC").

Use that class as config for your Flask app.
"""
from flask import Flask, render_template
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


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("1-index.html")
