"""
Unit tests for Tesouraria finance management system.
"""

import unittest
from datetime import datetime
from decimal import Decimal
import tempfile
import os
from pathlib import Path

from tesouraria.finance import (
    Account,
    Transaction,
    Category,
    FinanceManager
)


class TestCategory(unittest.TestCase):
    """Test Category class."""
    
    def test_create_income_category(self):
        """Test creating an income category."""
        cat = Category("Salary", "income")
        self.assertEqual(cat.name, "Salary")
        self.assertEqual(cat.category_type, "income")
    
    def test_create_expense_category(self):
        """Test creating an expense category."""
        cat = Category("Food", "expense")
        self.assertEqual(cat.name, "Food")
        self.assertEqual(cat.category_type, "expense")
    
    def test_invalid_category_type(self):
        """Test that invalid category type raises error."""
        with self.assertRaises(ValueError):
            Category("Test", "invalid")
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        cat = Category("Salary", "income")
        data = cat.to_dict()
        self.assertEqual(data['name'], "Salary")
        self.assertEqual(data['category_type'], "income")
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {'name': 'Food', 'category_type': 'expense'}
        cat = Category.from_dict(data)
        self.assertEqual(cat.name, "Food")
        self.assertEqual(cat.category_type, "expense")


class TestAccount(unittest.TestCase):
    """Test Account class."""
    
    def test_create_account_with_zero_balance(self):
        """Test creating an account with zero initial balance."""
        acc = Account("Checking", "checking")
        self.assertEqual(acc.name, "Checking")
        self.assertEqual(acc.account_type, "checking")
        self.assertEqual(acc.initial_balance, Decimal('0'))
    
    def test_create_account_with_initial_balance(self):
        """Test creating an account with initial balance."""
        acc = Account("Savings", "savings", Decimal('1000.50'))
        self.assertEqual(acc.initial_balance, Decimal('1000.50'))
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        acc = Account("Cash", "cash", Decimal('100'))
        data = acc.to_dict()
        self.assertEqual(data['name'], "Cash")
        self.assertEqual(data['account_type'], "cash")
        self.assertEqual(data['initial_balance'], '100')
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'name': 'Credit Card',
            'account_type': 'credit_card',
            'initial_balance': '0'
        }
        acc = Account.from_dict(data)
        self.assertEqual(acc.name, "Credit Card")
        self.assertEqual(acc.account_type, "credit_card")
        self.assertEqual(acc.initial_balance, Decimal('0'))


class TestTransaction(unittest.TestCase):
    """Test Transaction class."""
    
    def test_create_income_transaction(self):
        """Test creating an income transaction."""
        date = datetime(2025, 1, 15)
        trans = Transaction(
            date=date,
            description="Monthly Salary",
            amount=Decimal('5000'),
            category="Salary",
            transaction_type="income",
            account="Checking"
        )
        self.assertEqual(trans.description, "Monthly Salary")
        self.assertEqual(trans.amount, Decimal('5000'))
        self.assertEqual(trans.transaction_type, "income")
    
    def test_create_expense_transaction(self):
        """Test creating an expense transaction."""
        date = datetime(2025, 1, 16)
        trans = Transaction(
            date=date,
            description="Grocery Shopping",
            amount=Decimal('150.75'),
            category="Food",
            transaction_type="expense",
            account="Credit Card"
        )
        self.assertEqual(trans.description, "Grocery Shopping")
        self.assertEqual(trans.amount, Decimal('150.75'))
        self.assertEqual(trans.transaction_type, "expense")
    
    def test_invalid_transaction_type(self):
        """Test that invalid transaction type raises error."""
        with self.assertRaises(ValueError):
            Transaction(
                date=datetime.now(),
                description="Test",
                amount=Decimal('100'),
                category="Test",
                transaction_type="invalid",
                account="Test"
            )
    
    def test_amount_is_positive(self):
        """Test that amounts are stored as positive values."""
        trans = Transaction(
            date=datetime.now(),
            description="Test",
            amount=Decimal('-100'),
            category="Test",
            transaction_type="expense",
            account="Test"
        )
        self.assertEqual(trans.amount, Decimal('100'))
    
    def test_transaction_id_generated(self):
        """Test that transaction ID is generated automatically."""
        trans = Transaction(
            date=datetime.now(),
            description="Test",
            amount=Decimal('100'),
            category="Test",
            transaction_type="income",
            account="Test"
        )
        self.assertIsNotNone(trans.transaction_id)
        self.assertTrue(len(trans.transaction_id) > 0)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        date = datetime(2025, 1, 15, 10, 30)
        trans = Transaction(
            date=date,
            description="Test Transaction",
            amount=Decimal('100.50'),
            category="Test",
            transaction_type="income",
            account="Test Account"
        )
        data = trans.to_dict()
        self.assertEqual(data['description'], "Test Transaction")
        self.assertEqual(data['amount'], '100.50')
        self.assertEqual(data['transaction_type'], "income")
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'transaction_id': 'test-id-123',
            'date': '2025-01-15T10:30:00',
            'description': 'Test',
            'amount': '100.50',
            'category': 'Food',
            'transaction_type': 'expense',
            'account': 'Cash'
        }
        trans = Transaction.from_dict(data)
        self.assertEqual(trans.description, "Test")
        self.assertEqual(trans.amount, Decimal('100.50'))
        self.assertEqual(trans.transaction_type, "expense")


