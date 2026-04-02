# Personal Finance Manager - Web Version

Beautiful HTML/CSS web-based Finance Manager built with Flask, Bootstrap 5, and Chart.js

## Features

✨ **Dashboard** - Overview of your financial status with charts and summary cards
💰 **Expense Tracking** - Log and categorize your expenses
💳 **Budget Management** - Set and monitor budgets for different categories
📈 **Investment Tracking** - Track your investments and growth
🏦 **Savings Management** - Monitor your savings progress
📊 **Financial Reports** - Detailed reports with charts and comparisons
📱 **Responsive Design** - Works beautifully on desktop, tablet, and mobile
🎨 **Modern UI** - Beautiful gradient design with smooth animations

## Installation

### 1. Install Python Packages

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask==3.0.0
pip install mysql-connector-python==8.2.0
```

### 2. Ensure MySQL is Running

Make sure you have MySQL Server running on your system. The app will automatically create the database and tables.

Database credentials (update in `app.py` if needed):
- Host: localhost
- User: root
- Password: 763737@AF

## Running the Application

### Start the Flask Server

```bash
python app.py
```

The application will start on: **http://localhost:5000**

Access it in your web browser and you're ready to go!

## Usage

### Dashboard
- View your financial summary
- See expense breakdown by category
- Monitor budget vs actual comparison
- Track recent expenses

### Expenses
- Add new expenses with category, date, and description
- View complete expense history
- Expenses are automatically checked against your budget

### Budgets
- Set monthly or yearly budgets for different categories
- View budget progress and remaining amounts
- Get alerts when approaching or exceeding limits

### Investments
- Track different types of investments (Stocks, Bonds, etc.)
- Record investment amount and date
- Maintain complete investment portfolio

### Savings
- Log savings transactions
- View total savings and transaction statistics
- Track savings growth over time

### Reports
- Generate reports for different time periods
- See expense breakdown by category
- Compare actual spending vs budgets
- View net worth calculation

## Features Breakdown

### Responsive Navigation
- Easy navigation between different sections
- Mobile-friendly hamburger menu
- Active page highlighting

### Data Visualization
- Pie charts for expense distribution
- Bar charts for budget comparisons
- Real-time data updates

### Validation
- Form validation for all inputs
- Budget limit checking
- Date validation (no future dates)
- Amount validation

### Database
- MySQL backend for data persistence
- Automatic table creation
- Efficient queries with proper indexing

## File Structure

```
Auto typer/
├── app.py              # Flask application and backend logic
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Dashboard
│   ├── expenses.html  # Expenses page
│   ├── budgets.html   # Budgets page
│   ├── investments.html # Investments page
│   ├── savings.html   # Savings page
│   └── reports.html   # Reports page
└── static/            # Static files
    ├── css/
    │   └── style.css  # Custom styling
    └── js/
        └── script.js  # JavaScript functionality
```

## API Endpoints

- `GET /` - Dashboard
- `GET /expenses` - Expenses page
- `GET /budgets` - Budgets page
- `GET /investments` - Investments page
- `GET /savings` - Savings page
- `GET /reports` - Reports page
- `POST /api/add-expense` - Add expense
- `POST /api/add-budget` - Set budget
- `POST /api/add-investment` - Add investment
- `POST /api/add-savings` - Add savings
- `GET /api/get-report` - Get report data
- `GET /api/get-data` - Get all data

## Customization

### Database Credentials
Edit the credentials in `app.py` (line 56-60):
```python
self.connection = driver.connect(
    host='localhost',
    user='root',
    password='763737@AF',  # Change this
    charset='utf8'
)
```

### Categories
Edit the expense/budget/investment categories in the templates.

### Colors & Styling
Modify `static/css/style.css` to change the color scheme and styling.

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Troubleshooting

### Database Connection Error
- Make sure MySQL is running
- Check your username and password
- Verify the host is correct

### Port Already in Use
Change the port in `app.py` (last line):
```python
app.run(debug=True, host='localhost', port=5001)  # Change 5000 to 5001
```

### Missing Dependencies
Run: `pip install -r requirements.txt`

## Tips

1. **Regular Backups** - Export your data regularly
2. **Budget Planning** - Set realistic budgets based on your spending patterns
3. **Monthly Reviews** - Check reports at the end of each month
4. **Investment Tracking** - Update investment values regularly
5. **Category Consistency** - Use the same categories for better reporting

## Future Enhancements

- User authentication and multi-user support
- Data export (PDF, CSV, Excel)
- Advanced filtering and search
- Recurring expenses
- Bill reminders
- Goal setting and tracking
- Data visualization improvements
- Dark mode

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions, check the error messages in the browser console.

---

**Happy Financial Planning! 💰**
