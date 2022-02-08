import pytest
from tourdeflask import create_app
from tourdeflask import db
from tourdeflask.models import Item


@pytest.fixture(scope="function")
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
    app.app_context().push()

    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client


@pytest.fixture(scope="function")
def insert_tea(client):
    item = Item(name='tea', quantity='42')

    db.db.session.add(item)
    db.db.session.commit()

    item = Item.query.filter_by(name='tea').first()

    return item.id, 'tea', '42'


def test_basic_call(client):
    response = client.get('/hello')
    assert b'Welcome to Tour de Flask!' in response.data


def test_create(client):
    """
    Testuje přidání nové položky
    """
    response = client.post('/shopping-list/item',
                           data=dict(name='pea',
                                     quantity='11'))

    assert response.status_code == 201
    assert b'The item pea has been inserted 11-times' in response.data

    item = Item.query.filter_by(name='pea').first()
    assert item.quantity == 11


def test_update(client, insert_tea):
    """
    Testuje úpravu stávající položky
    """
    tea_id, _, _ = insert_tea

    response = client.put(f'/shopping-list/item/{tea_id}',
                          data=dict(name='coffee',
                                    quantity='89'))

    assert response.status_code == 200
    assert response.data == b'The item coffee has been inserted 89-times'

    item = Item.query.filter_by(id=tea_id).first()

    assert item.quantity == 89
    assert item.name == 'coffee'


def test_delete(client, insert_tea):
    """
    Testuje úpravu stávající položky
    """
    tea_id, tea_name, tea_quantity = insert_tea

    response = client.delete(f'/shopping-list/item/{tea_id}')

    assert response.status_code == 200

    item = Item.query.filter_by(name='tea').first()

    assert item is None
    assert f'The record [{tea_id}; {tea_name}; {tea_quantity}] has been deleted'\
        .encode('utf-8') in response.data


def test_not_found(client):
    response = client.delete(f'/shopping-list/item/{1}')

    assert response.status_code == 404
    assert b'Item with id 1 does not exist' in response.data
