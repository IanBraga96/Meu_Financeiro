from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa a instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Inicializa a instância do SQLAlchemy com a aplicação
    db.init_app(app)
    
    # Importa e registra as rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
