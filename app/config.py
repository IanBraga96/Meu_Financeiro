class Config:
    # Senha
    SECRET_KEY = 'senha_secreta_do_ian'

    # URI do banco de dados, nesse caso um banco de dados SQLite chamado site.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Desativa o rastreamento de modificações do banco de dados, melhorando o desempenho
    SQLALCHEMY_TRACK_MODIFICATIONS = False
