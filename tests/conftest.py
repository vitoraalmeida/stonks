import os
import pytest
from project import create_app, database
from project.models import Stock, User
from flask import current_app


# scope='module' = a fixture será chamada uma vez por modulo de teste (arquivo)
# caso seja scope='function' a fixture sera executada e finalizada a cada função
@pytest.fixture(scope='module')
def test_client():
    # Define a configuração de teste para a aplicação
    # Assim, pacotes/módulos que se comportam de forma especifica em contextos
    # de testes podem identificar o contexto
    #os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    testing_client = flask_app.test_client()

    # normalmente o contexto é criado quando a aplicação está executando e 
    # uma view function é chamada, mas não estamos chamando uma view functino
    # então para podermos acessar o contexto, precisamos criar 
    ctx = flask_app.app_context()
    ctx.push()

    # current_app é um proxy para o objeto global Application Context,
    # que armazena dados da aplicação (configs etc)
    current_app.logger.info('In the test_client() fixture...')
    database.create_all()

    # apos usar o contexto, removemos para limpeza da fixture
    ctx.pop()

    # retorna o controle para a função que chamou a fixture, injetando os objetos
    # que foram criados na fixture
    yield testing_client

    # após o teste ser concluido, limpa o banco de testes
    ctx = flask_app.app_context()
    ctx.push()
    database.drop_all()


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock


@pytest.fixture(scope='module')
def new_user():
    user = User('vitor@email.com', 'FlaskIsAwesome123')
    return user
