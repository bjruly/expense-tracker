import sqlite3
from modules.database import get_connection


class Analytics:
    """Thống kê và tổng hợp dữ liệu chi tiêu."""

    def __init__(self, conn=None):
        self.conn = conn if conn is not None else get_connection()

    def monthly_summary(self, month: str) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
            SUM(case when type = 'expense' then amount else 0 end) as expense,
            SUM(case when type = 'income' then amount else 0 end) as income
            FROM transactions
            WHERE strftime('%Y-%m', date) = ?
            """, (month,))
        result = cursor.fetchone()
        balance = (result[1] or 0.0) - (result[0] or 0.0)
        return {"expense": result[0] or 0.0, "income": result[1] or 0.0, "balance": balance}

    def category_breakdown(self, month: str) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT categories.name , SUM(transactions.amount) as total
            FROM transactions
            JOIN categories ON transactions.category_id = categories.id
            WHERE transactions.date LIKE ?
            AND transactions.type = 'expense'
            GROUP BY categories.name
            ORDER BY total DESC

        """, (f"{month}%",))
        return [{"category": row[0], "total": row[1]} for row in cursor.fetchall()]

    def daily_spending(self, month: str) -> list[dict]:
        """Chi tiêu theo từng ngày trong tháng."""
        # TODO
        pass

    def compare_months(self, m1: str, m2: str) -> dict:
        """So sánh tổng chi tiêu giữa 2 tháng."""
        # TODO
        pass

    def close(self):
        self.conn.close()