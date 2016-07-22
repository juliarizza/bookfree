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
    return render_template("newbook.html",
                           form=form)
