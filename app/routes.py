from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    from .models import User
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(fullname=fullname, username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registrado com sucesso! Faça login.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar usuário. Tente novamente.', 'danger')
            return redirect(url_for('main.register'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    from .models import User
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    from .models import Wallet, ExpenseType, RevenueType, Expense, Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    user_id = session['user_id']
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    expense_types = ExpenseType.query.filter_by(user_id=user_id).all()
    revenue_types = RevenueType.query.filter_by(user_id=user_id).all()

    total_revenue = db.session.query(db.func.sum(Revenue.amount)).filter(Revenue.user_id == user_id).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0

    # Preparar dados de despesas por tipo
    expense_data = {expense_type.name: 0 for expense_type in expense_types}
    for expense in Expense.query.filter_by(user_id=user_id).all():
        expense_type = ExpenseType.query.get(expense.expense_type_id)
        expense_data[expense_type.name] += expense.amount

    # Preparar os labels e valores para o gráfico
    labels = list(expense_data.keys())
    data = list(expense_data.values())

    # Adicionar valor disponível para gastar, se houver
    if total_revenue > total_expense:
        labels.append('Disponível para Gasto')
        data.append(total_revenue - total_expense)

    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    return render_template('dashboard.html', wallet=wallet, total_revenue=total_revenue,
                           total_expense=total_expense, labels=labels, data=data, expense_types=expense_types,
                           revenue_types=revenue_types, labels_json=labels_json, data_json=data_json)

@main.route('/add_wallet', methods=['POST'])
def add_wallet():
    from .models import Wallet
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
    return redirect(url_for('main.dashboard'))

@main.route('/add_expense', methods=['POST'])
def add_expense():
    from .models import Expense
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    expense_type_id = request.form.get('expense_type_id')

    new_expense = Expense(amount=amount, description=description, user_id=user_id, expense_type_id=expense_type_id)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/add_revenue', methods=['POST'])
def add_revenue():
    from .models import Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    revenue_type_id = request.form.get('revenue_type_id')

    new_revenue = Revenue(amount=amount, description=description, user_id=user_id, revenue_type_id=revenue_type_id)
    db.session.add(new_revenue)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/add_expense_type', methods=['POST'])
def add_expense_type():
    from .models import ExpenseType
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    name = request.form.get('name')
    new_expense_type = ExpenseType(name=name, user_id=user_id)
    db.session.add(new_expense_type)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/add_revenue_type', methods=['POST'])
def add_revenue_type():
    from .models import RevenueType
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    name = request.form.get('name')
    new_revenue_type = RevenueType(name=name, user_id=user_id)
    db.session.add(new_revenue_type)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/config', methods=['GET', 'POST'])
def config():
    from .models import User, ExpenseType, RevenueType, Expense, Revenue
    user_id = session.get('user_id')
    if not user_id:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    expense_types = ExpenseType.query.filter_by(user_id=user_id).all()
    revenue_types = RevenueType.query.filter_by(user_id=user_id).all()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    revenues = Revenue.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        user.fullname = fullname
        user.email = email
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('main.config'))

    return render_template('config.html', user=user, expense_types=expense_types, 
                           revenue_types=revenue_types, expenses=expenses, revenues=revenues)

@main.route('/delete_expense_type/<int:id>')
def delete_expense_type(id):
    from .models import ExpenseType, Expense
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir um tipo de despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    expense_type = ExpenseType.query.get(id)

    if not expense_type or expense_type.user_id != user_id:
        flash('Você não tem permissão para excluir esse tipo de despesa.', 'danger')
        return redirect(url_for('main.config'))

    # Verifica se existem despesas associadas a este tipo de despesa
    associated_expenses = Expense.query.filter_by(expense_type_id=id).count()
    if associated_expenses > 0:
        flash('Não é possível excluir este tipo de despesa, pois existem despesas associadas a ele.', 'danger')
        return redirect(url_for('main.config'))

    db.session.delete(expense_type)
    db.session.commit()
    flash('Tipo de despesa excluído com sucesso!', 'success')
    return redirect(url_for('main.config'))

@main.route('/delete_revenue_type/<int:id>')
def delete_revenue_type(id):
    from .models import RevenueType, Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir um tipo de receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    revenue_type = RevenueType.query.get(id)

    if not revenue_type or revenue_type.user_id != user_id:
        flash('Você não tem permissão para excluir esse tipo de receita.', 'danger')
        return redirect(url_for('main.config'))

    # Verifica se existem receitas associadas a este tipo de receita
    associated_revenues = Revenue.query.filter_by(revenue_type_id=id).count()
    if associated_revenues > 0:
        flash('Não é possível excluir este tipo de receita, pois existem receitas associadas a ele.', 'danger')
        return redirect(url_for('main.config'))

    db.session.delete(revenue_type)
    db.session.commit()
    flash('Tipo de receita excluído com sucesso!', 'success')
    return redirect(url_for('main.config'))

@main.route('/delete_expense/<int:id>')
def delete_expense(id):
    from .models import Expense
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma despesa.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    expense = Expense.query.get(id)

    if not expense or expense.user_id != user_id:
        flash('Você não tem permissão para excluir essa despesa.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(expense)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'success')
    return redirect(url_for('main.config'))

@main.route('/delete_revenue/<int:id>')
def delete_revenue(id):
    from .models import Revenue
    if 'user_id' not in session:
        flash('Por favor, faça login para excluir uma receita.', 'warning')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    revenue = Revenue.query.get(id)

    if not revenue or revenue.user_id != user_id:
        flash('Você não tem permissão para excluir essa receita.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(revenue)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('main.config'))


@main.route('/change_password', methods=['POST'])
def change_password():
    from .models import User
    if 'user_id' not in session:
        flash('Por favor, faça login para acessar essa página.', 'warning')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    
    if not check_password_hash(user.password, current_password):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('main.config'))
    
    if new_password != confirm_new_password:
        flash('As novas senhas não coincidem.', 'danger')
        return redirect(url_for('main.config'))
    
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('main.config'))
