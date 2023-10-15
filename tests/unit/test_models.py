"""
Este arquivo (test_models.py) contém os testes unitários para o arquivo models.py
"""

def test_new_stock(new_stock):
    """
    DATA um modelo Stock
    QUANDO um novo objeto Stock é criado
    ENTÃO checa se os campos ticket, numero de ações e preço de compra estão definidos corretamente
    """
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678

