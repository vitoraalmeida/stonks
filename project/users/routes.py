from . import users_blueprint
from flask import render_template, flash, abort, request, current_app, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegistrationForm, LoginForm
from project.models import User
from project import database
from sqlalchemy.exc import IntegrityError

@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('users/403.html'), 403


@users_blueprint.route('/admin')
def admin():
    abort(403)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash(f'Obrigado por se registrar, {new_user.email}!')
                current_app.logger.info(f'Registered new user: {form.email.data}')
                return redirect(url_for('stocks.list_stocks'))
            # email já registrado (email unique)
            except IntegrityError:
                database.session.rollback()
                flash(f'ERRO: dados inválidos foram usados para registro.')
        else:
            flash(f'ERRO: dados inválidos foram usados para registro.')
    # caso de GET
    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já está logado, não deixa logar novamente
    # current_user é um proxy fornecido pelo flask_login
    if current_user.is_authenticated:
        flash('Você já está logado!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            query = database.select(User).where(User.email == form.email.data)
            user = database.session.execute(query).scalar_one()

            if user and user.is_password_correct(form.password.data):
                # credenciais validadas, deixa logar
                # se usuário não tiver selecionado a opção de manter logado, quando fechar o browser será deslogado
                
                login_user(user, remember=form.remember_me.data)
                flash(f'Bem vindo, {current_user.email}!')
                current_app.logger.info(f'Logged in user: {current_user.email}')
                return redirect(url_for('index'))

        flash('ERRO! Credenciais inválidas.', 'error')
    # GET
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required # apenas usuários logados podem acessa a rota
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Até a próxima!')
    return redirect(url_for('index'))

