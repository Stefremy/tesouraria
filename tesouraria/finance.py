"""
Tesouraria - Personal Finance Accounting System
Core data models for managing accounts, transactions, and categories.
"""

from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal
import json
from pathlib import Path


class Category:
    """Represents a transaction category (e.g., Food, Transportation, Salary)."""
    
    def __init__(self, name: str, category_type: str):
        """
        Initialize a category.
        
        Args:
            name: Category name
            category_type: Either 'income' or 'expense'
        """
        if category_type not in ['income', 'expense']:
            raise ValueError("Category type must be 'income' or 'expense'")
        self.name = name
        self.category_type = category_type
    
    def to_dict(self) -> Dict:
        """Convert category to dictionary."""
        return {
            'name': self.name,
            'category_type': self.category_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Category':
        """Create category from dictionary."""
        return cls(data['name'], data['category_type'])


class Transaction:
    """Represents a financial transaction."""
    
    def __init__(self, date: datetime, description: str, amount: Decimal,
                 category: str, transaction_type: str, account: str,
                 transaction_id: Optional[str] = None):
        """
        Initialize a transaction.
        
        Args:
            date: Transaction date
            description: Transaction description
            amount: Transaction amount (positive for income, positive for expense)
            category: Category name
            transaction_type: Either 'income' or 'expense'
            account: Account name
            transaction_id: Unique identifier (auto-generated if None)
        """
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        
        self.transaction_id = transaction_id or self._generate_id()
        self.date = date
        self.description = description
        self.amount = abs(Decimal(str(amount)))  # Store as positive
        self.category = category
        self.transaction_type = transaction_type
        self.account = account
    
    @staticmethod
    def _generate_id() -> str:
        """Generate a unique transaction ID."""
        from uuid import uuid4
        return str(uuid4())
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary."""
        return {
            'transaction_id': self.transaction_id,
            'date': self.date.isoformat(),
            'description': self.description,
            'amount': str(self.amount),
            'category': self.category,
            'transaction_type': self.transaction_type,
            'account': self.account
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Create transaction from dictionary."""
        return cls(
            date=datetime.fromisoformat(data['date']),
            description=data['description'],
            amount=Decimal(data['amount']),
            category=data['category'],
            transaction_type=data['transaction_type'],
            account=data['account'],
            transaction_id=data.get('transaction_id')
        )


class Account:
    """Represents a financial account (e.g., Bank Account, Cash, Credit Card)."""
    
    def __init__(self, name: str, account_type: str, initial_balance: Decimal = Decimal('0')):
        """
        Initialize an account.
        
        Args:
            name: Account name
            account_type: Type of account (e.g., 'checking', 'savings', 'cash', 'credit_card')
            initial_balance: Starting balance
        """
        self.name = name
        self.account_type = account_type
        self.initial_balance = Decimal(str(initial_balance))
    
    def to_dict(self) -> Dict:
        """Convert account to dictionary."""
        return {
            'name': self.name,
            'account_type': self.account_type,
            'initial_balance': str(self.initial_balance)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Account':
        """Create account from dictionary."""
        return cls(
            data['name'],
            data['account_type'],
            Decimal(data['initial_balance'])
        )


class FinanceManager:
    """Main class for managing personal finances."""
    
    def __init__(self, data_file: str = 'data/finance_data.json'):
        """
        Initialize the finance manager.
        
        Args:
            data_file: Path to data storage file
        """
        self.data_file = Path(data_file)
        self.accounts: List[Account] = []
        self.transactions: List[Transaction] = []
        self.categories: List[Category] = []
        self._load_data()
    
    def _load_data(self):
        """Load data from file."""
        if not self.data_file.exists():
            self._initialize_default_data()
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.accounts = [Account.from_dict(a) for a in data.get('accounts', [])]
            self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
            self.categories = [Category.from_dict(c) for c in data.get('categories', [])]
        except Exception as e:
            print(f"Error loading data: {e}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize with default categories."""
        default_categories = [
            Category('Salary', 'income'),
            Category('Investment Income', 'income'),
            Category('Other Income', 'income'),
            Category('Food & Dining', 'expense'),
            Category('Transportation', 'expense'),
            Category('Housing', 'expense'),
            Category('Utilities', 'expense'),
            Category('Healthcare', 'expense'),
            Category('Entertainment', 'expense'),
            Category('Shopping', 'expense'),
            Category('Other Expense', 'expense'),
        ]
        self.categories = default_categories
    
    def save_data(self):
        """Save data to file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'accounts': [a.to_dict() for a in self.accounts],
            'transactions': [t.to_dict() for t in self.transactions],
            'categories': [c.to_dict() for c in self.categories]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_account(self, name: str, account_type: str, initial_balance: Decimal = Decimal('0')) -> Account:
        """Add a new account."""
        # Check if account already exists
        if any(a.name == name for a in self.accounts):
            raise ValueError(f"Account '{name}' already exists")
        
        account = Account(name, account_type, initial_balance)
        self.accounts.append(account)
        self.save_data()
        return account
    
    def add_transaction(self, date: datetime, description: str, amount: Decimal,
                       category: str, transaction_type: str, account: str) -> Transaction:
        """Add a new transaction."""
        # Validate account exists
        if not any(a.name == account for a in self.accounts):
            raise ValueError(f"Account '{account}' not found")
        
        # Validate category exists
        if not any(c.name == category for c in self.categories):
            raise ValueError(f"Category '{category}' not found")
        
        transaction = Transaction(date, description, amount, category, transaction_type, account)
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def add_category(self, name: str, category_type: str) -> Category:
        """Add a new category."""
        # Check if category already exists
        if any(c.name == name for c in self.categories):
            raise ValueError(f"Category '{name}' already exists")
        
        category = Category(name, category_type)
        self.categories.append(category)
        self.save_data()
        return category
    
    def get_account_balance(self, account_name: str) -> Decimal:
        """Calculate current balance for an account."""
        account = next((a for a in self.accounts if a.name == account_name), None)
        if not account:
            raise ValueError(f"Account '{account_name}' not found")
        
        balance = account.initial_balance
        
        for transaction in self.transactions:
            if transaction.account == account_name:
                if transaction.transaction_type == 'income':
                    balance += transaction.amount
                else:  # expense
                    balance -= transaction.amount
        
        return balance
    
    def get_transactions_by_account(self, account_name: str) -> List[Transaction]:
        """Get all transactions for an account."""
        return [t for t in self.transactions if t.account == account_name]
    
    def get_transactions_by_category(self, category_name: str) -> List[Transaction]:
        """Get all transactions for a category."""
        return [t for t in self.transactions if t.category == category_name]
    
    def get_transactions_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        """Get transactions within a date range."""
        return [t for t in self.transactions if start_date <= t.date <= end_date]
    
    def get_total_income(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> Decimal:
        """Calculate total income, optionally within a date range."""
        transactions = self.transactions
        
        if start_date and end_date:
            transactions = self.get_transactions_by_date_range(start_date, end_date)
        
        return sum(t.amount for t in transactions if t.transaction_type == 'income')
    
    def get_total_expenses(self, start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> Decimal:
        """Calculate total expenses, optionally within a date range."""
        transactions = self.transactions
        
        if start_date and end_date:
            transactions = self.get_transactions_by_date_range(start_date, end_date)
        
        return sum(t.amount for t in transactions if t.transaction_type == 'expense')
    
    def get_net_income(self, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> Decimal:
        """Calculate net income (income - expenses)."""
        return self.get_total_income(start_date, end_date) - self.get_total_expenses(start_date, end_date)
