import click
from flask import current_app, g
from flask.cli import with_appcontext

import sqlite3


def get_db():
    """
    funkce, která vytvoří spojení s databází, pokud takové ještě neexistuje a není uložené
    v g - globálním kontextu aplikace, unikátním pro každý request
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Zavře spojení s databází, pokud bylo vytvořeno
    :param e:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


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
    Nastaví automatické odstranění databáze po skončení requestu a
    přidá
    :param app:
    :return:
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
