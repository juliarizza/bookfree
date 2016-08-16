#coding: utf-8

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user
from app.models.book import Book
from app.models.collection import Collection
from app.models.sale import Sale
from app.models.forms import NewSaleForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField




@app.route('/sale', methods=["GET"])
def list_sale():
	collection_list = db.session.query(Collection,Book,Sale).\
	filter(Collection.id_user==current_user.id).\
    filter(Collection.id_book == Book.id).\
    filter(Sale.id_collection == Collection.id).\
    all()
	print("Dentro do list sale")
	return render_template("sale/list.html",collection_list=collection_list)

@app.route('/sale/save', methods=["POST"])
def save_sale(sale,action):
	return render_template("sale/list.html")
	# try:
	# 	action = int(action)
	# 	if(action == 1): #add
	# 		db.session.add(sale)
	# 		message = 'Livro adicionado para a venda!'
	# 	else: #update
	# 		s = db.session.query(Collection).\
	# 		filter(Sale.id_collection==sale.id_collection).\
	# 		first()
	# 		if s is None:
	# 			print ("S == none")

	# 		s.price = sale.price
	# 		s.shipping = sale.shipping
	# 		s.description = sale.description
	# 		message = 'Dados da venda atualizado!'	

	# 	db.session.commit()
	# 	flash(message,category='success')

	# 	return list_sale()
	# except Exception, e:
	# 	flash(u'Algo deu muito errado!',category='danger')
	# 	list_sale()
	# finally:
	# 	pass

@app.route('/sale/add/<int:id>', methods=["GET","POST"])
def add_sale(id):
	if db.session.query(Sale).get(id):
		flash(u'Este livro já está a venda!',category='danger')	
	else:
		form = NewSaleForm()
		collection = db.session.query(Collection,Book).\
		filter(Collection.id==id).\
		filter(Collection.id_book==Book.id).\
		first()
		form.book.data = collection.Book
		form.action_id.data = 1
		if request.method == 'POST':
			if form.validate_on_submit():
				s = Sale(id_collection=id,
					price=form.price.data,
					shipping=form.shipping.data,
					description=form.description.data)
				db.session.add(s)
				db.session.commit()
				flash(u'Livro disponibilizado para a venda!',category='success')	
				return redirect(url_for('list_sale'))

			flash(u'Dados inválidos!',category='danger')	
			
		return render_template("sale/new.html",form=form)
		
	return redirect(url_for('list_collection'))

@app.route('/sale/edit/<int:id>', methods=["GET","POST"])
def edit_sale(id):
	form = NewSaleForm()
	collection = db.session.query(Collection,Book,Sale).\
	filter(Collection.id==id).\
	filter(Collection.id_book==Book.id).\
	filter(Collection.id==Sale.id_collection).\
	first()

	form.book.data = collection.Book

	form.action_id.data = 2
	if request.method == 'POST':
		if form.validate_on_submit():
			s = db.session.query(Collection).\
			filter(Sale.id_collection==id).\
			first()
			s.price = form.price.data
			s.shipping = form.shipping.data
			s.description = form.shipping.data
			db.session.commit()
			message = 'Dados da venda atualizado!'
			flash(message,category='success')
			return redirect(url_for('list_sale'))
		flash(u'Dados inválidos!',category='danger')
		return redirect(url_for('list_sale'))
		
	return render_template("sale/new.html",form=form,sale=collection.Sale)

# @app.route('/collection/new', methods=["GET","POST"])
# def new_collection():
# 	form = NewCollectionForm()
# 	if form.validate_on_submit():
# 		print(form.book.id)
# 		b = Collection(id_user=current_user.id,
# 			id_book=form.book.data.id,
# 			quality=form.quality.data,
# 			status=form.status.data)
# 		db.session.add(b)
# 		db.session.commit()
# 		flash(u'Livro adicionado no Acervo!',category='success')
# 		return redirect(url_for('list_collection'))
# 	print (app.request_class.charset)
# 	#elif app.request_class.method is 'POST':
# 	flash(u'Dados Incorretos!',category='danger')
# 	return render_template("collection/new.html",form=form)

# @app.route('/collection/edit/<int:id_collection>', methods=["GET","POST"])
# def edit_collection(id_collection):
# 	form = EditCollectionForm()
	
# 	collection = db.session.query(Collection).\
# 		filter(Collection.id==id_collection).\
# 		first()

# 	book = db.session.query(Book).filter(Book.id==collection.id_book)
# 	form.book.query = book

# 	if form.validate_on_submit():
# 		collection.status = form.status.data
# 		collection.quality = form.quality.data
# 		db.session.commit()
# 		flash(u'Informações Salvas!',category='success')
# 		return redirect(url_for('list_collection'))

# 	app.logger.debug(form.errors)

# 	flash("Dados incorretos!",'warning')

# 	return render_template("collection/edit.html",form=form,collection=collection)
# @app.route('/collection/delete/<int:id_collection>', methods=["GET","POST"])
# def delete_collection(id_collection):
	
# 	#TODO: Add Confirmation Window

# 	try:
# 		collection = db.session.query(Collection).\
# 		filter(Collection.id==id_collection).delete()
# 		db.session.commit()
# 		flash(u'Livro deletado do acervo!',category='success')
# 	except:
# 		flash(u'Falha ao deletar livro do acervo!',category='danger')
		
# 	return redirect(url_for('list_collection'))