from tourdeflask.models import Item, ShoppingList, User


def test_item_belongs_to_shopping_list(app, inserted_list, item_tea, item_pea, item_coffee):
    """
    Test verifikující vztah mezi 'Item' a 'ShoppingList' z pohledu 'Item'
    """
    items = Item.query.with_parent(inserted_list).all()

    assert item_tea in items
    assert item_pea in items
    assert item_coffee not in items

    assert item_tea.shopping_list == inserted_list
    assert item_pea.shopping_list == inserted_list


def test_shopping_list_has_items(app, inserted_list, item_tea, item_pea, item_coffee):
    """
    Test verifikující vztah mezi 'Item' a 'ShoppingList' z pohledu 'ShoppingList'
    """
    shopping_list = ShoppingList.query.filter(
        ShoppingList.items.contains(item_tea)).first()

    assert shopping_list == inserted_list
    assert item_tea in shopping_list.items
    assert item_pea in shopping_list.items


def test_user_has_shopping_lists(app, shoppinglist, empty_shopping_list,
                                 user_tadej, user_chris):
    """
    Test verifikující vztah mezi 'User' a 'ShoppingList' z pohledu 'ShoppingList'
    Využívá definovaných a v databázi uložených uživatelů 'user_tadej' a 'user_chris',
    kdy tadej vlastní pouze 'empty_shopping_list' a chris jak 'empty_shopping_list', tak
    'shopping_lis'.
    Tyto modely jsou ytvořeny v tests/conftest.py
    """
    chrises_lists = ShoppingList.query.with_parent(user_chris).all()

    assert shoppinglist in chrises_lists
    assert empty_shopping_list in chrises_lists

    tadejs_lists = ShoppingList.query.with_parent(user_tadej).all()

    assert empty_shopping_list in tadejs_lists
    assert shoppinglist not in tadejs_lists


def test_shopping_list_has_users(app, shoppinglist, empty_shopping_list,
                                 user_tadej, user_chris):
    """
    Test verifikující vztah mezi 'User' a 'ShoppingList' z pohledu 'User'
    Využívá definovaných a v databázi uložených uživatelů 'user_tadej' a 'user_chris',
    kdy tadej vlastní pouze 'empty_shopping_list' a chris jak 'empty_shopping_list', tak
    'shopping_lisy'.
    Tyto modely jsou ytvořeny v tests/conftest.py
    """
    empty_list_owners = User.query.with_parent(empty_shopping_list).all()

    assert user_tadej in empty_list_owners
    assert user_chris in empty_list_owners

    shoppinglist_owners = User.query.with_parent(shoppinglist).all()
    assert user_chris in shoppinglist_owners
    assert user_tadej not in shoppinglist_owners
