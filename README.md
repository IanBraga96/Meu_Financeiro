# Meu_Financeiro

Este é um aplicativo web bem simples de controle financeiro desenvolvido com Python e Flask. Ele permite que os usuários gerenciem suas finanças, incluindo o registro de despesas, receitas, tipos de despesas e receitas, além de manter um histórico de transações.

A intenção da criação é de uma necessidade pessoal para organizar os gastos.
Continua em fase de testes e desenvolvimento.

---
**Atualizações de Código:**

Recentemente, criei um novo branch para o projeto no GitHub:
- O branch antigo foi renomeado para `master` e contém a primeira versão do meu projeto.
- Um novo branch `develop` foi criado para continuar o desenvolvimento e postar novas atualizações.

Você pode encontrar mais detalhes sobre cada versão nas respectivas branches do GitHub.

---
### Disponivel para teste
Acesse o aplicativo [aqui](https://ianbraga.pythonanywhere.com/login).

---
## Últimas atualizações:

- Correção no banco de dados para separação correta das informações por usuário.
- Implementação de gráficos para visualização de despesas ao longo do tempo. Posteriormente alterei o gráfico para o tipo doughnut.
- Adição de página de configuração para alteração de dados cadastrais e tipos de despesas/receitas.
- Melhorias nas páginas com adição de cabeçalho e rodapé.
- Implementação de modo escuro.
- Remodelação completa da estrutura do projeto para facilitar manutenção.

---
## Próximas atualizações

- Remodelação da Dashboard - Melhorar a experiência de uso da dashboard, tornando-a mais intuitiva e amigável.
- Adicionar reCAPTCHA no login

---
## Funcionalidades

- Registro e login de usuário.
- Gerenciamento de carteira financeira com visualização de gráficos de receitas/despesas.
- Cadastro e exclusão de despesas, receitas, tipos de despesas e tipos de receitas.
- Visualização do histórico de transações.

---
## Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Werkzeug
- HTML/CSS
- SQLite
- JavaScript

---
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

---
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

### Configurações

Na página de configuração, você pode:

- Alterar dados de login
- Excluir despesas, receitas, tipos de despesas e tipos de receitas.

---
## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---
## Contato

- **Nome:** Ian Braga
- **E-mail:** contatoianbraga@gmail.com
- **GitHub:** <https://github.com/IanBraga96>


