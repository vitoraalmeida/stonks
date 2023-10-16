from . import users_blueprint
from flask import render_template, flash, abort, request, current_app, redirect, url_for
from .forms import RegistrationForm
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

