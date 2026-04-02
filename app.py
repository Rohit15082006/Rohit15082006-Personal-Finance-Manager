from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from decimal import Decimal
import mysql.connector as driver
from mysql.connector import Error
from dataclasses import dataclass
from typing import List, Dict

app = Flask(__name__)

# Data Classes
@dataclass
class Expense:
    amount: float
    category: str
    date: str
    description: str = ''

@dataclass
class Budget:
    category: str
    amount: float
    period: str = 'monthly'

@dataclass
class Investment:
    type: str
    amount: float
    date: str
    description: str = ''

@dataclass
class Savings:
    amount: float
    date: str
    description: str = ''

# Database Manager
class DatabaseManager:
    def __init__(self):
        try:
            self.connection = driver.connect(
                host='localhost',
                user='root',
                password='763737@AF',
                charset='utf8'
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS personal_finance_manager")
            self.cursor.execute("USE personal_finance_manager")
            self.create_tables()
        except Error as e:
            print(f"Database Error: {str(e)}")
            raise

    def create_tables(self):
        tables = {}
        tables['expenses'] = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        tables['budgets'] = """
        CREATE TABLE IF NOT EXISTS budgets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100) NOT NULL UNIQUE,
            amount DECIMAL(10,2) NOT NULL,
            period ENUM('monthly', 'yearly') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        tables['investments'] = """
        CREATE TABLE IF NOT EXISTS investments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        tables['savings'] = """
        CREATE TABLE IF NOT EXISTS savings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        tables['trips'] = """
        CREATE TABLE IF NOT EXISTS trips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_name VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            total_members INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        tables['trip_members'] = """
        CREATE TABLE IF NOT EXISTS trip_members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL,
            member_name VARCHAR(255) NOT NULL,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
        """
        
        tables['trip_expenses'] = """
        CREATE TABLE IF NOT EXISTS trip_expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL,
            description VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            paid_by VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
        """
        for table_name, table_query in tables.items():
            try:
                self.cursor.execute(table_query)
            except Error as e:
                print(f"Failed to create table {table_name}: {str(e)}")
                raise

    def add_expense(self, expense: Expense) -> bool:
        query = """
        INSERT INTO expenses (amount, category, date, description)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (expense.amount, expense.category,
                                      expense.date, expense.description))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to add expense: {str(e)}")
            return False

    def get_expenses(self) -> List[Expense]:
        query = "SELECT amount, category, date, description FROM expenses ORDER BY date DESC"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [Expense(amount=row[0], category=row[1],
                          date=row[2].strftime('%Y-%m-%d'), description=row[3])
                   for row in results]
        except Error as e:
            print(f"Failed to fetch expenses: {str(e)}")
            return []

    def set_budget(self, budget: Budget) -> bool:
        query = """
        INSERT INTO budgets (category, amount, period)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        amount = VALUES(amount),
        period = VALUES(period)
        """
        try:
            self.cursor.execute(query, (budget.category, budget.amount, budget.period))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to set budget: {str(e)}")
            return False

    def get_budgets(self) -> Dict[str, Budget]:
        query = "SELECT category, amount, period FROM budgets"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return {row[0]: Budget(category=row[0], amount=row[1], period=row[2])
                   for row in results}
        except Error as e:
            print(f"Failed to fetch budgets: {str(e)}")
            return {}

    def add_investment(self, investment: Investment) -> bool:
        query = """
        INSERT INTO investments (type, amount, date, description)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (investment.type, investment.amount, investment.date, investment.description))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to add investment: {str(e)}")
            return False

    def get_investments(self) -> List[Investment]:
        query = "SELECT type, amount, date, description FROM investments ORDER BY date DESC"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [Investment(type=row[0], amount=row[1], date=row[2].strftime('%Y-%m-%d'), description=row[3])
                   for row in results]
        except Error as e:
            print(f"Failed to fetch investments: {str(e)}")
            return []

    def add_savings(self, savings: Savings) -> bool:
        query = """
        INSERT INTO savings (amount, date, description)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (savings.amount, savings.date, savings.description))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to add savings: {str(e)}")
            return False

    def get_savings(self) -> List[Savings]:
        query = "SELECT amount, date, description FROM savings ORDER BY date DESC"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [Savings(amount=row[0], date=row[1].strftime('%Y-%m-%d'), description=row[2])
                   for row in results]
        except Error as e:
            print(f"Failed to fetch savings: {str(e)}")
            return []

    def get_monthly_expenses_by_category(self, category: str, year: int, month: int) -> float:
        query = """
        SELECT SUM(amount) FROM expenses 
        WHERE category = %s 
        AND YEAR(date) = %s 
        AND MONTH(date) = %s
        """
        try:
            self.cursor.execute(query, (category, year, month))
            result = self.cursor.fetchone()[0]
            return float(result) if result else 0.0
        except Error as e:
            print(f"Failed to fetch monthly expenses: {str(e)}")
            return 0.0

    def create_trip(self, trip_name: str, destination: str, members: list) -> int:
        """Create a new trip and add members"""
        try:
            insert_trip = "INSERT INTO trips (trip_name, destination, total_members) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_trip, (trip_name, destination, len(members)))
            self.connection.commit()
            trip_id = self.cursor.lastrowid
            
            for member in members:
                insert_member = "INSERT INTO trip_members (trip_id, member_name) VALUES (%s, %s)"
                self.cursor.execute(insert_member, (trip_id, member))
            self.connection.commit()
            return trip_id
        except Error as e:
            print(f"Failed to create trip: {str(e)}")
            return None

    def get_trips(self) -> List[Dict]:
        """Get all trips"""
        try:
            query = "SELECT id, trip_name, destination, total_members, created_at FROM trips ORDER BY created_at DESC"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [{'id': row[0], 'trip_name': row[1], 'destination': row[2], 'total_members': row[3], 'date': row[4].strftime('%Y-%m-%d')} for row in results]
        except Error as e:
            print(f"Failed to fetch trips: {str(e)}")
            return []

    def get_trip_members(self, trip_id: int) -> List[str]:
        """Get members of a trip"""
        try:
            query = "SELECT member_name FROM trip_members WHERE trip_id = %s"
            self.cursor.execute(query, (trip_id,))
            results = self.cursor.fetchall()
            return [row[0] for row in results]
        except Error as e:
            print(f"Failed to fetch trip members: {str(e)}")
            return []

    def add_trip_expense(self, trip_id: int, description: str, amount: float, paid_by: str, date: str) -> bool:
        """Add expense to a trip"""
        try:
            query = "INSERT INTO trip_expenses (trip_id, description, amount, paid_by, date) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (trip_id, description, amount, paid_by, date))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to add trip expense: {str(e)}")
            return False

    def get_trip_expenses(self, trip_id: int) -> List[Dict]:
        """Get all expenses for a trip"""
        try:
            query = "SELECT description, amount, paid_by, date FROM trip_expenses WHERE trip_id = %s ORDER BY date DESC"
            self.cursor.execute(query, (trip_id,))
            results = self.cursor.fetchall()
            return [{'description': row[0], 'amount': row[1], 'paid_by': row[2], 'date': row[3].strftime('%Y-%m-%d')} for row in results]
        except Error as e:
            print(f"Failed to fetch trip expenses: {str(e)}")
            return []

    def calculate_splits(self, trip_id: int) -> Dict:
        """Calculate who owes whom in a trip"""
        try:
            members = self.get_trip_members(trip_id)
            expenses = self.get_trip_expenses(trip_id)
            
            if not members or not expenses:
                return {}
            
            total_amount = sum(float(e['amount']) for e in expenses)
            per_person = total_amount / len(members)
            
            paid_by_person = {}
            for expense in expenses:
                paid = float(expense['amount'])
                person = expense['paid_by']
                paid_by_person[person] = paid_by_person.get(person, 0) + paid
            
            splits = {}
            for member in members:
                splits[member] = {
                    'paid': paid_by_person.get(member, 0),
                    'owes': per_person,
                    'balance': paid_by_person.get(member, 0) - per_person
                }
            
            return {'splits': splits, 'total': total_amount, 'per_person': per_person}
        except Exception as e:
            print(f"Failed to calculate splits: {str(e)}")
            return {}

    def close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

# Finance Manager Class
class PersonalFinanceManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.load_data()

    def load_data(self):
        self.expenses = self.db.get_expenses()
        self.budgets = self.db.get_budgets()
        self.investments = self.db.get_investments()
        self.savings = self.db.get_savings()

    def add_expense(self, expense: Expense):
        if self.db.add_expense(expense):
            self.expenses.append(expense)
            return True
        return False

    def check_budget_limit(self, category: str, amount: float) -> tuple:
        if category not in self.budgets:
            return True, 0, 0
        budget = self.budgets[category]
        current_date = datetime.now()
        current_month_expenses = self.db.get_monthly_expenses_by_category(
            category, current_date.year, current_date.month
        )
        budget_amount = budget.amount
        if budget.period == 'yearly':
            budget_amount = budget.amount / 12
        new_total = current_month_expenses + amount
        remaining = budget_amount - current_month_expenses
        return new_total <= budget_amount, remaining, budget_amount

    def set_budget(self, budget: Budget):
        if self.db.set_budget(budget):
            self.budgets[budget.category] = budget
            return True
        return False

    def add_investment(self, investment: Investment):
        if self.db.add_investment(investment):
            self.investments.append(investment)
            return True
        return False

    def add_savings(self, savings: Savings):
        if self.db.add_savings(savings):
            self.savings.append(savings)
            return True
        return False

# Initialize FM
try:
    fm = PersonalFinanceManager()
except:
    fm = None

# Routes
@app.route('/')
def index():
    if fm is None:
        return "Database connection failed", 500
    return render_template('index.html', fm=fm)

@app.route('/expenses')
def expenses():
    if fm is None:
        return "Database connection failed", 500
    return render_template('expenses.html', expenses=fm.expenses)

@app.route('/budgets')
def budgets():
    if fm is None:
        return "Database connection failed", 500
    return render_template('budgets.html', budgets=fm.budgets)

@app.route('/investments')
def investments():
    if fm is None:
        return "Database connection failed", 500
    return render_template('investments.html', investments=fm.investments)

@app.route('/savings')
def savings():
    if fm is None:
        return "Database connection failed", 500
    return render_template('savings.html', savings=fm.savings)

@app.route('/reports')
def reports():
    if fm is None:
        return "Database connection failed", 500
    return render_template('reports.html')

@app.route('/trips')
def trips():
    if fm is None:
        return "Database connection failed", 500
    return render_template('trips.html')

# API Routes
@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        expense = Expense(
            amount=float(data['amount']),
            category=data['category'],
            date=data['date'],
            description=data.get('description', '')
        )
        within_limit, remaining, budget = fm.check_budget_limit(expense.category, expense.amount)
        if fm.add_expense(expense):
            return jsonify({'success': True, 'within_limit': within_limit, 'remaining': remaining})
        return jsonify({'success': False, 'error': 'Failed to add expense'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/add-budget', methods=['POST'])
def add_budget():
    try:
        data = request.json
        budget = Budget(
            category=data['category'],
            amount=float(data['amount']),
            period=data.get('period', 'monthly')
        )
        if fm.set_budget(budget):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to set budget'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/add-investment', methods=['POST'])
def add_investment():
    try:
        data = request.json
        investment = Investment(
            type=data['type'],
            amount=float(data['amount']),
            date=data['date'],
            description=data.get('description', '')
        )
        if fm.add_investment(investment):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to add investment'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/add-savings', methods=['POST'])
def add_savings():
    try:
        data = request.json
        savings = Savings(
            amount=float(data['amount']),
            date=data['date'],
            description=data.get('description', '')
        )
        if fm.add_savings(savings):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to add savings'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/get-report')
def get_report():
    try:
        period = request.args.get('period', 'This Month')
        end_date = datetime.now()
        
        if period == 'This Month':
            start_date = end_date.replace(day=1)
        elif period == 'Last Month':
            first_day = end_date.replace(day=1)
            start_date = first_day - timedelta(days=1)
            start_date = start_date.replace(day=1)
            end_date = first_day - timedelta(days=1)
        elif period == 'Last 3 Months':
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date.replace(month=1, day=1)

        total_expenses = sum(float(e.amount) for e in fm.expenses
                   if start_date <= datetime.strptime(e.date, '%Y-%m-%d') <= end_date)
        total_savings = sum(float(s.amount) for s in fm.savings
                  if start_date <= datetime.strptime(s.date, '%Y-%m-%d') <= end_date)
        total_investments = sum(float(i.amount) for i in fm.investments
                      if start_date <= datetime.strptime(i.date, '%Y-%m-%d') <= end_date)

        expenses_by_category = {}
        for e in fm.expenses:
            if start_date <= datetime.strptime(e.date, '%Y-%m-%d') <= end_date:
                expenses_by_category[e.category] = expenses_by_category.get(e.category, 0) + float(e.amount)

        budget_data = []
        for category, budget in fm.budgets.items():
            actual = expenses_by_category.get(category, 0)
            budget_amount = float(budget.amount)
            if budget.period == 'yearly' and period != 'This Year':
                budget_amount = budget_amount / 12
            difference = budget_amount - actual
            budget_data.append({
                'category': category,
                'budget': budget_amount,
                'actual': actual,
                'difference': difference
            })

        return jsonify({
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'total_investments': total_investments,
            'net_worth': total_savings + total_investments - total_expenses,
            'expenses_by_category': expenses_by_category,
            'budget_data': budget_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/get-data')
def get_data():
    fm.load_data()
    return jsonify({
        'expenses': [(e.amount, e.category, e.date, e.description) for e in fm.expenses],
        'budgets': {k: {'amount': v.amount, 'period': v.period} for k, v in fm.budgets.items()},
        'investments': [(i.type, i.amount, i.date, i.description) for i in fm.investments],
        'savings': [(s.amount, s.date, s.description) for s in fm.savings]
    })

@app.route('/api/create-trip', methods=['POST'])
def create_trip():
    try:
        data = request.json
        trip_id = fm.db.create_trip(data['trip_name'], data['destination'], data['members'])
        if trip_id:
            return jsonify({'success': True, 'trip_id': trip_id})
        return jsonify({'success': False, 'error': 'Failed to create trip'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/get-trips')
def get_trips():
    try:
        trips = fm.db.get_trips()
        return jsonify({'success': True, 'trips': trips})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/get-trip/<int:trip_id>')
def get_trip_details(trip_id):
    try:
        members = fm.db.get_trip_members(trip_id)
        expenses = fm.db.get_trip_expenses(trip_id)
        splits = fm.db.calculate_splits(trip_id)
        return jsonify({
            'success': True,
            'members': members,
            'expenses': expenses,
            'splits': splits
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/add-trip-expense', methods=['POST'])
def add_trip_expense():
    try:
        data = request.json
        if fm.db.add_trip_expense(data['trip_id'], data['description'], float(data['amount']), data['paid_by'], data['date']):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to add expense'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
