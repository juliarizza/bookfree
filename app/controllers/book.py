from flask import render_template
from app import app, db
from app.models.forms import NewBookForm
from app.models.tables import Book

@app.route("/novo_livro", methods=["GET", "POST"])
def new_book():
    form = NewBookForm()
    if form.validate_on_submit():
        b = Book(title=form.title.data,
                 author=form.author.data,
                 publisher=form.publisher.data,
                 gender=form.gender.data)
        db.session.add(b)
        db.session.commit()
    return render_template("book/newbook.html",
                           form=form)
@app.route("/book/list", methods=["GET"])
def list_all():
    return render_template("book/listbook.html",books=db.session.query(Book).all())

@app.route("/book/<int:id_book>", methods=["GET"])
def show_book(id_book):
    return render_template("book/showbook.html",book=db.session.query(Book).get(id_book))