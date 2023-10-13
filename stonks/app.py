import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask.logging import default_handler # para remover o default
from markupsafe import escape
from pydantic import BaseModel, validator, ValidationError


# cria instância de uma app Flask, o nome da app equivale ao __name__
app = Flask(__name__)
# remove o logger default. Assim a aplicação não mostra logs no terminal
#app.logger.removeHandler(default_handler)

# sem rotação de logs
# log_file_handler = logging.FileHandler('flask-stonks.log')

# quando o arquivo chega no tamanho determinado, move o arquivo para
# arquivo.1 e outro arquivo com o mesmo nome original é criado
# de forma que o arquivo com o nome original é sempre o mais recente
log_file_handler = RotatingFileHandler(
    'flask-stonks.log',
    maxBytes=16384, # tamanho máxima
    backupCount=20  # máximo de cópias
)
log_file_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]'
)
log_file_handler.setFormatter(log_file_formatter)
# Nível mínimo de log a ser mostrado
# É indicado que quanto mais cedo no ciclo de desenvolvimento
# mais informações sejam logadas, mas na medida em que avançamos na maturidade
# da aplicação, reduzimos a quantidade e criticidade dos logs
# DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
# também podemos definir o nível de log com base no ambiente
# log_level = logging.DEBUG if DEBUG else logging.INFO
log_file_handler.setLevel(logging.INFO)
app.logger.addHandler(log_file_handler)

app.logger.info('Starting the Stonks App')

# Key usada para assinar o cookie gerado pelo servidor.
# Quando o cliente envia o cookie, o servidor usa a key para
# verificar se o cookie foi modificado pelo cliente (tamper)
# gerado com:
# import secrets
# secrets.token_bytes(32).hex()
app.secret_key = '0d423c8b411e86a9b29ad8bd9907c3b11320e7222f3abb0f94dce8234f89edeb'


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


@app.route('/')
def index():
    # renderiza o template html passado, executando as operações
    # presentes no template
    return render_template('index.html')


@app.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    # permite passar dados que serão processados durante a renderização
    return render_template('about.html', developer='Vitor')


# permite receber o valor passado na url como uma variável que é recebida na
# função
@app.route('/hello/<message>')
def hello_message(message):
    return f'<h1>Welcome {escape(message)}!</h1>'


# permite definir um tipo esperado na variável. Caso outros tipo seja fornecido
# O flask não interpreta como uma rota existente
# tipos: string, int, path, uuid
@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog post #{post_id}...</h1>'


# /stocks != /stocks/
# Convencionalmente uma barra no fim indica que o 
# recurso agrupa outros
# ex.: /stocks/ -> retorna lista de stocks
#      /sotcks/1 -> retorna a stock com id 1 etc
@app.route('/stocks/')
def list_stocks():
    # dados da sessão do flask ficam disponíveis em templates
    # browsers diferentes tem sessões diferentes
    return render_template('stocks.html')


#                        permite lidar com diferentes métodos na mesma rota
@app.route('/add_stock', methods=['GET', 'POST'])
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
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            # adiciona flash messagem que será mostrada na próxima requisição
            flash(f'Nova ação adicionada ({stock_data.stock_symbol})', 'success')
            app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")

            return redirect(url_for('list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')
