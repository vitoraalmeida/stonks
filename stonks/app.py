from flask import Flask

# cria instância de uma app Flask, o nome da app equivale ao __name__
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'
