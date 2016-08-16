#coding: utf-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db, lm
from app.models.user import User
from app.models.forms import LoginForm, RegisterForm, EditUserForm,\
                             ChangePasswordForm
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(email=form.email.data).first()
            except:
                user = None
            if user:
                authorized = user.check_password(form.password.data)
                if authorized:
                    login_user(user, remember=form.remember_me.data)
                    flash('Login efetuado!',category='success')
                    return redirect(url_for('index'))
                else:
                    flash('E-mail ou senha incorretos!',category='danger')
            else:
                flash('E-mail ou senha incorretos!',category='danger')
            return redirect(url_for("login"))
        flash('Usuario ou senha invalido!',category='danger')
    return render_template('user/login.html',
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).first():
            entry = User(name=form.name.data,
                         email=form.email.data,
                         password=form.password.data)
            entry.set_password(entry.password)
            db.session.add(entry)
            db.session.commit()
            flash(u"Usuário cadastrado!",category='success')
        else:
            flash(u"Usuário já existe!",category='danger')
        return redirect(url_for('login'))
    return render_template('user/register.html',
                           form=form)


@app.route('/profile/<int:id>', methods=['GET'])
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('user/profile.html',
                           user=user)


@app.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    if id != current_user.id:
        flash(u'Você não pode editar um perfil que não é seu, espertinho!',category='danger')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        User.query.filter_by(id=id).update(dict(**form.data))
        db.session.commit()
        flash(u'Perfil atualizado!', category='success')
        return redirect(url_for('profile', id=id))

    return render_template('user/edit_profile.html',
                           form=form)


@app.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    if id != current_user.id:
        flash(u'Você não pode editar um perfil que não é seu, espertinho!',category='danger')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            if form.new_password.data != form.new_password_repeat.data:
                flash(u'As senhas são diferentes!',category='warning')
                return redirect(url_for('change_password', id=id))
            else:
                user.set_password(form.new_password.data)
                flash(u'Senha atualizada!',category='success')
                return redirect(url_for('index'))
        else:
            flash(u'Sua senha atual não confere!')
            return redirect(url_for('change_password', id=id))

    return render_template('user/change_password.html',
                           form=form)


# from flask import render_template, session, request, flash
# from app import app, db
# from app.models.user import User
# from app.models.collection import Collection
# from app.models.book import Book
# from app.models.forms import LoginForm

# @app.route("/user/<int:id_user>", methods=["GET"])
# def show_user(id_user):
# 	user = user=db.session.query(User).get(id_user)
# 	collection_list = db.session.query(Collection,Book).filter(id_user==user.id).\
#     filter(Collection.id_book == Book.id).all()

# 	return render_template("user/show.html",user=user,collection_list=collection_list)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def home(path):
#     if not session.get('logged_in'):
#         return render_template('user/login.html',redir=path)
#     else:
#         return render_template(path)

# def my_page():
#         return render_template("user/show.html",user=user,collection_list=collection_list)
 
# @app.route('/login', methods=['POST'])
# def do_admin_login():
# 	login_user = User(username=request.form['username'], password=request.form['password'])

# 	if db.session.query(User).filter(username=login_user).\
# 		filter(username,password=login_user.password).count():
# 		session['logged_in'] = True
# 	else:
# 		flash('wrong password!')
# 	return home(session.path)
 
# if __name__ == "__main__":
#     app.secret_key = os.urandom(12)
#     app.run(debug=True,host='0.0.0.0', port=8080)