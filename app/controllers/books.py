from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import app, db
from app.models.forms import SearchBook, NewBookForm
from app.models.tables import Book, UserBook
from flask_sqlalchemy import SQLAlchemy

def or_(gen):
    t = next(gen)
    for g in gen:
        t = t | g
    return t


@app.route('/shelf/<int:id>')
def my_shelves(id):
    #Pegando a lista de generos pra filtrar
    filters = request.args.getlist('genre')
    print(filters)
    if len(filters) == 0: # Nenhuma estante selecionada
        #qry = UserBook.query.join(Book).filter(UserBook.owner_id==id).group_by(Book.gender)
        qry = db.session.query( UserBook.owner_id, db.func.count(UserBook.id).label("count"), Book.gender.label('genre') ).join(Book).filter( UserBook.owner_id==id ).group_by(Book.gender)
        print( qry )
        my_shelves = qry.all()
        print(my_shelves)
        return render_template('books/shelf.html',shelf=False,my_shelves=my_shelves)
    else: # Filtra pelas estantes
        qry = db.session.query( UserBook.id.label("id"), UserBook.owner_id, Book.title.label("title"), Book.author.label('author') ).join(Book).filter( (UserBook.owner_id==id) & or_( ( Book.gender==genre for genre in filters ) ) )
        print( qry )
        my_books = qry.all()
        print( my_books )
        return render_template('books/shelf.html',shelf=True,my_books=my_books)
    return "bla" 


@app.route('/books/<int:id>')
def my_books(id):
    my_books = UserBook.query.filter(UserBook.owner_id==id).all()
    #print(my_books)
    #for b in my_books:
    #    print(b)
    return render_template('books/my_books.html',
                           my_books=my_books)


@app.route('/books/search', methods=["GET", "POST"])
def search():
    books = None
    form = SearchBook()
    if form.validate_on_submit():
        query = "%{0}%".format(form.book.data)
        books = Book.query.filter(Book.title.like(query)).all()

    return render_template('books/search.html',
                           form=form,
                           books=books)


@app.route("/books/new", methods=["GET", "POST"])
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


@app.route('/books/add/<int:id>')
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


@app.route('/books/remove/<int:id>')
def remove_book(id):
    book = UserBook.query.get(id)
    db.session.delete(book)
    db.session.commit()
    flash(u'Book deleted!')
    return redirect(url_for('my_books', id=current_user.id))
