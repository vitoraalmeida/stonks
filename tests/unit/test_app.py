from pydantic import ValidationError
import pytest

"""
Este arquivo (test_app.py) contém os testes unitários para a aplicação
"""
from project.stocks.routes import StockModel

def test_validate_stock_data_nominal():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados válidos são passados
    ENTÃO checa se a validação é bem sucedida
    """
    stock_data = StockModel(
        stock_symbol='SBUX',
        number_of_shares='100',
        purchase_price='45.67'
    )
    assert stock_data.stock_symbol == 'SBUX'
    assert stock_data.number_of_shares == 100
    assert stock_data.purchase_price == 45.67


def test_validate_stock_data_invalid_stock_symbol():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados inválidos são passados (stock_symbol)
    ENTÃO checa se a validação invoca um ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol='SBUX123',  # Invalid!
            number_of_shares='100',
            purchase_price='45.67'
        )


def test_validate_stock_data_invalid_number_of_shares():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados inválidos são passados (number_of_shares)
    ENTÃO checa se a validação invoca um ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100.1231',  # Invalid!
            purchase_price='45.67'
        )


def test_validate_stock_data_invalid_purchase_price():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados inválidos são passados (purchase_price)
    ENTÃO checa se a validação invoca um ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100',
            purchase_price='45,67'  # Invalid!
        )


def test_validate_stock_data_missing_inputs():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados inválidos são passados (sem input)
    ENTÃO checa se a validação invoca um ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel()  # Missing input data!


def test_validate_stock_data_missing_purchase_price():
    """
    DADA uma classe helper para validar dados de formulários
    QUANDO dados inválidos são passados (sem purchase_price)
    ENTÃO checa se a validação invoca um ValidationError
    """
    with pytest.raises(ValidationError):
        StockModel(
            stock_symbol='SBUX',
            number_of_shares='100',
            # Missing purchase_price!
        )

