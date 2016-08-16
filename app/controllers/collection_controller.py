from flask import render_template, flash, redirect, url_for
from app import app, db
from flask_login import current_user
from app.models.book import Book
from app.models.collection import Collection
from app.models.sale import Sale
from app.models.forms import NewCollectionForm,EditCollectionForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField


@app.route('/collection', methods=["GET"])
def list_collection():
	collection_list = db.session.query(Collection,Book).filter(Collection.id_user==current_user.id).\
    filter(Collection.id_book == Book.id).all()

	return render_template("collection/list.html",collection_list=collection_list)

@app.route('/collection/new', methods=["GET","POST"])
def new_collection():
	form = NewCollectionForm()
	if form.validate_on_submit():
		print(form.book.id)
		b = Collection(id_user=current_user.id,
			id_book=form.book.data.id,
			quality=form.quality.data,
			status=form.status.data)
		db.session.add(b)
		db.session.commit()
		flash(u'Livro adicionado no Acervo!',category='success')
		return redirect(url_for('list_collection'))
	print (app.request_class.charset)
	#elif app.request_class.method is 'POST':
	flash(u'Dados Incorretos!',category='danger')
	return render_template("collection/new.html",form=form)

@app.route('/collection/edit/<int:id_collection>', methods=["GET","POST"])
def edit_collection(id_collection):
	form = EditCollectionForm()
	
	collection = db.session.query(Collection).\
		filter(Collection.id==id_collection).\
		first()

	book = db.session.query(Book).filter(Book.id==collection.id_book)
	form.book.query = book

	if form.validate_on_submit():
		collection.status = form.status.data
		collection.quality = form.quality.data
		db.session.commit()
		flash(u'Informacoes Salvas!',category='success')
		return redirect(url_for('list_collection'))

	app.logger.debug(form.errors)

	flash("Dados incorretos!",'warning')

	return render_template("collection/edit.html",form=form,collection=collection)
@app.route('/collection/delete/<int:id_collection>', methods=["GET","POST"])
def delete_collection(id_collection):
	
	#TODO: Add Confirmation Window

	try:
		collection = db.session.query(Collection).\
		filter(Collection.id==id_collection).delete()
		db.session.commit()
		flash(u'Livro deletado do acervo!',category='success')
	except:
		flash(u'Falha ao deletar livro do acervo!',category='danger')
		
	return redirect(url_for('list_collection'))