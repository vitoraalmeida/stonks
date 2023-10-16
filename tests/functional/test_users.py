def test_get_registration_page(test_client):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/register' é requisitada (GET)
    ENTÃO checa se a resposta é válida
    """
    response = test_client.get('/users/register')
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert 'Registro de usuários' in response.data.decode()
    assert b'Email' in response.data
    assert b'Senha' in response.data


def test_valid_registration(test_client):
    """
    DATA uma aplicação configurada para testes
    QUANDO a rota '/users/register' for requisitada (POST)
    ENTÃO checa se a resposta é válida e o usuário foi registrado
    """
    response = test_client.post('/users/register',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsAwesome123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Obrigado por se registrar, vitor@email.com!' in response.data
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()


def test_invalid_registration(test_client):
    """
    DATA uma aplicação configurada para testes
    QUANDO a rota '/users/register' for requisitada (POST) com dados inválidos (faltando a senha)
    ENTÃO checa se a um erro foi enviado para o usuário
    """
    response = test_client.post('/users/register',
                                data={'email': 'vitor2@email.com',
                                      'password': ''},   # Empty field is not allowed!
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Obrigado por se registrar, vitor2@email.com!' not in response.data
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    print(response.data)
    assert b'[This field is required.]' in response.data


def test_duplicate_registration(test_client):
    """
    DATA uma aplicação configurada para testes
    QUANDO a rota '/users/register' for requisitada (POST) com um email já registrado
    ENTÃO checa se a um erro foi enviado para o usuário
    """
    test_client.post('/users/register',
                     data={'email': 'vitor3@email.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)
    response = test_client.post('/users/register',
                                data={'email': 'vitor3@email.com',   # email duplicado
                                      'password': 'FlaskIsStillGreat!'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Obrigado por se registrar, vitor3@email.com!' not in response.data
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert 'ERRO: dados inválidos foram usados para registro.' in response.data.decode()


def test_get_login_page(test_client):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/login' é requisitada (GET)
    ENTÃO checa se a resposta é válida
    """
    response = test_client.get('/users/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Senha' in response.data
    assert b'Login' in response.data


def test_valid_login_and_logout(test_client, register_default_user):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/login' é requisitada (POST) com credenciais válidas
    ENTÃO checa se a resposta é válida
    """
    response = test_client.post('/users/login',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsAwesome123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Bem vindo, vitor@email.com!' in response.data
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert 'Por favor, faça o login para acessar essa página.' not in response.data.decode()

    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/logout' é requisitada (GET) para um usuário logado
    ENTÃO checa se a resposta é válida
    """
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Até a próxima!' in response.data.decode()
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert 'Por favor, faça o login para acessar essa página.' not in response.data.decode()


def test_invalid_login(test_client, register_default_user):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/login' é requisitada (POST) com credenciais inválidas (senah errada)
    ENTÃO checa se uma mensagem de erro é retornada
    """
    response = test_client.post('/users/login',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsNotAwesome'},  # Incorrect!
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'ERRO! Credenciais inválidas.' in response.data.decode()


def test_valid_login_when_logged_in_already(test_client, log_in_default_user):
    """
    DADA uma aplicação Flask configurada para testes e com um usuário logado
    QUANDO a rota '/users/login' é requisitada (POST) com valores de credenciais para o usuário
    ENTÃO checa se um warning é retornado ao usuário (Já está logado)
    """
    response = test_client.post('/users/login',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsAwesome123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Você já está logado!' in response.data.decode()
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()


def test_invalid_logout(test_client):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/logout' é requisitada (POST)
    ENTÃO checa se um erro 405 é retornado
    """
    response = test_client.post('/users/logout', follow_redirects=True)
    assert response.status_code == 405
    assert 'Até a próxima!' not in response.data.decode()
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    print(response.data)
    assert 'Method Not Allowed' in response.data.decode()


def test_invalid_logout_not_logged_in(test_client):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/users/logout' é requisitada (GET) quando o usuário não está logado
    ENTÃO checa se o usuário é redirecionado para a página de login
    """
    test_client.get('/users/logout', follow_redirects=True)  # Double-check that there are no logged in users!
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Até a próxima!' not in response.data.decode()
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert b'Login' in response.data
    assert 'Por favor, faça o login para acessar essa página.' not in response.data.decode()

