#!/usr/bin/env python3
"""
Example script demonstrating Tesouraria usage.
This script creates sample accounts and transactions to show the system in action.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from tesouraria import FinanceManager


def main():
    print("=" * 60)
    print("  Tesouraria - Personal Finance Accounting Demo")
    print("=" * 60)
    
    # Initialize manager with a demo data file
    manager = FinanceManager('data/demo_finance_data.json')
    
    print("\n1. Creating accounts...")
    
    # Create accounts
    try:
        manager.add_account("Main Checking", "checking", Decimal('2500.00'))
        print("   ✓ Created 'Main Checking' account with $2,500.00")
    except ValueError:
        print("   • Account 'Main Checking' already exists")
    
    try:
        manager.add_account("Savings", "savings", Decimal('10000.00'))
        print("   ✓ Created 'Savings' account with $10,000.00")
    except ValueError:
        print("   • Account 'Savings' already exists")
    
    try:
        manager.add_account("Cash", "cash", Decimal('200.00'))
        print("   ✓ Created 'Cash' account with $200.00")
    except ValueError:
        print("   • Account 'Cash' already exists")
    
    print("\n2. Adding sample transactions...")
    
    # Add some transactions
    today = datetime.now()
    
    transactions = [
        (today - timedelta(days=30), "Monthly Salary", Decimal('5000'), "Salary", "income", "Main Checking"),
        (today - timedelta(days=25), "Grocery Shopping", Decimal('150.75'), "Food & Dining", "expense", "Main Checking"),
        (today - timedelta(days=20), "Gas Station", Decimal('45.00'), "Transportation", "expense", "Cash"),
        (today - timedelta(days=15), "Electric Bill", Decimal('120.50'), "Utilities", "expense", "Main Checking"),
        (today - timedelta(days=10), "Restaurant Dinner", Decimal('85.00'), "Food & Dining", "expense", "Main Checking"),
        (today - timedelta(days=5), "Movie Tickets", Decimal('30.00'), "Entertainment", "expense", "Cash"),
        (today - timedelta(days=3), "Freelance Work", Decimal('500.00'), "Other Income", "income", "Main Checking"),
        (today - timedelta(days=1), "Coffee Shop", Decimal('15.50'), "Food & Dining", "expense", "Cash"),
    ]
    
    for date, desc, amount, cat, trans_type, account in transactions:
        try:
            manager.add_transaction(date, desc, amount, cat, trans_type, account)
            symbol = "+" if trans_type == "income" else "-"
            print(f"   ✓ {symbol}${amount:>7.2f} - {desc:<25} ({account})")
        except ValueError as e:
            # Transaction might already exist
            pass
    
    print("\n3. Account Balances:")
    print("-" * 60)
    
    total = Decimal('0')
    for account in manager.accounts:
        balance = manager.get_account_balance(account.name)
        total += balance
        print(f"   {account.name:<25} ${balance:>12.2f}")
    
    print("-" * 60)
    print(f"   {'TOTAL NET WORTH':<25} ${total:>12.2f}")
    
    print("\n4. Financial Summary:")
    print("-" * 60)
    
    total_income = manager.get_total_income()
    total_expenses = manager.get_total_expenses()
    net_income = manager.get_net_income()
    
    print(f"   Total Income:    ${total_income:>12.2f}")
    print(f"   Total Expenses:  ${total_expenses:>12.2f}")
    print("-" * 60)
    print(f"   Net Income:      ${net_income:>12.2f}")
    
    print("\n5. Expense Breakdown by Category:")
    print("-" * 60)
    
    expense_by_cat = {}
    for transaction in manager.transactions:
        if transaction.transaction_type == 'expense':
            if transaction.category not in expense_by_cat:
                expense_by_cat[transaction.category] = Decimal('0')
            expense_by_cat[transaction.category] += transaction.amount
    
    for category, amount in sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        print(f"   {category:<25} ${amount:>10.2f}  ({percentage:>5.1f}%)")
    
    print("\n" + "=" * 60)
    print("Demo completed! Data saved to data/demo_finance_data.json")
    print("\nTo view/edit this data interactively, run:")
    print("  python -m tesouraria.cli")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
