from datetime import datetime
from database import Database

class ExpenseManager:
    def __init__(self):
        self.db = Database()

    def add_expense(self, category, amount, description=""):
        """Add a new expense"""
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_expense(date, category, amount, description)
            return True
        except ValueError as e:
            print(f"Error adding expense: {str(e)}")
            return False

    def get_all_expenses(self):
        """Get all expenses"""
        return self.db.get_all_expenses()

    def get_expenses_by_category(self, category):
        """Get expenses for a specific category"""
        return self.db.get_expenses_by_category(category)

    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a date range"""
        return self.db.get_expenses_by_date_range(start_date, end_date)

    def get_categories(self):
        """Get all expense categories"""
        return self.db.get_categories()

    def calculate_total_expenses(self, expenses=None):
        """Calculate total expenses"""
        if expenses is None:
            expenses = self.get_all_expenses()
        return sum(expense[3] for expense in expenses)

    def calculate_category_totals(self):
        """Calculate total expenses per category"""
        categories = self.get_categories()
        category_totals = {}
        
        for category in categories:
            expenses = self.get_expenses_by_category(category)
            total = self.calculate_total_expenses(expenses)
            category_totals[category] = total
            
        return category_totals 