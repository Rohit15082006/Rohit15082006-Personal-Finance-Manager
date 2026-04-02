# 💰 Personal Finance Manager

A modern, feature-rich web application for managing personal finances with real-time tracking, advanced reporting, and expense splitting for shared trips.

## ✨ Features

### Core Financial Management
- **Dashboard** - Real-time overview of all financial data with summary cards and charts
- **Expense Tracking** - Add, categorize, and track all expenses with dates and descriptions
- **Budget Management** - Set budgets by category and monitor actual spending vs. planned budget
- **Investment Portfolio** - Track investments across different types (Stocks, Bonds, Mutual Funds, Real Estate)
- **Savings Tracking** - Record savings with statistics and transaction history
- **Financial Reports** - Period-based reporting (This Month, Last Month, Last 3 Months, This Year) with detailed analysis

### Trip Expense Splitter ✨ NEW
- Create trips with destination and friend list
- Add shared expenses with who paid information
- Automatic equal-split calculation among all members
- Settlement summary showing who owes whom and how much
- Perfect for managing group trip costs

### User Interface
- Beautiful, modern Bootstrap 5 design with gradients and smooth animations
- Fully responsive (works on desktop, tablet, and mobile)
- Interactive charts using Chart.js for expense visualization
- Real-time data updates
- All amounts displayed in Indian Rupees (₹)

## 🛠 Tech Stack

### Backend
- **Python 3.13**
- **Flask 3.0.0** - Web framework
- **MySQL** - Database with `mysql-connector-python 8.2.0`

### Frontend
- **HTML5** - Structure
- **Bootstrap 5.3.0** - Responsive UI framework
- **Chart.js 4.4.0** - Data visualization
- **CSS3** - Styling with custom animations
- **JavaScript** - Client-side logic and form handling

## 📋 Requirements

```
Flask==3.0.0
mysql-connector-python==8.2.0
Werkzeug==3.0.1
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.13 or higher
- MySQL Server installed and running
- MySQL user with database creation permissions

### 2. Database Setup
```sql
CREATE DATABASE personal_finance_manager;
```

### 3. Clone & Install
```bash
# Navigate to project directory
cd "Auto typer"

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Configure Database Connection
Edit `app.py` and update the database credentials:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'personal_finance_manager',
    'charset': 'utf8'
}
```

### 5. Run the Application
```bash
python app.py
```

The app will start on `http://localhost:5000`

## 📁 Project Structure

```
Auto typer/
├── app.py                          # Flask application & database management
├── Finance-Manager.py              # Legacy Tkinter desktop app
├── README.md                        # This file
├── templates/
│   ├── base.html                  # Navigation template (extends all pages)
│   ├── index.html                 # Dashboard
│   ├── expenses.html              # Expense tracking
│   ├── budgets.html               # Budget management
│   ├── investments.html           # Investment portfolio
│   ├── savings.html               # Savings tracking
│   ├── reports.html               # Financial reports
│   └── trips.html                 # Trip expense splitter
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling & animations
│   └── js/
│       └── script.js              # Utility functions & validation
└── database/
    └── Tables created automatically on first run
```

## 💻 Usage

### Adding an Expense
1. Go to **Expenses** page
2. Fill in amount, category, date, and description
3. Click **Add Expense**
4. View all expenses in the history table

### Setting a Budget
1. Navigate to **Budgets** page
2. Enter category and budget amount
3. Click **Add Budget**
4. Compare actual spending against budget

### Tracking a Trip
1. Go to **Trip Splitter** page
2. Click **Plan a New Trip**
3. Enter trip name, destination, and friend names
4. Click **Create Trip**
5. Click **Manage Trip** to add expenses
6. View automatic settlement calculations

### Viewing Reports
1. Open **Reports** page
2. Select time period (This Month, Last Month, Last 3 Months, This Year)
3. View:
   - Total expenses, savings, investments, net worth
   - Expenses breakdown by category
   - Budget comparison
   - Charts and visualizations

## 🎯 Key API Endpoints

### Data Retrieval
- `GET /api/get-data` - Get all financial data
- `GET /api/get-report?period=<period>` - Get period-based report

### Transactions
- `POST /api/add-expense` - Add expense
- `POST /api/add-budget` - Add budget
- `POST /api/add-investment` - Add investment
- `POST /api/add-savings` - Add savings

### Trip Splitter
- `POST /api/create-trip` - Create new trip
- `GET /api/get-trips` - List all trips
- `GET /api/get-trip/<id>` - Get trip details with splits
- `POST /api/add-trip-expense` - Add expense to trip

## 🧮 Trip Splitter Algorithm

The expense splitter calculates equal splits automatically:

```
Per Person Share = Total Trip Expense ÷ Number of Members

For Each Member:
- Amount Paid: Sum of all expenses they paid
- Amount Owed: Per Person Share
- Balance: Amount Paid - Amount Owed
  - Positive = They receive money back
  - Negative = They owe money
  - Zero = Settled
```

**Example:**
- Trip Cost: ₹4500 (3 members)
- Per Person: ₹1500
- Aarya paid ₹3000 → Gets back ₹1500
- Raj paid ₹1500 → Even
- Priya paid ₹0 → Owes ₹1500

## 🔒 Data Security

- All database queries use parameterized statements
- Input validation on all forms
- No hardcoded test data in production
- MySQL database encryption compatible
- Passwords stored in database with hashing ready (extend as needed)

## 🎨 Customization

### Change Currency Symbol
Find all `₹` symbols in templates and replace with your preferred currency symbol.

### Modify Expense Categories
Edit the category options in `templates/expenses.html`:
```html
<option value="Your Category">Your Category</option>
```

### Adjust Budget Categories
Similar process in `templates/budgets.html`

## 📊 Database Tables

1. **expenses** - All expense records
2. **budgets** - Budget limits by category
3. **investments** - Investment portfolio
4. **savings** - Savings transactions
5. **trips** - Trip records
6. **trip_members** - Trip participant list
7. **trip_expenses** - Individual trip expenses

## 🐛 Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL
```
- Verify MySQL is running
- Check credentials in `app.py`
- Ensure database `personal_finance_manager` exists

### Port Already in Use
```
Address already in use
```
- Kill existing Flask process: `Get-Process python | Stop-Process -Force`
- Or change port in `app.py`: `app.run(port=5001)`

### Chart Not Displaying
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh page (Ctrl+F5)
- Check browser console for JavaScript errors

## 📈 Future Enhancements

- [ ] User authentication & multi-user support
- [ ] Data export (CSV, PDF)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics & predictions
- [ ] Recurring expense automation
- [ ] Currency conversion for international trips
- [ ] Splits with custom percentages (not just equal)
- [ ] Expense categories with subcategories
- [ ] Dark mode theme

## 📄 License

This project is open source and available for personal and educational use.

## 👤 Author

Created by **Aarya** - April 2026

For questions or suggestions, feel free to reach out!

---

**Made with ❤️ for better financial management**
