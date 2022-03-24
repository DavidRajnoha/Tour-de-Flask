import pytest

from tourdeflask.models import ShoppingList, Item, User


@pytest.fixture()
def user_not_saved(empty_shopping_list):
    """
    User, který vlastní 'empty_shopping_list',
    uložený v databázi.
    """
    name = 'Primos Roglic'
    email = 'primos@teamjumbo.com'

    user = User(name=name, email=email)

    return user


def test_create(client, user_not_saved):
    """
    Testuje přidání nové položky
    """
    response = client.post('/user/',
                           data=dict(name=user_not_saved.name,
                                     email=user_not_saved.email))

    assert response.status_code == 201
    assert f'The user {user_not_saved.name} has been inserted'.encode('utf8') in response.data

    created_user = User.query.filter_by(name=user_not_saved.name).first()

    assert created_user.name == user_not_saved.name
    assert created_user.email == user_not_saved.email


def test_get(client, user_chris):
    response = client.get('/user/')

    assert response.status_code == 200
    assert f'{user_chris.id}; {user_chris.name};' \
           f' {user_chris.email}\n'.encode('utf8') in response.data


def test_update(client, user_chris):
    """
    Testuje odstraňení nákupního seznamu. Když je odstraňen nákupní seznam,
    měly by být odstraněny i odpovídající položky.

    """
    email_updated = "froomey@israelcyclingacademy.com"

    response = client.put(f'/user/{user_chris.id}',
                          data=dict(email=email_updated))

    user_updated: User = User.query.filter_by(id=user_chris.id).first()

    assert response.status_code == 200
    assert user_updated.name == user_chris.name
    assert user_updated.email == email_updated


def test_delete(client, user_chris, shoppinglist):
    """
    Testuje odstraňení nákupního seznamu. Když je odstraňen nákupní seznam,
    měly by být odstraněny i odpovídající položky.

    """
    response = client.delete(f'/user/{user_chris.id}')

    deleted_user = User.query.filter_by(id=user_chris.id).first()
    not_deleted_list = ShoppingList.query.filter_by(id=shoppinglist.id)

    assert response.status_code == 200
    assert deleted_user is None
    assert not_deleted_list is not None
