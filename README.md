# Tesouraria - Personal Finance Accounting System

A simple and efficient personal finance management system for tracking accounts, transactions, income, and expenses.

## Features

- **Account Management**: Create and manage multiple accounts (checking, savings, cash, credit cards)
- **Transaction Tracking**: Record income and expenses with detailed categorization
- **Category System**: Organize transactions with customizable categories
- **Balance Calculation**: Real-time account balance tracking
- **Financial Reports**: View income vs expenses, category breakdowns, and account summaries
- **Data Persistence**: All data saved in JSON format for easy backup and portability
- **CLI Interface**: User-friendly command-line interface for all operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Stefremy/tesouraria.git
cd tesouraria
```

2. No external dependencies required! Python 3.6+ is all you need.

## Usage

### Running the CLI Application

Start the interactive CLI:
```bash
python -m tesouraria.cli
```

### Main Menu Options

1. **Manage Accounts**
   - List all accounts
   - Add new accounts
   - View account balances

2. **Manage Transactions**
   - List all transactions
   - Add income or expenses

3. **View Reports**
   - Account balances summary
   - Income vs expenses
   - Category breakdown

4. **Manage Categories**
   - List categories
   - Add custom categories

### Quick Start Example

1. Create an account:
   - Select "1. Manage Accounts"
   - Select "2. Add Account"
   - Enter account details (e.g., "Checking", "checking", initial balance "1000")

2. Add a transaction:
   - Select "2. Manage Transactions"
   - Select "2. Add Transaction"
   - Enter transaction details (date, description, type, category, amount, account)

3. View your finances:
   - Select "3. View Reports"
   - Choose any report to see your financial status

## Programmatic Usage

You can also use Tesouraria as a Python library:

```python
from datetime import datetime
from decimal import Decimal
from tesouraria import FinanceManager

# Initialize the finance manager
manager = FinanceManager()

# Create an account
manager.add_account("Checking", "checking", Decimal('1000'))

# Add a transaction
manager.add_transaction(
    date=datetime.now(),
    description="Monthly Salary",
    amount=Decimal('5000'),
    category="Salary",
    transaction_type="income",
    account="Checking"
)

# Get account balance
balance = manager.get_account_balance("Checking")
print(f"Current balance: ${balance}")

# View totals
total_income = manager.get_total_income()
total_expenses = manager.get_total_expenses()
net_income = manager.get_net_income()
```

## Data Storage

All financial data is stored in `data/finance_data.json`. This file contains:
- Account information
- Transaction history
- Category definitions

The file is automatically created on first run with default categories.

## Default Categories

### Income Categories
- Salary
- Investment Income
- Other Income

### Expense Categories
- Food & Dining
- Transportation
- Housing
- Utilities
- Healthcare
- Entertainment
- Shopping
- Other Expense

You can add custom categories through the CLI or programmatically.

## Running Tests

Run the test suite:
```bash
python -m unittest discover tests
```

Or run specific test file:
```bash
python -m unittest tests.test_finance
```

## Project Structure

```
tesouraria/
├── tesouraria/          # Main package
│   ├── __init__.py      # Package initialization
│   ├── finance.py       # Core finance management logic
│   └── cli.py           # Command-line interface
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_finance.py  # Unit tests
├── data/                # Data storage (created on first run)
│   └── finance_data.json
├── requirements.txt     # Python dependencies (none for basic usage)
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for personal and educational use.

## Author

Tesouraria Gilberto
