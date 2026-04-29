import sqlite3
import os
from pathlib import Path

DB_PATH = Path("data/expense.db")

def get_connection() -> sqlite3.Connection:
    os.makedirs(DB_PATH.parent, exist_ok=True) 

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def create_tables() -> None:

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            icon TEXT,
            color TEXT);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL REFERENCES categories(id),
            month TEXT NOT NULL,
            monthly_limit REAL NOT NULL);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL REFERENCES categories(id),
            date TEXT NOT NULL,
            description TEXT,
            type TEXT NOT NULL CHECK (type IN ('expense', 'income')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        """)
    conn.commit()
    conn.close()

def seed_default_categories() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM categories")
    count = cursor.fetchone()[0]

    if count == 0:
        categories = [
            ("Food and drinks",     "🍜", "#FF6B6B"),
            ("Transportation",   "🚗", "#4ECDC4"),
            ("Shopping",     "🛍️", "#45B7D1"),
            ("Entertainment",    "🎮", "#96CEB4"),
            ("Health",    "💊", "#FFEAA7"),
            ("Education",     "📚", "#DDA0DD"),
            ("Utilities",     "💡", "#98D8C8"),
            ("Other",        "📦", "#B0B0B0"),
        ]
        cursor.executemany("INSERT INTO categories (name, icon, color) VALUES (?, ?, ?)", categories)
    conn.commit()
    conn.close()

def initialize_database() -> None:
    create_tables()
    seed_default_categories()
    print("Database initialized successfully.")