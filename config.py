import os


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


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

