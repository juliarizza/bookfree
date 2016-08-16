from app import db
from user import User
from book import Book

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_lender = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    id_borrower = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
    final_date = db.Column(db.Date, nullable=False)

    lender = db.relationship(User, foreign_keys=id_lender)
    borrower = db.relationship(User, foreign_keys=id_borrower)
    book = db.relationship(Book, foreign_keys=id_book)

    def __repr__(self):
        return "<Borrow %r>" % self.id
