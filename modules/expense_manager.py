import sqlite3
from dataclasses import dataclass
from datetime import date
from modules.database import get_connection


@dataclass
class Transaction:
    id: int
    amount: float
    category_id: int
    description: str
    date: str
    type: str  # 'expense' | 'income'


class ExpenseManager:

    def __init__(self):
        self.conn = get_connection()

    def add_transaction(
        self,
        amount: float,
        category_id: int,
        description: str,
        date: str,
        type: str
    ) -> Transaction:
        # TODO: viết câu INSERT, dùng cursor.lastrowid để lấy id vừa tạo
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (amount, category_id, description, date, type)
            VALUES (?, ?, ?, ?, ?)
        """, (amount, category_id, description, date, type))
        self.conn.commit()
        transaction_id = cursor.lastrowid
        return Transaction(
            id=transaction_id,
            amount=amount,
            category_id=category_id,
            description=description,
            date=date,
            type=type
        )

    def get_transactions(self, filters: dict = {}) -> list[Transaction]:
        # TODO: viết câu SELECT, xử lý filters
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if "category_id" in filters:
            query += " AND category_id = ?"
            params.append(filters["category_id"])

        if "month" in filters:
            query += " AND date LIKE ?"
            params.append(f"{filters['month']}%")
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        transactions = []
        for row in rows:
            transactions.append(Transaction(
                # Thay row[0], row[1]... thành:
                id=row["id"],
                amount=row["amount"],
                category_id=row["category_id"],
                description=row["description"],
                date=row["date"],
                type=row["type"]
            ))
        return transactions

    def update_transaction(self, id: int, **kwargs) -> bool:
        # TODO: viết câu UPDATE, xử lý kwargs, 
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        params = list(kwargs.values()) + [id]
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE transactions SET {set_clause} WHERE id = ?", params)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_transaction(self, id: int) -> bool:
        # TODO: viết câu DELETE, 
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self):
        self.conn.close()
