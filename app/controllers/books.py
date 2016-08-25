from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app import app, db
from app.models.forms import SearchBook, NewBookForm
from app.models.tables import Book, UserBook

# Função que recebe um gerador e aplica o or no valores do gerador.
def or_(gen):
	# Pega o primeiro valor
    t = next(gen)
    for g in gen:
        # Aplica or entre ele e os outros valores.
        t = t | g
    return t

@app.route('/shelf/<int:id>')
def my_shelves(id):
    # Variáveis padrão para o display
    shelf = False # Mostrar gêneros
    my_books = [] # Nenhum livro disponível
    my_shelves = [] # Nenhuma estante disponível
    # Pegando a lista de generos pra filtrar
    # Por exemplo .../shelf/1?genre=Matemática&genre=Cálculo
    filters = request.args.getlist('genre')
    if len(filters) == 0: # Caso nenhuma estante tenha sido selecionada
        # A query abaixo é utilizada, que pega todos os livros daquele usuário
        # e junta eles por gênero, contando quantos livros tem em cada gênero.
        """
        SELECT
            user_book.owner_id AS user_book_owner_id
            , count(user_book.id) AS count
            , book.gender AS genre 
        FROM
            user_book JOIN book
                ON book.id = user_book.book_id 
        WHERE
            user_book.owner_id = :owner_id_1
        GROUP BY
            book.gender
        """
        qry = db.session.query( UserBook.owner_id, db.func.count(UserBook.id).label("count"), Book.gender.label('genre') ).join(Book).filter( UserBook.owner_id==id ).group_by(Book.gender)
        # Realiza a busca
        my_shelves = qry.all()
        # Diz que não foi escolhida nenhuma estante ainda
        shelf = False
    else: # Caso algum gênero tenha sido escolhido, filtra os livros por gênero
        # Uma query similar à mostrada abaixo é gerada, que pega todos os
        # livros que atendem a ao menos uma dos generos escolhidos e que sejam
        # daquele usuário.
        """
        SELECT
            user_book.id AS id
            , user_book.owner_id AS user_book_owner_id
            , book.title AS title
            , book.author AS author
        FROM
            user_book JOIN book
                ON book.id = user_book.book_id 
        WHERE
            user_book.owner_id = :owner_id_1
            AND (book.gender = :gender_1
            OR book.gender = :gender_2
            OR book.gender = ...)
        """
        qry = db.session.query( UserBook.id.label("id"), UserBook.owner_id, Book.title.label("title"), Book.author.label('author') ).join(Book).filter( (UserBook.owner_id==id) & or_( ( Book.gender==genre for genre in filters ) ) )
        # Realiza a query
        my_books = qry.all()
        # Diz que já foi escolhida alguma estante
        shelf = True
    return render_template('books/shelf.html',shelf=shelf,my_books=my_books,my_shelves=my_shelves)


@app.route('/books/<int:id>')
def my_books(id):
    my_books = UserBook.query.filter(UserBook.owner_id==id).all()
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
