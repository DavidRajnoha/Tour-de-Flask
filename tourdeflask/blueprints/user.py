from flask import Blueprint, request, abort


from tourdeflask.db import db
from tourdeflask.models import User, ShoppingList

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()

    result = ""
    for user in users:
        result += f'{user.id}; {user.name}; {user.email}\n'

    return result


@bp.route('/', methods=['POST'])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')

    user: User = User(name=name, email=email)

    db.session.add(user)
    db.session.commit()

    return f'The user {name} has been inserted.', 201


def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        abort(404, f'User with id {user_id} does not exist')

    return user


@bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    user: User = get_user(user_id)

    name = request.form.get('name') or user.name
    email = request.form.get('email') or user.email

    user.name = name
    user.email = email

    db.session.add(user)
    db.session.commit()

    return f'The user {name} has been updated'


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # kontroluje, jestli user_id opravdu existuje
    user: User = get_user(user_id)
    db.session.delete(user)
    db.session.commit()

    return f'The record [{user_id}; {user.name}; {user.email}] has been deleted'
