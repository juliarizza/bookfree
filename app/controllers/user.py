from flask import render_template
from app import app, db
from app.models.tables import User,Collection,Book

@app.route("/user/<int:id_user>", methods=["GET"])
def show_user(id_user):
	user = user=db.session.query(User).get(id_user)
	#collection_list = db.session.query(Collection).filter().join(Book)

	collection_list = db.session.query(Collection,Book).filter(id_user==user.id).\
    filter(Collection.id_book == Book.id).all()

	return render_template("user/showuser.html",user=user,collection_list=collection_list)