from app import db
from user import User
from book import Book
from collection import Collection

class Sale(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    id_collection = db.Column(db.Integer, db.ForeignKey(Collection.id), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    shipping = db.Column(db.Float,nullable=False)
    description = db.Column(db.String, nullable=False)

    collection = db.relationship(Collection, foreign_keys=id_collection)