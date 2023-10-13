"""
Este arquivo (test_stocks.py) contém os testes funcionais para o arquivo app.py
"""
from stonks.app import app


def test_index_page():
    """
    DADA uma aplicação Flask 
    QUANDO a página '/' for requisitada (GET)
    ENTÃO checa se a resposta é valida
    """
    # flask provê um cliente http para facilitar os testes
    # que usa uma versão para testes da nossa aplicação 
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert 'Stonks - Portifólio de investimentos' in response.data.decode()
        assert b'Bem vindo ao Stonks!' in response.data
        assert 'Monitore e gerencie seu portifólio de investimentos' in response.data.decode()


def test_about_page():
    """
    DADA uma aplicação Flask 
    QUANDO a página '/about' for requisitada (GET)
    ENTÃO checa se a resposta é valida
    """
    with app.test_client() as client:
        response = client.get('/about')
        assert response.status_code == 200
        assert 'Stonks - Portifólio de investimentos' in response.data.decode()
        assert b'Sobre' in response.data
        assert 'Essa aplicação foi feita utilizando o framework web Flask' in response.data.decode()
        assert b'Desenvolvido por Vitor' in response.data


def test_get_add_stock_page():
    """
    DADA uma aplicação Flask 
    Quando a página '/add_stock' for requisitada (GET)
    ENTÃO checa se a resposta é valida
    """
    with app.test_client() as client:
        response = client.get('/add_stock')
        assert response.status_code == 200
        assert 'Stonks - Portifólio de investimentos' in response.data.decode()
        assert 'Adicione uma ação' in response.data.decode()
        assert 'Ticket: <em>(obrigatório, de 1-5 letras maiúsculas</em>' in response.data.decode()
        assert 'Número de ações: <em>(obrigatório)</em>' in response.data.decode()
        assert 'Preço de compra (R$):' in response.data.decode()


def test_post_add_stock_page():
    """
    DADA uma aplicação Flask 
    QUANDO a página '/add_stock' for requisitada (POST)
    ENTÃO checa se o usuário é redirecionado para a página '/stocks'
    """

    with app.test_client() as client:
        response = client.post(
            '/add_stock',
            data={
                'stock_symbol': 'AAPL',
                'number_of_shares': '23',
                'purchase_price': '432.17'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert 'Lista de ações' in response.data.decode()
        assert b'Ticket' in response.data
        assert 'Número de ações' in response.data.decode()
        assert 'Preço de compra' in response.data.decode()
        assert b'AAPL' in response.data
        assert b'23' in response.data
        assert b'432.17' in response.data

