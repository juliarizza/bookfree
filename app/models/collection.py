from app import db
from user import User
from book import Book

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id))
    id_book = db.Column(db.Integer, db.ForeignKey(Book.id))
    quality = db.Column(db.String)
    status = db.Column(db.String)

    book = db.relationship(Book, foreign_keys=id_book)
    user = db.relationship(User, foreign_keys=id_user)