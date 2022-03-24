from tourdeflask.models import ShoppingList, Item


def test_create(client, shoppinglist):
    """
    Testuje přidání nové položky
    """
    response = client.post('/shopping-list/',
                           data=dict(name=shoppinglist.name,
                                     date=shoppinglist.date,
                                     budget=str(shoppinglist.budget),
                                     currency=shoppinglist.currency.value))

    assert response.status_code == 201
    assert f'The list {shoppinglist.name} has been inserted created'.encode('utf8') in response.data

    created_list = ShoppingList.query.filter_by(name=shoppinglist.name).first()

    assert created_list.date == shoppinglist.date
    assert created_list.budget == shoppinglist.budget
    assert created_list.currency == shoppinglist.currency


def test_get(client, inserted_list):
    response = client.get('/shopping-list/')

    assert response.status_code == 200
    assert f'{inserted_list.id}, {inserted_list.name},' \
           f' {inserted_list.date}, {inserted_list.budget},' \
           f' {inserted_list.currency}'.encode('utf8') in response.data


def test_get_individual_list(client, inserted_list):
    response = client.get(f'/shopping-list/{inserted_list.id}/')

    assert response.status_code == 200
    assert f'{inserted_list.id}, {inserted_list.name},' \
           f' {inserted_list.date}, {inserted_list.budget},' \
           f' {inserted_list.currency}'.encode('utf8') in response.data


def test_update(client, inserted_list):
    """
    Testuje odstraňení nákupního seznamu. Když je odstraňen nákupní seznam,
    měly by být odstraněny i odpovídající položky.

    """
    name_updated = "Updated Name"
    budget_updated = 1989

    response = client.put(f'/shopping-list/{inserted_list.id}/',
                          data=dict(name=name_updated,
                                    budget=str(budget_updated)))

    shopping_list: ShoppingList = ShoppingList.query.filter_by(id=inserted_list.id).first()

    assert response.status_code == 200
    assert shopping_list.name == name_updated
    assert shopping_list.budget == budget_updated
    assert shopping_list.date == inserted_list.date
    assert shopping_list.currency == inserted_list.currency


def test_delete(client, inserted_list):
    """
    Testuje odstraňení nákupního seznamu. Když je odstraňen nákupní seznam,
    měly by být odstraněny i odpovídající položky.

    """
    item = Item.query.with_parent(inserted_list).first()

    response = client.delete(f'/shopping-list/{inserted_list.id}/')
    shopping_list = ShoppingList.query.filter_by(id=inserted_list.id).first()

    deleted_item = Item.query.filter_by(id=item.id).first()

    assert response.status_code == 200
    assert shopping_list is None
    assert deleted_item is None
