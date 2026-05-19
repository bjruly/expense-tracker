import sqlite3
from modules.database import get_connection


class Analytics:
    """Thống kê và tổng hợp dữ liệu chi tiêu."""

    def __init__(self, conn=None):
        self.conn = conn if conn is not None else get_connection()

    def monthly_summary(self, month: str) -> dict:
        
        pass

    def category_breakdown(self, month: str) -> list[dict]:
        """Chi tiêu theo từng danh mục trong tháng."""
        # TODO
        pass

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