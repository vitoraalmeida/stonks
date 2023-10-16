"""
Este arquivo (test_models.py) contém os testes unitários para o arquivo models.py
"""

def test_new_stock(new_stock):
    """
    DADO um modelo Stock
    QUANDO um novo objeto Stock é criado
    ENTÃO checa se os campos ticket, numero de ações e preço de compra estão definidos corretamente
    """
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678


def test_new_user(new_user):
    """
    DADO um modelo de User
    QUANDO um novo objeto User for criado
    ENTÃO cheque se o email é valido e se o hash da senha não é igual à senha fornecida
    """
    assert new_user.email == 'vitor@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'
