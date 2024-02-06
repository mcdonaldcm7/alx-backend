#!/usr/bin/env python3
"""
Task

3. Parameterize templates

Use the _ or gettext function to parametrize your templates. Use the message
IDs home_title and home_header.

Create a babel.cfg file containing

    [python: **.py]
    [jinja2: **/templates/**.html]
    extensions=jinja2.ext.autoescape,jinja2.ext.with_

Then initialize your translations with

    $ pybabel extract -F babel.cfg -o messages.pot .

and your two dictionaries with

    $ pybabel init -i messages.pot -d translations -l en
    $ pybabel init -i messages.pot -d translations -l fr

Then edit files translations/[en|fr]/LC_MESSAGES/messages.po to provide the
correct value for each message ID for each language. Use the following
translations:

msgid	    English	                French
home_title	"Welcome to Holberton"	"Bienvenue chez Holberton"
home_header	"Hello world!"	        "Bonjour monde!"

Then compile your dictionaries with

    $ pybabel compile -d translations

Reload the home page of your app and make sure that the correct messages show up.
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
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """
    A simple flask app
    """
    return render_template("3-index.html")
