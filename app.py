#imports
from flask import Flask, request, render_template, redirect, url_for, flash, session #Framework para criar aplicações web em Python.
from flask_sqlalchemy import SQLAlchemy #ORM para interagir com bancos de dados.
from werkzeug.security import generate_password_hash, check_password_hash #Funções para criptografar e verificar senhas.
from datetime import datetime #Módulo para trabalhar com datas e horas.
import os #Módulo para interagir com o sistema operacional.


#Configuração do Flask e banco de dados SQLAlchemy
app = Flask(__name__) #Cria uma instância do Flask.
app.config.from_object('config.Config') # Configura o aplicativo Flask com base em um arquivo de configuração.
db = SQLAlchemy(app) # Cria uma instância do SQLAlchemy e associa ao aplicativo Flask.


#Definição de modelos de banco de dados:
#Define quatro modelos de banco de dados: User, Wallet, Expense, Revenue, ExpenseType,
#RevenueType, representando usuários, carteiras, despesas, receitas, tipos de despesa
#e tipos de receita, respectivamente. Cada modelo é uma classe que herda da classe db.Model do SQLAlchemy.
class User(db.Model):
    # Modelo de usuário com campos para fullname, username, email e password
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Wallet(db.Model):
    # Modelo de carteira
    id = db.Column(db.Integer, primary_key=True)
    total_value = db.Column(db.Float, nullable=False)
    total_expenses = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    # Modelo de despesa
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Revenue(db.Model):
    # Modelo de receitas
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revenue_type_id = db.Column(db.Integer, db.ForeignKey('revenue_type.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExpenseType(db.Model):
    # Modelo de tipos de despesa
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class RevenueType(db.Model):
    # Modelo de tipos de receitas
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


#Define várias rotas para o Flask
#@app.route('/'): Rota principal que redireciona para o login.
#@app.route('/register', methods=['GET', 'POST']): Rota para registrar um novo usuário.
#@app.route('/login', methods=['GET', 'POST']): Rota para fazer login.
#@app.route('/dashboard'): Rota para o painel de controle, acessível apenas se o usuário estiver logado.
#@app.route('/add_wallet', methods=['POST']): Rota para adicionar ou atualizar informações da carteira.
#@app.route('/add_expense', methods=['POST']): Rota para adicionar uma nova despesa.
#@app.route('/add_revenue', methods=['POST']): Rota para adicionar uma nova receita.
#@app.route('/add_expense_type', methods=['POST']): Rota para adicionar um novo tipo de despesa.
#@app.route('/add_revenue_type', methods=['POST']): Rota para adicionar um novo tipo de receita.
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(fullname=fullname, username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registrado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar usuário. Tente novamente.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    expense_types = ExpenseType.query.filter_by(user_id=user_id).all()
    revenue_types = RevenueType.query.filter_by(user_id=user_id).all()

    total_revenue = db.session.query(db.func.sum(Revenue.amount)).filter(Revenue.user_id == user_id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0
    total_value = total_revenue - total_expense
    
    # Calcular dados para o gráfico
    expense_types = ExpenseType.query.filter_by(user_id=user_id).all()
    revenue_types = RevenueType.query.filter_by(user_id=user_id).all()
    
    expense_data = {expense_type.name: 0 for expense_type in expense_types}
    revenue_data = {revenue_type.name: 0 for revenue_type in revenue_types}
    
    for expense in Expense.query.filter_by(user_id=user_id).all():
        expense_type = ExpenseType.query.get(expense.expense_type_id)
        expense_data[expense_type.name] += expense.amount
        
    for revenue in Revenue.query.filter_by(user_id=user_id).all():
        revenue_type = RevenueType.query.get(revenue.revenue_type_id)
        revenue_data[revenue_type.name] += revenue.amount

    labels = list(expense_data.keys()) + list(revenue_data.keys())
    data = list(expense_data.values()) + list(revenue_data.values())

    expenses = Expense.query.filter_by(user_id=user_id).all()
    revenues = Revenue.query.filter_by(user_id=user_id).all()
    
    return render_template('dashboard.html', wallet=wallet, total_value=total_value,
                           total_expense=total_expense, labels=labels, data=data, expense_types=expense_types,
                           revenue_types=revenue_types, expenses=expenses, revenues=revenues, user_id=user_id)

@app.route('/add_wallet', methods=['POST'])
def add_wallet():
    total_value = request.form.get('total_value')
    total_expenses = request.form.get('total_expenses')
    user_id = session['user_id']
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if wallet:
        wallet.total_value = total_value
        wallet.total_expenses = total_expenses
    else:
        new_wallet = Wallet(total_value=total_value, total_expenses=total_expenses, user_id=user_id)
        db.session.add(new_wallet)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    expense_type_id = request.form.get('expense_type_id')

    new_expense = Expense(amount=amount, description=description, user_id=user_id, expense_type_id=expense_type_id)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_revenue', methods=['POST'])
def add_revenue():
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    amount = request.form.get('amount')
    description = request.form.get('description')
    revenue_type_id = request.form.get('revenue_type_id')
    new_revenue = Revenue(amount=amount, description=description, revenue_type_id=revenue_type_id, user_id=user_id)
    db.session.add(new_revenue)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_expense_type', methods=['POST'])
def add_expense_type():
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    name = request.form.get('name')
    new_expense_type = ExpenseType(name=name, user_id=user_id)
    db.session.add(new_expense_type)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_revenue_type', methods=['POST'])
def add_revenue_type():
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    name = request.form.get('name')
    new_revenue_type = RevenueType(name=name, user_id=user_id)
    db.session.add(new_revenue_type)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/config', methods=['GET', 'POST'])
def config():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    expense_types = ExpenseType.query.all()
    revenue_types = RevenueType.query.all()

    if request.method == 'POST':
        # Atualizar dados do usuário
        user.fullname = request.form.get('fullname')
        user.email = request.form.get('email')
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'uccess')
    
    return render_template('config.html', user=user, expense_types=expense_types, revenue_types=revenue_types)

@app.route('/delete_expense_type/<int:id>')
def delete_expense_type(id):
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma despesa.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    expense = Expense.query.get(id)

    if expense is None or expense.user_id!= user_id:
        flash('Você não tem permissão para excluir essa despesa.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(expense)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'uccess')
    return redirect(url_for('dashboard'))

@app.route('/delete_revenue_type/<int:id>')
def delete_revenue_type(id):
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma receita.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    revenue = Revenue.query.get(id)

    if revenue is None or revenue.user_id!= user_id:
        flash('Você não tem permissão para excluir essa receita.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(revenue)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'uccess')
    return redirect(url_for('dashboard'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    
    if not check_password_hash(user.password, current_password):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('config'))
    
    if new_password != confirm_new_password:
        flash('As novas senhas não coincidem.', 'danger')
        return redirect(url_for('config'))
    
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('config'))



#Debug flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all() #Cria as tabelas no banco de dados.
    app.run(debug=True) #Executa o Flask em modo de depuração.
