import datetime
from os import linesep
from typing import List

from flask import Blueprint, request, abort

from tourdeflask.db import db
from tourdeflask.models import ShoppingList
from tourdeflask.enums import Currency
from tourdeflask.blueprints.item import bp_item as bp_item

bp_lists = Blueprint('shopping-lists', __name__, url_prefix='/shopping-list')
bp_list = Blueprint('shopping-list', __name__, url_prefix='/<shopping_list_id>')

bp_lists.register_blueprint(bp_list)
bp_list.register_blueprint(bp_item)


@bp_lists.route('/')
def get_shopping_lists():
    """
    View, který vypíše všechny existující ShoppingListy 
    """
    shopping_lists: List[ShoppingList] = ShoppingList.query.all()

    result = ""
    for shopping_list in shopping_lists:
        result += format_shopping_list(shopping_list)

    return result


def format_shopping_list(shopping_list: ShoppingList):
    return f'{shopping_list.id}, {shopping_list.name}, {shopping_list.date},' \
                  f' {shopping_list.budget}, {shopping_list.currency}{linesep}'


@bp_lists.route('/', methods=['POST'])
def create_shoppinglist():
    """
    Vytvoření nového modelu ShoppingList na základě argumentů html POST requestu
    a následné uložení modelu do databáze.
    """
    name = request.form.get('name')
    date = datetime.date.fromisoformat(request.form.get('date'))
    budget = int(request.form.get('budget'))
    currency = Currency(request.form.get('currency'))

    shoppinglist: ShoppingList = ShoppingList(name=name,
                                date=date,
                                budget=budget,
                                currency=currency)

    db.session.add(shoppinglist)
    db.session.commit()

    return f'The list {name} has been inserted created', 201


def find_shopping_list(shopping_list_id: int):
    shopping_list: ShoppingList = ShoppingList.query.filter_by(id=shopping_list_id).first()

    if shopping_list is None:
        abort(404, f'Item with id {shopping_list_id} does not exist')

    return shopping_list


@bp_list.route('/', methods=['GET'])
def get_shopping_list(shopping_list_id: int):
    shopping_list = find_shopping_list(shopping_list_id)
    return format_shopping_list(shopping_list)


@bp_list.route('/', methods=['PUT'])
def update_shopping_list(shopping_list_id: int):
    """
    Vytvoření nového modelu ShoppingList na základě argumentů html POST requestu
    a následné uložení modelu do databáze.
    """
    sl: ShoppingList = find_shopping_list(shopping_list_id)

    sl.name = request.form.get('name') or sl.name
    sl.date = datetime.date.fromisoformat(request.form.get('date')) if request.form.get('date') else sl.date
    sl.budget = int(request.form.get('budget')) if request.form.get('budget') else sl.budget
    sl.currency = Currency(request.form.get('currency')) if request.form.get('currency') else sl.currency

    db.session.add(sl)
    db.session.commit()

    return f'The list {sl.name} has been updated', 200


@bp_list.route('/', methods=['DELETE'])
def delete_shopping_list(shopping_list_id: int):
    """
    Odstranění shopping listu
    Itemy v něm obsažené jsou také smazány díky sqlalchemy cascade
    """
    sl: ShoppingList = find_shopping_list(shopping_list_id)

    db.session.delete(sl)
    db.session.commit()

    return f'The list {sl.name} has been deleted', 200

