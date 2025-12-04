"""Tesouraria package initialization."""

from .finance import (
    Account,
    Transaction,
    Category,
    FinanceManager
)

__all__ = ['Account', 'Transaction', 'Category', 'FinanceManager']
__version__ = '1.0.0'
