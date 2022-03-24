from tourdeflask.db import db
from tourdeflask.enums import Currency


class Item(db.Model):
    """
    Třída, která reprezentuje položku v nákupním seznamu.
    Je potomkem třídy Model z SQLAlchemy, která obsahuje funkcionalitu pro
    "propojení" s databází.
    Každý item patří do jednoho nákupního seznamu.
    """
    # v Flask-SQLAlchemy není povinné, ale zde pro lepší přehlednost uvedeno
    __tablename__ = 'items'
    # definice jednotlivých sloupců databáze
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    # sloupec definující cizí klíč pro shopping_list, kterému item patři
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'))
    # specifikace vztahu s ShoppingList, tak aby bylo možné přistoupit k shopping_list
    # jako k atributu ITEM
    # TODO: ShoppingList odkazuje na název třídy, 'items' na název tabulky
    shopping_list = db.relationship("ShoppingList", back_populates='items')


# asociační tabulka určená k vytvoření many-to-many relationship mezi ShoppingList a User
# sloupce jsou obsazeny id jednotlivých tabulek (a označeny jako cizí klíče)
list_user_association_table = db.Table('list_user_association', db.Model.metadata,
                                       db.Column('shopping_list_id', db.ForeignKey('shopping_list.id')),
                                       db.Column('user_id', db.ForeignKey('user.id')))


class ShoppingList(db.Model):
    """
    Třída reprezentující nákupn( seznam.
    Tento nákupní seznam obsahuje v(ce itemu, ke kterým lze
    přistupovat přes attribut items.
    Stejně tak je nákupní seznam asociovaný s několika uživateli.
    Jelikož i uživatelé mohou mít více nákupních seznamů, je tento
    vztah realizov*n pomoc( asociacn( tabulky list_user_asssociation table.
    """
    __tablename__ = 'shopping_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    budget = db.Column(db.Integer)
    currency = db.Column(db.Enum(Currency))

    # Specifikace vztahu s Item, aby bylo možné přistupovat skrz atribut, obdobně jako výše v Item
    items = db.relationship('Item', back_populates='shopping_list', cascade='all, delete-orphan')

    # definice many-to-many vztahu skrze asociační tabulku
    # 'User' odkazuje na název třídy, secondary na asociační tabulku
    # a back_populates na název tabulky, se kterou se vztah tvoří
    users = db.relationship(
        "User",
        secondary=list_user_association_table,
        back_populates='shopping_lists'
    )


class User(db.Model):
    """
    Model reprezentující uživatele, který vlastní více nákupních seznamů.
    Logika provázání je stejná, jako na druhé straně vztahu, v tabulce shopping list
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    shopping_lists = db.relationship(
        "ShoppingList",
        secondary=list_user_association_table,
        back_populates='users'
    )
