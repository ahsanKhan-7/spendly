import calendar
import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "spendly.db",
)

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    def day_in_month(day_of_month):
        return date(today.year, today.month, min(day_of_month, last_day))

    sample_expenses = [
        (user_id, 12.50, "Food", day_in_month(2), "Groceries"),
        (user_id, 8.75, "Food", day_in_month(18), "Lunch"),
        (user_id, 45.00, "Transport", day_in_month(4), "Fuel"),
        (user_id, 120.00, "Bills", day_in_month(6), "Electricity bill"),
        (user_id, 60.00, "Health", day_in_month(10), "Pharmacy"),
        (user_id, 25.00, "Entertainment", day_in_month(14), "Movie tickets"),
        (user_id, 90.00, "Shopping", day_in_month(20), "New shoes"),
        (user_id, 15.00, "Other", day_in_month(24), "Miscellaneous"),
    ]
    conn.executemany(
        """
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (uid, amount, category, d.isoformat(), description)
            for uid, amount, category, d, description in sample_expenses
        ],
    )
    conn.commit()
    conn.close()
