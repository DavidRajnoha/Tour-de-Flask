import logging

import click
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

db = SQLAlchemy()


def init_db():
    db.drop_all()
    db.create_all()


# definujeme příkaz příkazové řádky
@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Smaže aktuální data a vytvoří prázdnou tabulku.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Prováže db s app
    db tím získá přístup ke konfiguracím, které
    se nacházejí v app
    :param app:
    :return:
    """
    db.init_app(app)
    app.cli.add_command(init_db_command)

    if 'PLATFORM' in app.config and app.config['PLATFORM'] == 'heroku':
        app.app_context().push()
        init_db()
        logging.info("Initialized the db")
