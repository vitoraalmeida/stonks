from project import database
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column


class Stock(database.Model):
    """
    Classe que representa uma ação comprada num portifólio

    Os seguintes atributos de uma ação estão armazenados na tabela:
        stock symbol (string) = ticket da ação
        number of shares (integer) = número de ações
        purchased price (integer) = preço de compra

    Nota: os preços de compra são definidos como inteiros para evitar problemas
          com ponto flutuante. Valores são multiplicados por 100 ao salvar
            R$ 24.10 -> 2410
            R$ 100.00 -> 10000
    """
    
    # define o nome da tabela que será criada
    __tablename__ = 'stocks'

    # mapped_column é o objeto que mapeia o tipo do python ao tipo do banco
    id = mapped_column(Integer(), primary_key=True)
    stock_symbol = mapped_column(String())
    number_of_shares = mapped_column(Integer())
    purchase_price = mapped_column(Integer())

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} ações compradas por R$ {self.purchase_price / 100}'
