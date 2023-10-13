from flask import Flask
from markupsafe import escape

# cria instância de uma app Flask, o nome da app equivale ao __name__
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'


@app.route('/about')
def about():
    return '<h2>About this application...</h2>'


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
