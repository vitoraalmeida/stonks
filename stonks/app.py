from flask import Flask, render_template, request
from markupsafe import escape
from pydantic import BaseModel, validator, ValidationError


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

# cria instância de uma app Flask, o nome da app equivale ao __name__
app = Flask(__name__)

@app.route('/')
def index():
    # renderiza o template html passado, executando as operações
    # presentes no template
    return render_template('index.html')


@app.route('/about')
def about():
    # permite passar dados que serão processados durante a renderização
    return render_template('about.html', developer='Vitor')


# /stocks != /stocks/
# Convencionalmente uma barra no fim indica que o 
# recurso agrupa outros
# ex.: /stocks/ -> retorna lista de stocks
#      /sotcks/1 -> retorna a stock com id 1 etc
@app.route('/stocks/')
def stocks():
    return '<h2>Stock list...</h2>'


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
        except ValidationError as e:
            print(e)

    return render_template('add_stock.html')
