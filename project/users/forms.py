from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


# Herdar de FlaskForm adiciona a proteção contra CSRF
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=120)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=100)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Manter logado')
    submit = SubmitField('Login')
