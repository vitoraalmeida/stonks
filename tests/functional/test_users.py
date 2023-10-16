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

