from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from webapp.db import db
from webapp.user.forms import LoginForm, RegForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        if request.values.get('next'):
            return redirect(request.values.get('next'))
        return redirect(url_for('news.index'))
    title = 'Авторизация'
    form = LoginForm()
    return render_template(
        'login.html',
        title=title,
        form=form,
    )


@blueprint.route('/login-process', methods=['POST'])
def login_process():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('С возращением!')
        if request.values.get('next'):
            return redirect(request.values.get('next'))
        return redirect(url_for('news.index'))
    flash('Проверьте корректность имени пользователя и пароля')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('news.index'))


@blueprint.route('/reg')
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = RegForm()
    return render_template(
        'reg.html',
        title=title,
        form=form,
    )


@blueprint.route('/reg-process', methods=['POST'])
def reg_process():
    form = RegForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            status='admin',
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {field}: {error}')
        return redirect(url_for('user.reg'))
