import pytest

from tourdeflask import db
from tourdeflask.models import Item


@pytest.fixture(scope="function")
def insert_tea(client, empty_shopping_list):
    item = Item(name='tea', quantity='42')

    empty_shopping_list.items = [item]

    db.db.session.add(empty_shopping_list)
    db.db.session.commit()

    item = Item.query.with_parent(empty_shopping_list).filter_by(name='tea').first()

    return item


def test_create(client, empty_shopping_list):
    """
    Testuje přidání nové položky
    """

    response = client.post(f'/shopping-list/{empty_shopping_list.id}/item/',
                           data=dict(name='pea',
                                     quantity='11'))

    assert response.status_code == 201

    assert b'The item pea has been inserted 11-times' in response.data

    item = Item.query.filter_by(name='pea').first()
    assert item.quantity == 11
    assert item.shopping_list == empty_shopping_list


def test_update(client, insert_tea):
    """
    Testuje úpravu stávající položky
    """
    tea_item = insert_tea

    response = client.put(f'/shopping-list/{tea_item.shopping_list_id}/item/{tea_item.id}',
                          data=dict(name='coffee',
                                    quantity='89'))

    assert response.status_code == 200

    assert response.data == b'The item coffee has been inserted 89-times'

    item = Item.query.filter_by(id=tea_item.id).first()

    assert item.quantity == 89
    assert item.name == 'coffee'


def test_delete(client, insert_tea):
    """
    Testuje smazání stávající položky
    """
    tea_item: Item = insert_tea

    response = client.delete(f'/shopping-list/{tea_item.shopping_list_id}/item/{tea_item.id}')

    assert response.status_code == 200

    item = Item.query.filter_by(name='tea').first()

    assert item is None
    assert f'The record [{tea_item.id}; {tea_item.name}; {tea_item.quantity}] has been deleted' \
           .encode('utf-8') in response.data
