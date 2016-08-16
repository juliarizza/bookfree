from flask import render_template
from app import app, db
from app.models.forms import NewBookForm
from app.models.book import Book
from flask import render_template, flash, redirect, url_for

@app.route("/book/new", methods=["GET", "POST"])
def new_book():
    form = NewBookForm()
    if form.validate_on_submit():
        b = Book(title=form.title.data,
                 author=form.author.data,
                 publisher=form.publisher.data,
                 gender=form.gender.data)
        db.session.add(b)
        db.session.commit()
        flash(u'Livro cadastrado com sucesso!',category='success')
        return redirect(url_for('show_book', id_book=b.id))
    else:
        flash(u'Dados Incorretos!',category='warning')
    return render_template("book/new.html",
                           form=form)
@app.route("/book/list", methods=["GET"])
def list_all_book():
    return render_template("book/list.html",books=db.session.query(Book).all())

@app.route("/book/<int:id_book>", methods=["GET"])
def show_book(id_book):
    form = NewBookForm()
    return render_template("book/show.html",book=db.session.query(Book).get(id_book),form=form)