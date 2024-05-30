from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_value = db.Column(db.Float, nullable=False)
    total_expenses = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    revenue_type_id = db.Column(db.Integer, db.ForeignKey('revenue_type.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExpenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class RevenueType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

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
    
    wallet = Wallet.query.first()
    expenses = Expense.query.all()
    revenues = Revenue.query.all()
    expense_types = ExpenseType.query.all()
    revenue_types = RevenueType.query.all()
    return render_template('dashboard.html', wallet=wallet, expenses=expenses, revenues=revenues, expense_types=expense_types, revenue_types=revenue_types)

@app.route('/add_wallet', methods=['POST'])
def add_wallet():
    total_value = request.form.get('total_value')
    total_expenses = request.form.get('total_expenses')
    new_wallet = Wallet(total_value=total_value, total_expenses=total_expenses)
    db.session.add(new_wallet)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = request.form.get('amount')
    description = request.form.get('description')
    expense_type_id = request.form.get('expense_type_id')
    new_expense = Expense(amount=amount, description=description, expense_type_id=expense_type_id)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_revenue', methods=['POST'])
def add_revenue():
    amount = request.form.get('amount')
    description = request.form.get('description')
    revenue_type_id = request.form.get('revenue_type_id')
    new_revenue = Revenue(amount=amount, description=description, revenue_type_id=revenue_type_id)
    db.session.add(new_revenue)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_expense_type', methods=['POST'])
def add_expense_type():
    name = request.form.get('name')
    new_expense_type = ExpenseType(name=name)
    db.session.add(new_expense_type)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_revenue_type', methods=['POST'])
def add_revenue_type():
    name = request.form.get('name')
    new_revenue_type = RevenueType(name=name)
    db.session.add(new_revenue_type)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
