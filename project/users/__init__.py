"""
O Blueprint users lida com gerenciamento de usuários para essa aplicação.
Especificamente, esse Blueprint permite registro de novos usuários, login e 
logout na aplicação
"""
from flask import Blueprint

users_blueprint = Blueprint('users', __name__, template_folder='templates')

from . import routes


