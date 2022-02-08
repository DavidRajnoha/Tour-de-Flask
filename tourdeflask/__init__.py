import logging
import os

from flask import Flask

from . import shopping_list, db


def create_app(test_config=None):
    # Vupravit initytvoření app objektu, který tvoří jádro naší aplikace
    # (Pro zajemce: wsgi aplikace)
    app = Flask(__name__, instance_relative_config=True)
    logging.info("Application initialized with instance path: " + app.instance_path)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    logging.info("Application initialized with instance path: " + app.instance_path)

    db.init_app(app)

    # Při zadání 127.0.0.1:5000/ se spustí funkce hello. V tomto kontextu se o ní bavíme jako o view.
    @app.route('/hello')
    def hello():
        return 'Welcome to Tour de Flask!\nThe tour will start on 1st July 2022'

    app.register_blueprint(shopping_list.bp)

    return app
