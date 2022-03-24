from flask import Blueprint, request, abort


from tourdeflask.db import db
from tourdeflask.models import Item, ShoppingList

bp_item = Blueprint('item', __name__, url_prefix='/item')


@bp_item.route('/', methods=['GET'])
def get_items(shopping_list_id):
    items = Item.query.filter_by(shopping_list_id=shopping_list_id).all()

    result = ""
    for item in items:
        result += f'{item.id}; {item.name}: {item.quantity}\n'

    return result


@bp_item.route('/', methods=['POST'])
def create_item(shopping_list_id):
    name = request.form.get('name')
    quantity = request.form.get('quantity')

    shopping_list: ShoppingList = ShoppingList\
        .query.filter_by(id=shopping_list_id).first()
    item = Item(name=name, quantity=quantity)

    shopping_list.items.append(item)

    db.session.add(shopping_list)
    db.session.commit()

    return f'The item {name} has been inserted {quantity}-times', 201


def get_item(shopping_list_id: int, item_id: int):
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    item = Item.query.with_parent(shopping_list)\
        .filter_by(id=item_id)\
        .first()

    if item is None:
        abort(404, f'Item with id {item_id} does not exist')

    return item


@bp_item.route('/<item_id>', methods=['PUT'])
def update_item(shopping_list_id, item_id):
    item = get_item(shopping_list_id, item_id)

    name = request.form.get('name') or item.name
    quantity = request.form.get('quantity') or item.quantity

    item.name = name
    item.quantity = quantity

    db.session.add(item)
    db.session.commit()

    return f'The item {name} has been inserted {quantity}-times'


@bp_item.route('/<item_id>', methods=['DELETE'])
def delete_item(shopping_list_id, item_id):
    # kontroluje, jestli item_id opravdu existuje
    item = get_item(shopping_list_id, item_id)
    db.session.delete(item)
    db.session.commit()

    return f'The record [{item_id}; {item.name}; {item.quantity}] has been deleted'
