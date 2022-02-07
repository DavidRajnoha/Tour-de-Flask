import os
import tempfile

import pytest
from tourdeflask import create_app
from tourdeflask.db import init_db, get_db


@pytest.fixture(scope="function")
def client():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture(scope="function")
def insert_tea(client):
    client.post('/shopping-list/item',
                data=dict(name='tea',
                          quantity='42'))
    item = get_db().execute(
        'SELECT id, name, quantity FROM item WHERE name = ?',
        ('tea',)).fetchone()
    return item['id'], 'tea', '42'


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

    item = get_db().execute(
        'SELECT id, name, quantity FROM item WHERE name = ?',
        ('pea',)).fetchone()

    assert item['quantity'] == 11


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

    item = get_db().execute(
        'SELECT id, name, quantity FROM item WHERE id = ?',
        (tea_id,)).fetchone()

    assert item['quantity'] == 89
    assert item['name'] == 'coffee'


def test_delete(client, insert_tea):
    """
    Testuje úpravu stávající položky
    """
    tea_id, tea_name, tea_quantity = insert_tea

    response = client.delete(f'/shopping-list/item/{tea_id}')

    assert response.status_code == 200

    item = get_db().execute(
        'SELECT id, name, quantity FROM item WHERE id = ?',
        (tea_id,)).fetchone()

    assert item is None
    assert f'The record [{tea_id}; {tea_name}; {tea_quantity}] has been deleted'\
        .encode('utf-8') in response.data


def test_not_found(client):
    response = client.delete(f'/shopping-list/item/{1}')

    assert response.status_code == 404
    assert b'Item with id 1 does not exist' in response.data
