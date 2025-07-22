import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        self.close()

    def add_expense(self, date, category, amount, description=""):
        """Add a new expense to the database"""
        self.connect()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO expenses (date, category, amount, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, category, amount, description, created_at))
        self.conn.commit()
        self.close()

    def get_all_expenses(self):
        """Retrieve all expenses from the database"""
        self.connect()
        self.cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = self.cursor.fetchall()
        self.close()
        return expenses

    def get_expenses_by_category(self, category):
        """Retrieve expenses for a specific category"""
        self.connect()
        self.cursor.execute('SELECT * FROM expenses WHERE category = ? ORDER BY date DESC', (category,))
        expenses = self.cursor.fetchall()
        self.close()
        return expenses

    def get_expenses_by_date_range(self, start_date, end_date):
        """Retrieve expenses within a date range"""
        self.connect()
        self.cursor.execute('''
            SELECT * FROM expenses 
            WHERE date BETWEEN ? AND ? 
            ORDER BY date DESC
        ''', (start_date, end_date))
        expenses = self.cursor.fetchall()
        self.close()
        return expenses

    def get_categories(self):
        """Get all unique categories"""
        self.connect()
        self.cursor.execute('SELECT DISTINCT category FROM expenses')
        categories = [row[0] for row in self.cursor.fetchall()]
        self.close()
        return categories 