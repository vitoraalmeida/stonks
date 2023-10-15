from . import stocks_blueprint

from flask import current_app, render_template, request, session, flash, redirect, url_for
from pydantic import BaseModel, validator, ValidationError
from project import database
from project.models import Stock


# quando um StockModel é criado passando os seus elementos, ocorre a tentativa
# de converter cada campo ao tipo definido nos atributos
class StockModel(BaseModel):
    """ Classe para fazer o parsing de uma nova ação a partir de um form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    # validador customizado
    @validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()


# /stocks != /stocks/
# Convencionalmente uma barra no fim indica que o 
# recurso agrupa outros
# ex.: /stocks/ -> retorna lista de stocks
#      /sotcks/1 -> retorna a stock com id 1 etc
@stocks_blueprint.route('/stocks/')
def list_stocks():
    query = database.select(Stock).order_by(Stock.id)
    # execute() retorna um iterável (Result)
    # scalars().all() consome o iterável e retorna a lista de objetos
    # all() converte o tipo result.ScalarResult em uma lista
    # o tipo ScalarResult é um iterável, quando consumimos uma vez, o elemento
    # é excluído
    stocks = database.session.execute(query).scalars().all()
    # dados da sessão do flask ficam disponíveis em templates
    # browsers diferentes tem sessões diferentes
    return render_template('stocks/stocks.html', stocks=stocks)


#                        permite lidar com diferentes métodos na mesma rota
@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # dados de formulários são disponibilizados como um dict
        # as chaves são as mesmas definidas no atributo name do form html
        for key, value in request.form.items():
            print(f'{key}: {value}')

        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # armazena dados na sessão
            # sessões permitem armazenar dados de forma persisitente sobre
            # multiplos requests. Idealizado para infos (não sensíveis)
            # de usuários (como tokens gerados ao fazer o login)
            # armazenados em cookies criptograficamente assinados
            # não criptografados!
            # session['stock_symbol'] = stock_data.stock_symbol
            # session['number_of_shares'] = stock_data.number_of_shares
            # session['purchase_price'] = stock_data.purchase_price
            # adiciona flash messagem que será mostrada na próxima requisição


            new_stock = Stock(
                stock_data.stock_symbol,
                stock_data.number_of_shares,
                stock_data.purchase_price
            )
            database.session.add(new_stock)
            database.session.commit()

            flash(f'Nova ação adicionada ({stock_data.stock_symbol})', 'success')
            current_app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")

            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('stocks/add_stock.html')

