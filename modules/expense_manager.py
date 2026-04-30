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
        pass

    def get_transactions(self, filters: dict = {}) -> list[Transaction]:
        # TODO: viết câu SELECT, xử lý filters
        pass

    def update_transaction(self, id: int, **kwargs) -> bool:
        # TODO: viết câu UPDATE
        pass

    def delete_transaction(self, id: int) -> bool:
        # TODO: viết câu DELETE
        pass

    def close(self):
        self.conn.close()