from tourdeflask.db import db


class Item(db.Model):
    """
    Třída, která reprezentuje položku v nákupním seznamu.
    Je potomkem třídy Model z SQLAlchemy, která obsahuje funkcionalitu pro
    "propojení" s databází
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
