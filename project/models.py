import flask_login
from datetime import datetime
from project import database
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(flask_login.UserMixin, database.Model):
    """
    Classe que representa um usuário da aplicação

    Os seguintes atributos de um usuário são armazenados na tabela:
        * email
        * hashed_password
        * registered_on
        *email_confirmation_sent_on
        * email_confirmed
        * email_confirmed_on

    Nunca armazene a senha em texto claro
    """
    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True)
    email = mapped_column(String(), unique=True)
    password_hashed = mapped_column(String(128))
    registered_on = mapped_column(DateTime())
    email_confirmation_sent_on = mapped_column(DateTime())
    email_confirmed = mapped_column(Boolean(), default=False)
    email_confirmed_on = mapped_column(DateTime())

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    # staticmethods indicam que o método não depende de alguma variável de instância
    # métodos que começam com _ são convencionalmente privados
    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'
