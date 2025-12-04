#!/usr/bin/env python3
"""
Tesouraria CLI - Command Line Interface for Personal Finance Accounting
"""

import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from tesouraria.finance import FinanceManager


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_menu():
    """Display the main menu."""
    print_header("TESOURARIA - Personal Finance Manager")
    print("\n1. Manage Accounts")
    print("2. Manage Transactions")
    print("3. View Reports")
    print("4. Manage Categories")
    print("0. Exit")
    print()


def manage_accounts(manager: FinanceManager):
    """Account management submenu."""
    while True:
        print_header("Account Management")
        print("\n1. List Accounts")
        print("2. Add Account")
        print("3. View Account Balance")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            list_accounts(manager)
        elif choice == '2':
            add_account(manager)
        elif choice == '3':
            view_account_balance(manager)
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def list_accounts(manager: FinanceManager):
    """List all accounts."""
    if not manager.accounts:
        print("\nNo accounts found.")
        return
    
    print("\n" + "-" * 60)
    print(f"{'Account Name':<25} {'Type':<20} {'Initial Balance':>14}")
    print("-" * 60)
    
    for account in manager.accounts:
        print(f"{account.name:<25} {account.account_type:<20} ${account.initial_balance:>13.2f}")
    
    print("-" * 60)


def add_account(manager: FinanceManager):
    """Add a new account."""
    print("\n--- Add New Account ---")
    
    name = input("Account name: ").strip()
    if not name:
        print("Account name cannot be empty.")
        return
    
    account_type = input("Account type (checking/savings/cash/credit_card): ").strip()
    if not account_type:
        print("Account type cannot be empty.")
        return
    
    try:
        initial_balance = Decimal(input("Initial balance (default 0): ").strip() or "0")
    except InvalidOperation:
        print("Invalid balance amount.")
        return
    
    try:
        manager.add_account(name, account_type, initial_balance)
        print(f"\n✓ Account '{name}' created successfully!")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def view_account_balance(manager: FinanceManager):
    """View balance for a specific account."""
    if not manager.accounts:
        print("\nNo accounts found. Please create an account first.")
        return
    
    print("\n--- Account Balance ---")
    list_accounts(manager)
    
    account_name = input("\nEnter account name: ").strip()
    
    try:
        balance = manager.get_account_balance(account_name)
        print(f"\nCurrent balance for '{account_name}': ${balance:.2f}")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def manage_transactions(manager: FinanceManager):
    """Transaction management submenu."""
    while True:
        print_header("Transaction Management")
        print("\n1. List Transactions")
        print("2. Add Transaction")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            list_transactions(manager)
        elif choice == '2':
            add_transaction(manager)
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def list_transactions(manager: FinanceManager):
    """List all transactions."""
    if not manager.transactions:
        print("\nNo transactions found.")
        return
    
    print("\n" + "-" * 100)
    print(f"{'Date':<12} {'Description':<25} {'Category':<18} {'Type':<8} {'Amount':>12} {'Account':<20}")
    print("-" * 100)
    
    for transaction in sorted(manager.transactions, key=lambda t: t.date, reverse=True):
        amount_str = f"${transaction.amount:.2f}"
        print(f"{transaction.date.strftime('%Y-%m-%d'):<12} "
              f"{transaction.description[:24]:<25} "
              f"{transaction.category[:17]:<18} "
              f"{transaction.transaction_type:<8} "
              f"{amount_str:>12} "
              f"{transaction.account[:19]:<20}")
    
    print("-" * 100)


def add_transaction(manager: FinanceManager):
    """Add a new transaction."""
    if not manager.accounts:
        print("\nNo accounts found. Please create an account first.")
        return
    
    print("\n--- Add New Transaction ---")
    
    # Date
    date_str = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if not date_str:
        date = datetime.now()
    else:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format.")
            return
    
    # Description
    description = input("Description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return
    
    # Transaction type
    print("\nTransaction type:")
    print("1. Income")
    print("2. Expense")
    type_choice = input("Select (1 or 2): ").strip()
    
    if type_choice == '1':
        transaction_type = 'income'
    elif type_choice == '2':
        transaction_type = 'expense'
    else:
        print("Invalid transaction type.")
        return
    
    # Category
    print("\nAvailable categories:")
    categories = [c for c in manager.categories if c.category_type == transaction_type]
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat.name}")
    
    try:
        cat_idx = int(input("Select category number: ").strip()) - 1
        if cat_idx < 0 or cat_idx >= len(categories):
            print("Invalid category selection.")
            return
        category = categories[cat_idx].name
    except ValueError:
        print("Invalid input.")
        return
    
    # Amount
    try:
        amount = Decimal(input("Amount: ").strip())
        if amount <= 0:
            print("Amount must be positive.")
            return
    except InvalidOperation:
        print("Invalid amount.")
        return
    
    # Account
    print("\nAvailable accounts:")
    for i, acc in enumerate(manager.accounts, 1):
        print(f"{i}. {acc.name}")
    
    try:
        acc_idx = int(input("Select account number: ").strip()) - 1
        if acc_idx < 0 or acc_idx >= len(manager.accounts):
            print("Invalid account selection.")
            return
        account = manager.accounts[acc_idx].name
    except ValueError:
        print("Invalid input.")
        return
    
    try:
        manager.add_transaction(date, description, amount, category, transaction_type, account)
        print(f"\n✓ Transaction added successfully!")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def view_reports(manager: FinanceManager):
    """View financial reports."""
    while True:
        print_header("Financial Reports")
        print("\n1. Account Balances Summary")
        print("2. Income vs Expenses")
        print("3. Category Breakdown")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            account_balances_summary(manager)
        elif choice == '2':
            income_vs_expenses(manager)
        elif choice == '3':
            category_breakdown(manager)
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def account_balances_summary(manager: FinanceManager):
    """Show summary of all account balances."""
    if not manager.accounts:
        print("\nNo accounts found.")
        return
    
    print("\n" + "-" * 60)
    print(f"{'Account Name':<30} {'Current Balance':>20}")
    print("-" * 60)
    
    total = Decimal('0')
    for account in manager.accounts:
        balance = manager.get_account_balance(account.name)
        total += balance
        print(f"{account.name:<30} ${balance:>19.2f}")
    
    print("-" * 60)
    print(f"{'TOTAL':<30} ${total:>19.2f}")
    print("-" * 60)


