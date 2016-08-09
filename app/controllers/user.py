from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db, lm
from app.models.tables import User
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
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except:
            user = None
        if user:
            authorized = user.check_password(form.password.data)
            if authorized:
                login_user(user, remember=form.remember_me.data)
                flash(u'Login efetuado!')
                return redirect(url_for('index'))
            else:
                flash(u'E-mail ou senha incorretos!')
        else:
            flash(u'E-mail ou senha incorretos!')
        return redirect(url_for("login"))
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
            flash(u"Usuário cadastrado!")
        else:
            flash(u"Usuário já existe!")
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
        flash(u'Você não pode editar um perfil que não é seu, espertinho!')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        User.query.filter_by(id=id).update(dict(**form.data))
        db.session.commit()
        flash(u'Perfil atualizado!', 'positive')
        return redirect(url_for('profile', id=id))

    return render_template('user/edit_profile.html',
                           form=form)


@app.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    if id != current_user.id:
        flash(u'Você não pode editar um perfil que não é seu, espertinho!')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            if form.new_password.data != form.new_password_repeat.data:
                flash(u'As senhas são diferentes!')
                return redirect(url_for('change_password', id=id))
            else:
                user.set_password(form.new_password.data)
                flash(u'Senha atualizada!')
                return redirect(url_for('index'))
        else:
            flash(u'Sua senha atual não confere!')
            return redirect(url_for('change_password', id=id))

    return render_template('user/change_password.html',
                           form=form)
