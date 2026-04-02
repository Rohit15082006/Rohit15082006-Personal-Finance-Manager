
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import mysql.connector as driver
from mysql.connector import Error
from dataclasses import dataclass
from typing import List, Dict
from calendar import monthrange
from decimal import Decimal

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
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
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

        for table_name, table_query in tables.items():
            try:
                self.cursor.execute(table_query)
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to create table {table_name}: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to add expense: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to fetch expenses: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to set budget: {str(e)}")
            return False

    def get_budgets(self) -> Dict[str, Budget]:
        query = "SELECT category, amount, period FROM budgets"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return {row[0]: Budget(category=row[0], amount=row[1], period=row[2])
                   for row in results}
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch budgets: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to add investment: {str(e)}")
            return False

    def get_investments(self) -> List[Investment]:
        query = "SELECT type, amount, date, description FROM investments ORDER BY date DESC"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [Investment(type=row[0], amount=row[1], date=row[2].strftime('%Y-%m-%d'), description=row[3])
                   for row in results]
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch investments: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to add savings: {str(e)}")
            return False

    def get_savings(self) -> List[Savings]:
        query = "SELECT amount, date, description FROM savings ORDER BY date DESC"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [Savings(amount=row[0], date=row[1].strftime('%Y-%m-%d'), description=row[2])
                   for row in results]
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch savings: {str(e)}")
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
            messagebox.showerror("Database Error", f"Failed to fetch monthly expenses: {str(e)}")
            return 0.0
    def get_monthly_investments_by_type(self, type: str, year: int, month: int) -> float:
        query = """
        SELECT SUM(amount) FROM investments 
        WHERE type = %s 
        AND YEAR(date) = %s 
        AND MONTH(date) = %s
        """
        try:
            self.cursor.execute(query, (type, year, month))
            result = self.cursor.fetchone()[0]
            return float(result) if result else 0.0
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch monthly investments: {str(e)}")
            return 0.0
    
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
        """Load all data from database"""
        self.expenses = self.db.get_expenses()
        self.budgets = self.db.get_budgets()
        self.investments = self.db.get_investments()
        self.savings = self.db.get_savings()

    def add_expense(self, expense: Expense):
        if self.db.add_expense(expense):
            self.expenses.append(expense)

    def check_budget_limit(self, category: str, amount: float) -> tuple[bool, float, float]:
        """Check if an expense would exceed the budget limit"""
        if category not in self.budgets:
            return True, 0, 0  # No budget set, so no limit

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

    def check_investment_limit(self, type: str, amount: float) -> tuple[bool, float, float]:
        """Check if an investment would exceed the budget limit"""
        if type not in self.budgets:
            return True, 0, 0  # No budget set, so no limit

        budget = self.budgets[type]
        current_date = datetime.now()
        current_month_investments = self.db.get_monthly_investments_by_type(
            type, current_date.year, current_date.month
        )

        budget_amount = budget.amount
        if budget.period == 'yearly':
            budget_amount = budget.amount / 12

        new_total = current_month_investments + amount
        remaining = budget_amount - current_month_investments
        
        return new_total <= budget_amount, remaining, budget_amount

    
    def add_investment(self, investment: Investment):
        if self.db.add_investment(investment):
            self.investments.append(investment)

    def add_savings(self, savings: Savings):
        if self.db.add_savings(savings):
            self.savings.append(savings)

# GUI Class

class FinanceManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("800x600")
        
        try:
            self.fm = PersonalFinanceManager()
        except Error as e:
            messagebox.showerror("Fatal Error", "Failed to initialize database. Application will exit.")
            root.destroy()
            return
            
        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # Create tabs
        self.budgets_frame = ttk.Frame(self.notebook)
        self.expenses_frame = ttk.Frame(self.notebook)
        self.savings_frame = ttk.Frame(self.notebook)
        self.investments_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook with savings before investments
        self.notebook.add(self.budgets_frame, text='Budgets')
        self.notebook.add(self.expenses_frame, text='Expenses')
        self.notebook.add(self.savings_frame, text='Savings')
        self.notebook.add(self.investments_frame, text='Investments')
        self.notebook.add(self.report_frame, text='Report')
        
        # Initialize all tabs in the same order
        self.create_budgets_tab()
        self.create_expenses_tab()
        self.create_savings_tab()
        self.create_investments_tab()
        self.create_report_tab()
        
        # Status Bar
        self.status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_expenses_tab(self):
        # Expense Input Section
        input_frame = ttk.LabelFrame(self.expenses_frame, text="Add New Expense")
        input_frame.pack(padx=10, pady=10, fill='x')

        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_combo = ttk.Combobox(input_frame, values=[
            'Food', 'Transportation', 'Utilities', 'Entertainment', 'Other'
        ])
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)

        # Date
        ttk.Label(input_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Description
        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        # Add Expense Button
        add_expense_btn = ttk.Button(input_frame, text="Add Expense", command=self.add_expense)
        add_expense_btn.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Expenses List
        self.expenses_tree = ttk.Treeview(self.expenses_frame, columns=('Amount', 'Category', 'Date', 'Description'), show='headings')
        self.expenses_tree.heading('Amount', text='Amount')
        self.expenses_tree.heading('Category', text='Category')
        self.expenses_tree.heading('Date', text='Date')
        self.expenses_tree.heading('Description', text='Description')
        self.expenses_tree.pack(padx=10, pady=10, expand=True, fill='both')

        # Populate existing expenses
        self.refresh_expenses_list()

    def create_budgets_tab(self):
        # Budget Input Section
        input_frame = ttk.LabelFrame(self.budgets_frame, text="Set Budget")
        input_frame.pack(padx=10, pady=10, fill='x')

        # Category
        ttk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_category_combo = ttk.Combobox(input_frame, values=[
            'Food', 'Transportation', 'Utilities', 'Entertainment', 'Other'
        ])
        self.budget_category_combo.grid(row=0, column=1, padx=5, pady=5)

        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.budget_amount_entry = ttk.Entry(input_frame)
        self.budget_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        # Period
        ttk.Label(input_frame, text="Period:").grid(row=1, column=0, padx=5, pady=5)
        self.budget_period_combo = ttk.Combobox(input_frame, values=['monthly', 'yearly'])
        self.budget_period_combo.grid(row=1, column=1, padx=5, pady=5)
        self.budget_period_combo.set('monthly')

        # Set Budget Button
        set_budget_btn = ttk.Button(input_frame, text="Set Budget", command=self.set_budget)
        set_budget_btn.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def create_investments_tab(self):
        # Investment Input Section
        input_frame = ttk.LabelFrame(self.investments_frame, text="Add New Investment")
        input_frame.pack(padx=10, pady=10, fill='x')
    
        # Type
        ttk.Label(input_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.investment_type_combo = ttk.Combobox(input_frame, values=[
            'Stocks', 'Bonds', 'Mutual Funds', 'Real Estate', 'Other'
        ])
        self.investment_type_combo.grid(row=0, column=1, padx=5, pady=5)
    
        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.investment_amount_entry = ttk.Entry(input_frame)
        self.investment_amount_entry.grid(row=0, column=3, padx=5, pady=5)
    
        # Date
        ttk.Label(input_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.investment_date_entry = ttk.Entry(input_frame)
        self.investment_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.investment_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
        # Description
        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5)
        self.investment_desc_entry = ttk.Entry(input_frame)
        self.investment_desc_entry.grid(row=1, column=3, padx=5, pady=5)
    
        # Add Investment Button
        add_investment_btn = ttk.Button(input_frame, text="Add Investment", command=self.add_investment)
        add_investment_btn.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    
        # Investments List
        self.investments_tree = ttk.Treeview(self.investments_frame, columns=('Type', 'Amount', 'Date', 'Description'), show='headings')
        self.investments_tree.heading('Type', text='Type')
        self.investments_tree.heading('Amount', text='Amount')
        self.investments_tree.heading('Date', text='Date')
        self.investments_tree.heading('Description', text='Description')
        self.investments_tree.pack(padx=10, pady=10, expand=True, fill='both')
    
        # Populate existing investments
        self.refresh_investments_list()

    def create_savings_tab(self):
        # Savings Input Section
        input_frame = ttk.LabelFrame(self.savings_frame, text="Add New Savings")
        input_frame.pack(padx=10, pady=10, fill='x')
    
        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.savings_amount_entry = ttk.Entry(input_frame)
        self.savings_amount_entry.grid(row=0, column=1, padx=5, pady=5)
    
        # Date
        ttk.Label(input_frame, text="Date:").grid(row=0, column=2, padx=5, pady=5)
        self.savings_date_entry = ttk.Entry(input_frame)
        self.savings_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.savings_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
        # Description
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.savings_desc_entry = ttk.Entry(input_frame)
        self.savings_desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
    
        # Add Savings Button
        add_savings_btn = ttk.Button(input_frame, text="Add Savings", command=self.add_savings)
        add_savings_btn.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    
        # Savings List
        self.savings_tree = ttk.Treeview(self.savings_frame, columns=('Amount', 'Date', 'Description'), show='headings')
        self.savings_tree.heading('Amount', text='Amount')
        self.savings_tree.heading('Date', text='Date')
        self.savings_tree.heading('Description', text='Description')
        self.savings_tree.pack(padx=10, pady=10, expand=True, fill='both')
    
        # Populate existing savings
        self.refresh_savings_list()
    
    def create_report_tab(self):
        # Report Controls
        control_frame = ttk.Frame(self.report_frame)
        control_frame.pack(padx=10, pady=5, fill='x')
    
        ttk.Label(control_frame, text="Period:").pack(side=tk.LEFT, padx=5)
        self.report_period = ttk.Combobox(control_frame, values=['This Month', 'Last Month', 'Last 3 Months', 'This Year'])
        self.report_period.pack(side=tk.LEFT, padx=5)
        self.report_period.set('This Month')
    
        refresh_btn = ttk.Button(control_frame, text="Refresh Report", command=self.refresh_report)
        refresh_btn.pack(side=tk.LEFT, padx=5)
    
        # Report Display
        report_display = ttk.Frame(self.report_frame)
        report_display.pack(padx=10, pady=5, expand=True, fill='both')
    
        # Summary Section
        summary_frame = ttk.LabelFrame(report_display, text="Financial Summary")
        summary_frame.pack(padx=5, pady=5, fill='x')
    
        self.total_expenses_label = ttk.Label(summary_frame, text="Total Expenses: $0")
        self.total_expenses_label.pack(anchor='w', padx=5, pady=2)
    
        self.total_savings_label = ttk.Label(summary_frame, text="Total Savings: $0")
        self.total_savings_label.pack(anchor='w', padx=5, pady=2)
    
        self.total_investments_label = ttk.Label(summary_frame, text="Total Investments: $0")
        self.total_investments_label.pack(anchor='w', padx=5, pady=2)
    
        self.net_worth_label = ttk.Label(summary_frame, text="Net Worth: $0")
        self.net_worth_label.pack(anchor='w', padx=5, pady=2)
    
        # Budget vs Actual Section
        budget_frame = ttk.LabelFrame(report_display, text="Budget vs Actual")
        budget_frame.pack(padx=5, pady=5, fill='both', expand=True)
    
        self.budget_tree = ttk.Treeview(budget_frame, columns=('Category', 'Budget', 'Actual', 'Difference'), show='headings')
        self.budget_tree.heading('Category', text='Category')
        self.budget_tree.heading('Budget', text='Budget')
        self.budget_tree.heading('Actual', text='Actual')
        self.budget_tree.heading('Difference', text='Difference')
        self.budget_tree.pack(padx=5, pady=5, fill='both', expand=True)
    
    def refresh_report(self):
        period = self.report_period.get()
        
        # Calculate date range
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
        else:  # This Year
            start_date = end_date.replace(month=1, day=1)
    
        # Calculate totals
        total_expenses = sum(float(expense.amount) for expense in self.fm.expenses 
                     if start_date <= datetime.strptime(expense.date, '%Y-%m-%d') <= end_date)
        
        total_savings = sum(saving.amount for saving in self.fm.savings 
                           if start_date <= datetime.strptime(saving.date, '%Y-%m-%d') <= end_date)
        
        total_investments = sum(float(investment.amount) for investment in self.fm.investments
                                if start_date <= datetime.strptime(investment.date, '%Y-%m-%d') <= end_date)
        
        # Update summary labels
        self.total_expenses_label.config(text=f"Total Expenses: ${total_expenses:,.2f}")
        self.total_savings_label.config(text=f"Total Savings: ${total_savings:,.2f}")
        self.total_investments_label.config(text=f"Total Investments: ${total_investments:,.2f}")
        
        # Convert values to Decimal before calculation
        net_worth = (Decimal(str(total_savings)) + Decimal(str(total_investments)) - Decimal(str(total_expenses)))
        self.net_worth_label.config(text=f"Net Worth: ${net_worth:,.2f}")
    
        # Update budget vs actual
        self.budget_tree.delete(*self.budget_tree.get_children())
        
        # Calculate expenses by category
        expenses_by_category = {}
        for expense in self.fm.expenses:
            if start_date <= datetime.strptime(expense.date, '%Y-%m-%d') <= end_date:
                expenses_by_category[expense.category] = expenses_by_category.get(expense.category, 0) + expense.amount
    
        # Compare with budgets
        for category, budget in self.fm.budgets.items():
            actual = expenses_by_category.get(category, 0)
            budget_amount = budget.amount
            if budget.period == 'yearly' and period != 'This Year':
                budget_amount = budget_amount / 12
            
            # If you want to use Decimal (recommended for financial calculations)
            difference = Decimal(str(budget_amount)) - Decimal(str(actual))
            
            # OR if you prefer using float
            difference = float(budget_amount) - float(actual)
            self.budget_tree.insert('', 'end', values=(
                category,
                f"${budget_amount:,.2f}",
                f"${actual:,.2f}",
                f"${difference:,.2f}"
            ))
    
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combo.get()
            date = self.date_entry.get()
            description = self.desc_entry.get()

            if not all([amount, category, date]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Check budget limit
            within_limit, remaining, budget = self.fm.check_budget_limit(category, amount)
            
            if not within_limit:
                warning_msg = f"Warning: This expense will exceed your {category} budget!\n\n"
                warning_msg += f"Budget: ${budget:,.2f}\n"
                warning_msg += f"Remaining: ${remaining:,.2f}\n"
                warning_msg += f"This expense: ${amount:,.2f}\n\n"
                warning_msg += "Do you want to proceed anyway?"
                
                if not messagebox.askyesno("Budget Warning", warning_msg):
                    return

            expense = Expense(amount=amount, category=category, date=date, description=description)
            self.fm.add_expense(expense)
            self.refresh_expenses_list()
            self.clear_expense_inputs()
            self.refresh_report()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def add_investment(self):
        try:
            amount = float(self.investment_amount_entry.get())
            type_ = self.investment_type_combo.get()
            date = self.investment_date_entry.get()
            description = self.investment_desc_entry.get()

            if not all([amount, type_, date]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Check investment limit
            within_limit, remaining, budget = self.fm.check_investment_limit(type_, amount)
            
            if not within_limit:
                warning_msg = f"Warning: This investment will exceed your {type_} budget!\n\n"
                warning_msg += f"Budget: ${budget:,.2f}\n"
                warning_msg += f"Remaining: ${remaining:,.2f}\n"
                warning_msg += f"This investment: ${amount:,.2f}\n\n"
                warning_msg += "Do you want to proceed anyway?"
                
                if not messagebox.askyesno("Budget Warning", warning_msg):
                    return

            investment = Investment(type=type_, amount=amount, date=date, description=description)
            self.fm.add_investment(investment)
            self.refresh_investments_list()
            self.clear_investment_inputs()
            self.refresh_report()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def add_savings(self):
        try:
            amount = float(self.savings_amount_entry.get())
            date = self.savings_date_entry.get()
            description = self.savings_desc_entry.get()
    
            if not all([amount, date]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
    
            savings = Savings(amount=amount, date=date, description=description)
            self.fm.add_savings(savings)
            self.refresh_savings_list()
            self.clear_savings_inputs()
            self.refresh_report()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def set_budget(self):
        try:
            amount = float(self.budget_amount_entry.get())
            category = self.budget_category_combo.get()
            period = self.budget_period_combo.get()
    
            if not all([amount, category, period]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
    
            budget = Budget(category=category, amount=amount, period=period)
            self.fm.set_budget(budget)
            self.clear_budget_inputs()
            self.refresh_report()
            messagebox.showinfo("Success", "Budget has been set successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
    
    def refresh_expenses_list(self):
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        for expense in self.fm.expenses:
            self.expenses_tree.insert('', 'end', values=(
                f"${expense.amount:,.2f}",
                expense.category,
                expense.date,
                expense.description
            ))
    
    def refresh_investments_list(self):
        for item in self.investments_tree.get_children():
            self.investments_tree.delete(item)
        
        for investment in self.fm.investments:
            self.investments_tree.insert('', 'end', values=(
                investment.type,
                f"${investment.amount:,.2f}",
                investment.date,
                investment.description
            ))
    
    def refresh_savings_list(self):
        for item in self.savings_tree.get_children():
            self.savings_tree.delete(item)
        
        for saving in self.fm.savings:
            self.savings_tree.insert('', 'end', values=(
                f"${saving.amount:,.2f}",
                saving.date,
                saving.description
            ))
    
    def clear_expense_inputs(self):
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set('')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.desc_entry.delete(0, tk.END)
    
    def clear_investment_inputs(self):
        self.investment_amount_entry.delete(0, tk.END)
        self.investment_type_combo.set('')
        self.investment_date_entry.delete(0, tk.END)
        self.investment_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.investment_desc_entry.delete(0, tk.END)

    def clear_savings_inputs(self):
        self.savings_amount_entry.delete(0, tk.END)
        self.savings_date_entry.delete(0, tk.END)
        self.savings_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.savings_desc_entry.delete(0, tk.END)

    def clear_budget_inputs(self):
        self.budget_amount_entry.delete(0, tk.END)
        self.budget_category_combo.set('')
        self.budget_period_combo.set('monthly')

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))

    def __del__(self):
        if hasattr(self, 'fm'):
            self.fm.db.close()

def main():
    try:
        root = tk.Tk()
        root.title("Personal Finance Manager")
        
        # Set the theme for ttk widgets
        style = ttk.Style()
        try:
            style.theme_use('clam')  # Use 'clam' theme for a modern look
        except tk.TclError:
            pass  # If theme is not available, use default

        # Configure some basic styles
        style.configure('TLabel', padding=2)
        style.configure('TButton', padding=4)
        style.configure('TEntry', padding=2)
        
        # Configure Treeview colors and style
        style.configure("Treeview",
                    background="#ffffff",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#ffffff")
        style.map('Treeview',
                background=[('selected', '#0078D7')])

        # Initialize the application
        app = FinanceManagerGUI(root)
        
        # Center the window on the screen
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Make window resizable
        root.resizable(True, True)
        
        # Set minimum window size
        root.minsize(800, 600)
        
        # Add window closing handler
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                if hasattr(app, 'fm'):
                    app.fm.db.close()
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()