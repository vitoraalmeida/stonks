from flask import Flask, flash, render_template
from flask.logging import default_handler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from logging.handlers import RotatingFileHandler
import logging
from markupsafe import escape
import os


#######################
#### Configuration ####
#######################

# Create a naming convention for the database tables
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# cria instância da extensão no contexto global, mas ainda não foi adicionado na aplicação
database = SQLAlchemy(metadata=metadata)
db_migration = Migrate()
csrf_protection = CSRFProtect()


########################
### Helper Functions ###
########################


def create_app():
    # cria instância de uma app Flask, o nome da app equivale ao __name__
    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)
    initialize_extensions(app)
    register_blueprints(app)
    register_global_routes(app)
    register_error_pages(app)
    configure_logging(app)

    return app


def register_blueprints(app):
    # importa blueprints evitando circular imports
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint

    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')


def initialize_extensions(app):
    # faz o bind da extensão à aplicação
    database.init_app(app)
    db_migration.init_app(app, database)
    csrf_protection.init_app(app)


def configure_logging(app):
    # remove o logger default. Assim a aplicação não mostra logs no terminal
    #app.logger.removeHandler(default_handler)

    # sem rotação de logs
    # log_file_handler = logging.FileHandler('flask-stonks.log')

    # quando o arquivo chega no tamanho determinado, move o arquivo para
    # arquivo.1 e outro arquivo com o mesmo nome original é criado
    # de forma que o arquivo com o nome original é sempre o mais recente
    log_file_handler = RotatingFileHandler(
        'instance/flask-stonks.log',
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


def register_global_routes(app):
    # rotas globais / não agrupadas num blueprint
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


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405


