# Import třídy Flask z knihovny flsk
from flask import Flask, request, abort
import os
from . import db

# Vytvoření app objektu, který tvoří jádro naší aplikace
# (Pro zajemce: wsgi aplikace)
app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route('/shopping-list')
def shopping_list():
    db_conn = db.get_db()
    items = db_conn.execute(
        ' SELECT id, name, quantity '
        ' FROM item '
        ' ORDER BY id DESC ').fetchall()

    result = ""

    for item in items:
        result += f'{item["id"]}; {item["name"]}: {item["quantity"]}\n'

    return result


@app.route('/shopping-list/item', methods=['POST'])
def create_item():
    name = request.form.get('name')
    quantity = request.form.get('quantity')

    db_conn = db.get_db()

    db_conn.execute(
        'INSERT INTO item (name, quantity) '
        'VALUES (?, ?) ',
        (name, int(quantity))
    )
    db_conn.commit()

    return f'The item {name} has been inserted {quantity}-times', 201


def get_item(item_id: int):
    item = db.get_db().execute(
        'SELECT id, name, quantity FROM item WHERE id = ?',
        (item_id,)).fetchone()

    if item is None:
        abort(404, f'Item with id {item_id} does not exist')

    return item


@app.route('/shopping-list/item/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = get_item(item_id)

    name = request.form.get('name') or item['name']
    quantity = request.form.get('quantity') or item['quantity']

    db_conn = db.get_db()
    db_conn.execute(
        ' UPDATE item SET name = ?, quantity = ? WHERE id = ? ',
        (name, int(quantity), item_id)
    )
    db_conn.commit()

    return f'The item {name} has been inserted {quantity}-times'


@app.route('/shopping-list/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    # kontroluje, jestli item_id opravdu existuje
    item = get_item(item_id)

    db_conn = db.get_db()
    db_conn.execute(
        'DELETE FROM item WHERE id =?',
        item_id
    )
    db_conn.commit()

    return f'The record [{item_id}; {item["name"]}; {item["quantity"]}] has been deleted'


# Při zadání 127.0.0.1:5000/ se spustí funkce hello. V tomto kontextu se o ní bavíme jako o view.
@app.route('/hello')
def hello():
    return 'Welcome to Tour de Flask!\nThe tour will start on 1st July 2022'

