from flask import Blueprint, request, abort

from tourdeflask.db import db
from tourdeflask.models import Item

bp = Blueprint('shopping-list', __name__, url_prefix='/shopping-list')


@bp.route('/')
def shopping_list():
    items = Item.query.all()

    result = ""
    for item in items:
        result += f'{item.id}; {item.name}: {item.quantity}\n'

    return result


@bp.route('/item', methods=['POST'])
def create_item():
    name = request.form.get('name')
    quantity = request.form.get('quantity')

    item = Item(name=name, quantity=quantity)
    db.session.add(item)
    db.session.commit()

    return f'The item {name} has been inserted {quantity}-times', 201


def get_item(item_id: int):
    item = Item.query.filter_by(id=item_id).first()

    if item is None:
        abort(404, f'Item with id {item_id} does not exist')

    return item


@bp.route('/item/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = get_item(item_id)

    name = request.form.get('name') or item.name
    quantity = request.form.get('quantity') or item.quantity

    item.name = name
    item.quantity = quantity

    db.session.add(item)
    db.session.commit()

    return f'The item {name} has been inserted {quantity}-times'


@bp.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    # kontroluje, jestli item_id opravdu existuje
    item = get_item(item_id)
    db.session.delete(item)
    db.session.commit()

    return f'The record [{item_id}; {item.name}; {item.quantity}] has been deleted'
