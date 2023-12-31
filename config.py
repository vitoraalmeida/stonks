import os
from datetime import timedelta


# determina o caminho absoluto para o diretório que contém este arquivo
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    # Key usada para assinar o cookie gerado pelo servidor.
    # Quando o cliente envia o cookie, o servidor usa a key para
    # verificar se o cookie foi modificado pelo cliente (tamper)
    # gerado com:
    # import secrets
    # secrets.token_bytes(32).hex()
    SECRET_KEY = os.getenv('SECRET_KEY', default='0d423c8b411e86a9b29ad8bd9907c3b11320e7222f3abb0f94dce8234f89edeb')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                         default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # emite sinais quando ocorrem modificações
    WTF_CSRF_ENABLED = True # proteção contra CSRF do Flask-WTF
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default='')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', default='')


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
                                         default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")
    # em ambiente de testes, o POST é feito diretamente, não atraves do form
    WTF_CSRF_ENABLED = False 
