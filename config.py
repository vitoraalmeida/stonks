import os


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


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

