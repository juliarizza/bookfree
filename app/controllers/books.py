from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from app import app, db
from app.models.forms import SearchBook, NewBookForm
from app.models.tables import Book, UserBook


@app.route('/my_books/<int:id>')
def my_books(id):
    my_books = UserBook.query.filter_by(owner_id=id).all()
    return render_template('books/my_books.html',
                           my_books=my_books)


@app.route('/search', methods=["GET", "POST"])
def search():
    books = None
    form = SearchBook()
    if form.validate_on_submit():
        query = "%{0}%".format(form.book.data)
        books = Book.query.filter(Book.title.like(query)).all()

    return render_template('books/search.html',
                           form=form,
                           books=books)


@app.route("/new_book", methods=["GET", "POST"])
def new_book():
    form = NewBookForm()
    if form.validate_on_submit():
        b = Book(title=form.title.data,
                 author=form.author.data,
                 publisher=form.publisher.data,
                 gender=form.gender.data)
        db.session.add(b)
        db.session.commit()
        flash(u'New book added!')
        return redirect(url_for('search'))
    elif form.errors:
        flash(u'Invalid submit. Please, try again!')
    return render_template("books/new_book.html",
                           form=form)


@app.route('/add_book/<int:id>')
def add_book(id):
    register = UserBook.query.filter_by(book_id=id, owner_id=current_user.id).first()
    if not register:
        new_book = UserBook(
                            book_id=id,
                            owner_id=current_user.id
                           )
        db.session.add(new_book)
        db.session.commit()
        flash(u'Book added!')
        return redirect(url_for('search'))
    else:
        flash(u'You already added this book!')
        return redirect(url_for('search'))


@app.route('/remove_book/<int:id>')
def remove_book(id):
    book = UserBook.query.get(id)
    db.session.delete(book)
    db.session.commit()
    flash(u'Book deleted!')
    return redirect(url_for('my_books', id=current_user.id))