def income_vs_expenses(manager: FinanceManager):
    """Show income vs expenses report."""
    print("\n--- Income vs Expenses Report ---")
    
    total_income = manager.get_total_income()
    total_expenses = manager.get_total_expenses()
    net_income = manager.get_net_income()
    
    print(f"\nTotal Income:    ${total_income:>12.2f}")
    print(f"Total Expenses:  ${total_expenses:>12.2f}")
    print("-" * 35)
    print(f"Net Income:      ${net_income:>12.2f}")
    print()


def category_breakdown(manager: FinanceManager):
    """Show spending by category."""
    if not manager.transactions:
        print("\nNo transactions found.")
        return
    
    print("\n--- Category Breakdown ---")
    
    # Income categories
    print("\nIncome by Category:")
    print("-" * 40)
    income_by_cat = {}
    for transaction in manager.transactions:
        if transaction.transaction_type == 'income':
            if transaction.category not in income_by_cat:
                income_by_cat[transaction.category] = Decimal('0')
            income_by_cat[transaction.category] += transaction.amount
    
    for category, amount in sorted(income_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"{category:<25} ${amount:>12.2f}")
    
    # Expense categories
    print("\nExpenses by Category:")
    print("-" * 40)
    expense_by_cat = {}
    for transaction in manager.transactions:
        if transaction.transaction_type == 'expense':
            if transaction.category not in expense_by_cat:
                expense_by_cat[transaction.category] = Decimal('0')
            expense_by_cat[transaction.category] += transaction.amount
    
    for category, amount in sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"{category:<25} ${amount:>12.2f}")
    print()


def manage_categories(manager: FinanceManager):
    """Category management submenu."""
    while True:
        print_header("Category Management")
        print("\n1. List Categories")
        print("2. Add Category")
        print("0. Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            list_categories(manager)
        elif choice == '2':
            add_category(manager)
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def list_categories(manager: FinanceManager):
    """List all categories."""
    if not manager.categories:
        print("\nNo categories found.")
        return
    
    print("\n--- Income Categories ---")
    income_cats = [c for c in manager.categories if c.category_type == 'income']
    for cat in income_cats:
        print(f"  • {cat.name}")
    
    print("\n--- Expense Categories ---")
    expense_cats = [c for c in manager.categories if c.category_type == 'expense']
    for cat in expense_cats:
        print(f"  • {cat.name}")
    print()


def add_category(manager: FinanceManager):
    """Add a new category."""
    print("\n--- Add New Category ---")
    
    name = input("Category name: ").strip()
    if not name:
        print("Category name cannot be empty.")
        return
    
    print("\nCategory type:")
    print("1. Income")
    print("2. Expense")
    type_choice = input("Select (1 or 2): ").strip()
    
    if type_choice == '1':
        category_type = 'income'
    elif type_choice == '2':
        category_type = 'expense'
    else:
        print("Invalid category type.")
        return
    
    try:
        manager.add_category(name, category_type)
        print(f"\n✓ Category '{name}' created successfully!")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main application entry point."""
    manager = FinanceManager()
    
    while True:
        print_menu()
        choice = input("Select option: ").strip()
        
        if choice == '1':
            manage_accounts(manager)
        elif choice == '2':
            manage_transactions(manager)
        elif choice == '3':
            view_reports(manager)
        elif choice == '4':
            manage_categories(manager)
        elif choice == '0':
            print("\nThank you for using Tesouraria!")
            sys.exit(0)
        else:
            print("\nInvalid option. Please try again.")


if __name__ == '__main__':
    main()
