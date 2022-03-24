import datetime

import pytest

from tourdeflask import create_app, db
from tourdeflask.enums import Currency
from tourdeflask.models import Item, ShoppingList, User


@pytest.fixture(scope="function")
def app():
    """
    Vytvoří Flask aplikacei s testovacím nastavením.
    Aplikace využívá databázi, která je vytvořená v operační paměti.
    scope="function" specifikuje, že se aplikace vytvoří znovu pro každou
    testovací funkci. Každá testovací funkce tak začne s čistou databází.
    """
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
    with app.app_context():
        db.init_db()
        yield app


@pytest.fixture(scope="function")
def client(app):
    """
    Client, pomocí kterého můžeme posílat requesty vůči endpointům naší aplikace.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture()
def item_tea():
    return Item(name='tea', quantity=42)


@pytest.fixture()
def item_pea():
    return Item(name='pea', quantity=23)


@pytest.fixture()
def item_coffee():
    return Item(name='coffee', quantity=11)


@pytest.fixture()
def shoppinglist(item_tea, item_pea):
    name = 'myAwesomeList'
    date = datetime.date(2022, 7, 5)
    budget = 135
    currency = Currency.EUR

    shoppinglist = ShoppingList(name=name, date=date, budget=budget, currency=currency)
    shoppinglist.items = [item_pea, item_tea]

    return shoppinglist


@pytest.fixture()
def empty_shopping_list():
    """
    ShoppingList bez jakýchkoliv itemů
    """
    name = 'emptyList'
    date = datetime.date(2022, 7, 25)
    budget = 111
    currency = Currency.USD

    sl = ShoppingList(name=name, date=date, budget=budget, currency=currency)
    db.db.session.add(sl)
    db.db.session.commit()

    return sl


@pytest.fixture()
def inserted_list(shoppinglist):
    """
    Vloží shoppingList do databáze
    """
    db.db.session.add(shoppinglist)
    db.db.session.commit()

    shoppinglist = ShoppingList.query.filter_by(name=shoppinglist.name).first()

    return shoppinglist


@pytest.fixture()
def user_chris(shoppinglist, empty_shopping_list):
    """
    User, který vlastní 'shopping_list' i 'empty_shopping_list',
    uložený v databázi.
    """
    name = 'Chris Froome'
    email = 'froomy@teamsky.com'

    user = User(name=name, email=email)
    user.shopping_lists = [shoppinglist, empty_shopping_list]

    db.db.session.add(user)
    db.db.session.commit()

    return user


@pytest.fixture()
def user_tadej(empty_shopping_list):
    """
    User, který vlastní 'empty_shopping_list',
    uložený v databázi.
    """
    name = 'Tadej Pogacar'
    email = 'tadej@uaeteamemirates.com'

    user = User(name=name, email=email)
    user.shopping_lists = [empty_shopping_list]

    db.db.session.add(user)
    db.db.session.commit()

    return user
