# Meu_Financeiro

Este é um aplicativo web bem simples de controle financeiro desenvolvido com Python e Flask. Ele permite que os usuários gerenciem suas finanças, incluindo o registro de despesas, receitas, tipos de despesas e receitas, além de manter um histórico de transações.

A intenção da criação é de uma necessidade pessoal para organizar os gastos.
Ainda está em fase de testes e desenvolvimento.

## Próximas atualizações

- Remodelação da Dashboard - Melhorar a experiência de uso da dashboard, tornando-a mais intuitiva e amigável.
- Gráficos de Despesas - Implementar gráficos para visualização das despesas ao longo do tempo
- Disponibilização Online - Hospedar o aplicativo online para uso externo, Garantir que seja responsivo e funcione bem em smartphones e tablets.

## Funcionalidades

- Registro de Usuário
- Login de Usuário
- Gerenciamento de Carteira Financeira
- Cadastro de Despesas
- Cadastro de Receitas
- Cadastro de Tipos de Despesas
- Cadastro de Tipos de Receitas
- Visualização do Histórico de Transações

## Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Werkzeug
- HTML/CSS
- SQLite

## Instalação

### Pré-requisitos

- Python 3.x instalado
- Virtualenv (opcional, mas recomendado)

### Passos para instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/IanBraga96/Meu_Financeiro
    cd seu-repositorio
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute a aplicação:
    ```bash
    python app.py
    ```

5. Abra o navegador e acesse `http://127.0.0.1:5000`.

## Estrutura do Projeto

Claro! Um README bem estruturado ajuda muito na hora de compartilhar o projeto no GitHub. Aqui está um exemplo de README que você pode usar e ajustar conforme necessário:

markdown
Copiar código
# Controle Financeiro

Este é um aplicativo web de controle financeiro desenvolvido com Flask. Ele permite que os usuários gerenciem suas finanças, incluindo o registro de despesas, receitas, tipos de despesas e receitas, além de manter um histórico de transações.

## Funcionalidades

- Registro de Usuário
- Login de Usuário
- Gerenciamento de Carteira Financeira
- Cadastro de Despesas
- Cadastro de Receitas
- Cadastro de Tipos de Despesas
- Cadastro de Tipos de Receitas
- Visualização do Histórico de Transações

## Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Werkzeug
- HTML/CSS
- SQLite

## Instalação

### Pré-requisitos

- Python 3.x instalado
- Virtualenv (opcional, mas recomendado)

### Passos para instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute a aplicação:
    ```bash
    python app.py
    ```

5. Abra o navegador e acesse `http://127.0.0.1:5000`.

## Estrutura do Projeto
.
├── app.py
├── config.py
├── requirements.txt
├── templates
│ ├── dashboard.html
│ ├── login.html
│ ├── register.html
└── README.md


## Uso

### Registro de Usuário

1. Acesse a página de registro em `/register`.
2. Preencha os campos de nome completo, nome de usuário, e-mail e senha.
3. Clique no botão "Registrar".

### Login de Usuário

1. Acesse a página de login em `/login`.
2. Preencha os campos de nome de usuário e senha.
3. Clique no botão "Entrar".

### Dashboard

Após o login, você será redirecionado para o painel de controle, onde poderá:

- Adicionar o valor total da carteira e o total de despesas.
- Cadastrar novas despesas e receitas.
- Cadastrar novos tipos de despesas e receitas.
- Visualizar o histórico de transações.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.


## Contato

- **Nome:** Ian Braga
- **E-mail:** contatoianbraga@gmail.com
- **GitHub:** https://github.com/IanBraga96


