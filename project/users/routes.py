from . import users_blueprint
from datetime import datetime
from flask import copy_current_request_context, render_template, flash, abort, request, current_app, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from .forms import RegistrationForm, LoginForm
from project.models import User
from project import database, mail
from sqlalchemy.exc import IntegrityError
from threading import Thread
from urllib.parse import urlparse

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
                flash(f'Obrigado por se registrar, {new_user.email}! Por favor, cheque seu email para confirmar o endereço de email.', 'success')
                current_app.logger.info(f'Registered new user: {form.email.data}')
                
                # configura o flask para fazer cópia do contexto para enviar 
                # o email em outra thread. Só funciona em view functions
                @copy_current_request_context
                def send_email(message):
                    with current_app.app_context():
                        mail.send(message)

                msg = generate_confirmation_email(form.email.data)
                # cria a thread e inicia
                email_thread = Thread(target=send_email, args=[msg])
                email_thread.start()

                return redirect(url_for('users.login'))
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

                if not request.args.get('next'):
                    return redirect(url_for('users.user_profile'))

                next_url = request.args.get('next')
                current_app.logger.debug(f"{next_url}")
                current_app.logger.debug(f"{urlparse(next_url)}")
                if urlparse(next_url).scheme != '' or urlparse(next_url).netloc != '':
                    current_app.logger.info(f'Invalid next path in login request: {next_url}')
                    logout_user()
                    return abort(400)
                    current_app.logger.info(f'Redirecting after valid login to: {next_url}')
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


@users_blueprint.route('/profile')
@login_required
def user_profile():
    return render_template('users/profile.html')


@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature:
        flash('O link de confirmação expirou ou é inválido.', 'error')
        current_app.logger.info(f'Invalid or expired confirmation link received from IP address: {request.remote_addr}')
        return redirect(url_for('users.login'))

    query = database.select(User).where(User.email == email)
    user = database.session.execute(query).scalar_one()

    if user.email_confirmed:
        flash('A conta já foi verificada. Faça o login', 'info')
        current_app.logger.info(f'Confirmation link received for a confirmed user: {user.email}')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        database.session.add(user)
        database.session.commit()
        flash('Obrigado por confirmar seu email!', 'success')
        current_app.logger.info(f'Email address confirmed for: {user.email}')

    return redirect(url_for('index'))


def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('users.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True) # gera url absoluta
    return Message(subject='Stonks - Confirme seu endereço de email',
                   html=render_template('users/email_confirmation.html', confirm_url=confirm_url),
                   recipients=[user_email])

