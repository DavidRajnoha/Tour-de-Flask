import os

from flask import Flask

from tourdeflask import db
from . import shopping_list


def create_app(test_config=None):
    # Vytvoření app objektu, který tvoří jádro naší aplikace
    # (Pro zajemce: wsgi aplikace)
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Při zadání 127.0.0.1:5000/ se spustí funkce hello. V tomto kontextu se o ní bavíme jako o view.
    @app.route('/hello')
    def hello():
        return 'Welcome to Tour de Flask!\nThe tour will start on 1st July 2022'

    app.register_blueprint(shopping_list.bp)

    return app
