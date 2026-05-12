import sqlite3
import pytest
from modules.database import create_tables
from modules.expense_manager import ExpenseManager

@pytest.fixture
def manager():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    m = ExpenseManager(conn=conn)
    yield m
    m.close()
def test_add_transaction(manager):
    transaction = manager.add_transaction(
        amount=100.0,
        category_id=1,
        description="Test transaction",
        date="2024-06-01",
        type="expense"
    )
    assert transaction.id is not None
    assert transaction.amount == 100.0
    assert transaction.category_id == 1
    assert transaction.description == "Test transaction"
    assert transaction.date == "2024-06-01"
    assert transaction.type == "expense"
def test_get_transactions(manager):
    manager.add_transaction(
        amount=100.0,
        category_id=1,
        description="Test transaction 1",
        date="2024-06-01",
        type="expense"
    )
    manager.add_transaction(
        amount=200.0,
        category_id=2,
        description="Test transaction 2",
        date="2024-06-02",
        type="income"
    )
    transactions = manager.get_transactions()
    assert len(transactions) == 2
    assert transactions[0].description == "Test transaction 1"
    assert transactions[1].description == "Test transaction 2"
def test_update_transaction(manager):
    transaction = manager.add_transaction(
        amount=100.0,
        category_id=1,
        description="Test transaction",
        date="2024-06-01",
        type="expense"
    )
    result = manager.update_transaction(transaction.id, amount=150.0)
    assert result is True
    transactions = manager.get_transactions()
    assert len(transactions) == 1
    assert transactions[0].amount == 150.0
def test_delete_transaction(manager):
    transaction = manager.add_transaction(
        amount=100.0,
        category_id=1,
        description="Test transaction",
        date="2024-06-01",
        type="expense"
    )
    manager.delete_transaction(transaction.id)
    transactions = manager.get_transactions()
    assert len(transactions) == 0  