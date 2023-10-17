import os
import pytest
from project import create_app, database
from project.models import Stock, User
from flask import current_app


@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()
    flask_app.extensions['mail'].suppress = True  # NEW!!

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():
            flask_app.logger.info('Creating database tables in test_client fixture...')

            # Create the database and the database table(s)
            database.create_all()

        yield testing_client  # this is where the testing happens!

        with flask_app.app_context():
            database.drop_all()

# config do test client lidando manualmente com adição e remoção do contexto

# scope='module' = a fixture será chamada uma vez por modulo de teste (arquivo)
# caso seja scope='function' a fixture sera executada e finalizada a cada função
#@pytest.fixture(scope='module')
#def test_client():
#    # Define a configuração de teste para a aplicação
#    # Assim, pacotes/módulos que se comportam de forma especifica em contextos
#    # de testes podem identificar o contexto
#    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
#    flask_app = create_app()
#    # Não envia de fato os emails | ambiente de teste
#    flask_app.extensions['mail'].suppress = True
#
#    testing_client = flask_app.test_client()
#
#    # normalmente o contexto é criado quando a aplicação está executando e 
#    # uma view function é chamada, mas não estamos chamando uma view functino
#    # então para podermos acessar o contexto, precisamos criar 
#    ctx = flask_app.app_context()
#    ctx.push()
#
#    # current_app é um proxy para o objeto global Application Context,
#    # que armazena dados da aplicação (configs etc)
#    current_app.logger.info('In the test_client() fixture...')
#    database.create_all()
#
#    # apos usar o contexto, removemos para limpeza da fixture
#    ctx.pop()
#
#    # retorna o controle para a função que chamou a fixture, injetando os objetos
#    # que foram criados na fixture
#    yield testing_client
#
#    # após o teste ser concluido, limpa o banco de testes
#    ctx = flask_app.app_context()
#    ctx.push()
#    database.drop_all()


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock


@pytest.fixture(scope='module')
def new_user():
    user = User('vitor@email.com', 'FlaskIsAwesome123')
    return user


@pytest.fixture(scope='module')
def register_default_user(test_client):
    test_client.post('/users/register',
                     data={'email': 'vitor@email.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)
    return


@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    test_client.post('/users/login',
                     data={'email': 'vitor@email.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)
    yield
    test_client.get('/users/logout', follow_redirects=True)

