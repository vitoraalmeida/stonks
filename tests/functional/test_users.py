from project import mail


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
    ENTÃO checa se a resposta é válida, o usuário foi registrado e se um email foi enfileirado para ser enviado
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/users/register',
                                    data={'email': 'vitor@email.com',
                                          'password': 'FlaskIsAwesome123'},
                                    follow_redirects=True)
        assert response.status_code == 200
        assert b'Obrigado por se registrar, vitor@email.com!' in response.data
        assert 'Stonks - Portifólio de investimentos' in response.data.decode()
        assert len(outbox) == 1
        assert outbox[0].subject == 'Registro - Stonks - Portifólio de investimentos'
        assert outbox[0].sender == 'almeidavitor.dev@gmail.com'
        assert outbox[0].recipients[0] == 'vitor@email.com'


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


def test_user_profile_not_logged_in(test_client):
    """
    DADA uma aplicação Flask configurada para testes com usuário logado
    QUANDO a rota '/users/profile' for requisitada (GET) e o usuário não estiver logado
    ENTÃO checa se o usuário é redirecionado para a pagina de login
    """
    response = test_client.get('/users/profile', follow_redirects=True)
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    print(response.data.decode())
    assert 'Perfil do Usuário' not in response.data.decode()
    assert b'Email: vitor@email.com' not in response.data
    assert 'Por favor, faça o login para acessar essa página.' not in response.data.decode()


def test_user_profile_logged_in(test_client, log_in_default_user):
    """
    DADA uma aplicação Flask configurada para testes com usuário logado
    QUANDO a rota '/users/profile' for requisitada (GET) 
    ENTÃO checa se o perfil para o usuário logado é mostrado
    """
    response = test_client.get('/users/profile')
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert 'Perfil do Usuário' in response.data.decode()
    assert b'Email: vitor@email.com' in response.data


def test_navigation_bar_logged_in(test_client, log_in_default_user):
    """
    DADA uma aplicação Flask configurada para testes com usuário logado
    QUANDO a rota '/' é requisitada (GET)
    ENTÃO checa se os links 'Listar ações', 'Adicionar ação', 'Meu perfil' e 'Logout' estão presentes
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert b'Bem vindo ao' in response.data
    assert b'Stonks!' in response.data
    assert 'Listar ações' in response.data.decode()
    assert 'Adicionar ação' in response.data.decode()
    assert b'Meu perfil' in response.data
    assert b'Logout' in response.data
    assert b'Criar conta' not in response.data
    assert b'Login' not in response.data


def test_navigation_bar_not_logged_in(test_client):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota '/' é requisitada (GET) e o usuário não está logado
    ENTÃO checa se os links 'Criar conta' e 'Login' estão presentes
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert b'Bem vindo ao' in response.data
    assert b'Stonks!' in response.data
    assert b'Criar conta' in response.data
    assert b'Login' in response.data
    assert 'Listar ações' not in response.data.decode()
    assert 'Adicionar ação' not in response.data.decode()
    assert b'Meu perfil' not in response.data
    assert b'Logout' not in response.data


def test_login_with_next_valid_path(test_client, register_default_user):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota 'users/login?next=%2Fusers%2Fprofile' for requisitada (POST) com credenciais válidas
    ENTÃO checa se o usuário é redirecionado para o perfil do usuário
    """
    response = test_client.post('users/login?next=%2Fusers%2Fprofile',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsAwesome123'},
                                follow_redirects=True)
    print(response.data.decode())
    assert response.status_code == 200
    assert 'Stonks - Portifólio de investimentos' in response.data.decode()
    assert b'Meu perfil' in response.data
    assert b'Bem vindo, vitor@email.com!' in response.data

    test_client.get('/users/logout', follow_redirects=True)


def test_login_with_next_invalid_path(test_client, register_default_user):
    """
    DADA uma aplicação Flask configurada para testes
    QUANDO a rota 'users/login?next=http://www.badsite.com' for requisitada (POST) com credenciais válidas
    ENTÃO checa se um erro 400 (Bad Request) e retornado
    """
    response = test_client.post('users/login?next=http://www.badsite.com',
                                data={'email': 'vitor@email.com',
                                      'password': 'FlaskIsAwesome123'},
                                follow_redirects=True)
    assert response.status_code == 400
    assert b'Meu perfil' not in response.data
    assert b'Bem vindo, vitor@email.com!' not in response.data