class TestFinanceManager(unittest.TestCase):
    """Test FinanceManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = FinanceManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            os.unlink(self.temp_file.name)
        except (OSError, FileNotFoundError):
            pass
    
    def test_initial_categories_created(self):
        """Test that default categories are created."""
        self.assertTrue(len(self.manager.categories) > 0)
        # Check for some default categories
        cat_names = [c.name for c in self.manager.categories]
        self.assertIn('Salary', cat_names)
        self.assertIn('Food & Dining', cat_names)
    
    def test_add_account(self):
        """Test adding a new account."""
        acc = self.manager.add_account("Test Account", "checking", Decimal('500'))
        self.assertEqual(acc.name, "Test Account")
        self.assertEqual(len(self.manager.accounts), 1)
    
    def test_add_duplicate_account(self):
        """Test that adding duplicate account raises error."""
        self.manager.add_account("Test", "checking")
        with self.assertRaises(ValueError):
            self.manager.add_account("Test", "savings")
    
    def test_add_transaction(self):
        """Test adding a transaction."""
        self.manager.add_account("Checking", "checking", Decimal('1000'))
        trans = self.manager.add_transaction(
            date=datetime.now(),
            description="Test Income",
            amount=Decimal('500'),
            category="Salary",
            transaction_type="income",
            account="Checking"
        )
        self.assertEqual(trans.description, "Test Income")
        self.assertEqual(len(self.manager.transactions), 1)
    
    def test_add_transaction_invalid_account(self):
        """Test that adding transaction to non-existent account raises error."""
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                date=datetime.now(),
                description="Test",
                amount=Decimal('100'),
                category="Salary",
                transaction_type="income",
                account="NonExistent"
            )
    
    def test_add_transaction_invalid_category(self):
        """Test that adding transaction with non-existent category raises error."""
        self.manager.add_account("Checking", "checking")
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                date=datetime.now(),
                description="Test",
                amount=Decimal('100'),
                category="NonExistentCategory",
                transaction_type="income",
                account="Checking"
            )
    
    def test_add_category(self):
        """Test adding a new category."""
        cat = self.manager.add_category("Custom Category", "expense")
        self.assertEqual(cat.name, "Custom Category")
        self.assertTrue(any(c.name == "Custom Category" for c in self.manager.categories))
    
    def test_add_duplicate_category(self):
        """Test that adding duplicate category raises error."""
        self.manager.add_category("Test Cat", "income")
        with self.assertRaises(ValueError):
            self.manager.add_category("Test Cat", "expense")
    
    def test_get_account_balance_zero(self):
        """Test getting balance of account with no transactions."""
        self.manager.add_account("Test", "checking", Decimal('500'))
        balance = self.manager.get_account_balance("Test")
        self.assertEqual(balance, Decimal('500'))
    
    def test_get_account_balance_with_income(self):
        """Test account balance calculation with income."""
        self.manager.add_account("Test", "checking", Decimal('1000'))
        self.manager.add_transaction(
            date=datetime.now(),
            description="Income",
            amount=Decimal('500'),
            category="Salary",
            transaction_type="income",
            account="Test"
        )
        balance = self.manager.get_account_balance("Test")
        self.assertEqual(balance, Decimal('1500'))
    
    def test_get_account_balance_with_expense(self):
        """Test account balance calculation with expense."""
        self.manager.add_account("Test", "checking", Decimal('1000'))
        self.manager.add_transaction(
            date=datetime.now(),
            description="Expense",
            amount=Decimal('200'),
            category="Food & Dining",
            transaction_type="expense",
            account="Test"
        )
        balance = self.manager.get_account_balance("Test")
        self.assertEqual(balance, Decimal('800'))
    
    def test_get_account_balance_mixed(self):
        """Test account balance with both income and expenses."""
        self.manager.add_account("Test", "checking", Decimal('1000'))
        self.manager.add_transaction(
            date=datetime.now(),
            description="Income",
            amount=Decimal('500'),
            category="Salary",
            transaction_type="income",
            account="Test"
        )
        self.manager.add_transaction(
            date=datetime.now(),
            description="Expense",
            amount=Decimal('300'),
            category="Food & Dining",
            transaction_type="expense",
            account="Test"
        )
        balance = self.manager.get_account_balance("Test")
        self.assertEqual(balance, Decimal('1200'))
    
    def test_get_account_balance_nonexistent(self):
        """Test that getting balance of non-existent account raises error."""
        with self.assertRaises(ValueError):
            self.manager.get_account_balance("NonExistent")
    
    def test_get_transactions_by_account(self):
        """Test filtering transactions by account."""
        self.manager.add_account("Account1", "checking")
        self.manager.add_account("Account2", "savings")
        
        self.manager.add_transaction(
            datetime.now(), "T1", Decimal('100'),
            "Salary", "income", "Account1"
        )
        self.manager.add_transaction(
            datetime.now(), "T2", Decimal('200'),
            "Salary", "income", "Account2"
        )
        
        trans = self.manager.get_transactions_by_account("Account1")
        self.assertEqual(len(trans), 1)
        self.assertEqual(trans[0].description, "T1")
    
    def test_get_transactions_by_category(self):
        """Test filtering transactions by category."""
        self.manager.add_account("Test", "checking")
        
        self.manager.add_transaction(
            datetime.now(), "Paycheck", Decimal('5000'),
            "Salary", "income", "Test"
        )
        self.manager.add_transaction(
            datetime.now(), "Groceries", Decimal('150'),
            "Food & Dining", "expense", "Test"
        )
        
        trans = self.manager.get_transactions_by_category("Salary")
        self.assertEqual(len(trans), 1)
        self.assertEqual(trans[0].description, "Paycheck")
    
    def test_get_transactions_by_date_range(self):
        """Test filtering transactions by date range."""
        self.manager.add_account("Test", "checking")
        
        date1 = datetime(2025, 1, 1)
        date2 = datetime(2025, 1, 15)
        date3 = datetime(2025, 2, 1)
        
        self.manager.add_transaction(
            date1, "T1", Decimal('100'),
            "Salary", "income", "Test"
        )
        self.manager.add_transaction(
            date2, "T2", Decimal('200'),
            "Salary", "income", "Test"
        )
        self.manager.add_transaction(
            date3, "T3", Decimal('300'),
            "Salary", "income", "Test"
        )
        
        trans = self.manager.get_transactions_by_date_range(
            datetime(2025, 1, 1),
            datetime(2025, 1, 31)
        )
        self.assertEqual(len(trans), 2)
    
    def test_get_total_income(self):
        """Test calculating total income."""
        self.manager.add_account("Test", "checking")
        
        self.manager.add_transaction(
            datetime.now(), "Income1", Decimal('5000'),
            "Salary", "income", "Test"
        )
        self.manager.add_transaction(
            datetime.now(), "Income2", Decimal('1000'),
            "Other Income", "income", "Test"
        )
        
        total = self.manager.get_total_income()
        self.assertEqual(total, Decimal('6000'))
    
    def test_get_total_expenses(self):
        """Test calculating total expenses."""
        self.manager.add_account("Test", "checking")
        
        self.manager.add_transaction(
            datetime.now(), "Expense1", Decimal('100'),
            "Food & Dining", "expense", "Test"
        )
        self.manager.add_transaction(
            datetime.now(), "Expense2", Decimal('50'),
            "Transportation", "expense", "Test"
        )
        
        total = self.manager.get_total_expenses()
        self.assertEqual(total, Decimal('150'))
    
    def test_get_net_income(self):
        """Test calculating net income."""
        self.manager.add_account("Test", "checking")
        
        self.manager.add_transaction(
            datetime.now(), "Income", Decimal('5000'),
            "Salary", "income", "Test"
        )
        self.manager.add_transaction(
            datetime.now(), "Expense", Decimal('2000'),
            "Food & Dining", "expense", "Test"
        )
        
        net = self.manager.get_net_income()
        self.assertEqual(net, Decimal('3000'))
    
    def test_save_and_load_data(self):
        """Test saving and loading data."""
        # Add some data
        self.manager.add_account("Savings", "savings", Decimal('1000'))
        self.manager.add_transaction(
            datetime(2025, 1, 1), "Test", Decimal('500'),
            "Salary", "income", "Savings"
        )
        
        # Create new manager with same file
        manager2 = FinanceManager(self.temp_file.name)
        
        # Verify data was loaded
        self.assertEqual(len(manager2.accounts), 1)
        self.assertEqual(manager2.accounts[0].name, "Savings")
        self.assertEqual(len(manager2.transactions), 1)
        self.assertEqual(manager2.transactions[0].description, "Test")


if __name__ == '__main__':
    unittest.main()
