import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta

class ExpenseReports:
    def __init__(self, expense_manager):
        self.expense_manager = expense_manager

    def generate_summary_report(self):
        """Generate a summary report of all expenses"""
        expenses = self.expense_manager.get_all_expenses()
        if not expenses:
            return "No expenses found."

        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(expenses, columns=['id', 'date', 'category', 'amount', 'description', 'created_at'])
        
        # Calculate totals
        total_expenses = df['amount'].sum()
        category_totals = df.groupby('category')['amount'].sum()
        
        # Create report
        report = []
        report.append("=== Expense Summary Report ===")
        report.append(f"Total Expenses: ₹{total_expenses:.2f}")
        report.append("\nCategory Breakdown:")
        
        for category, amount in category_totals.items():
            percentage = (amount / total_expenses) * 100
            report.append(f"{category}: ₹{amount:.2f} ({percentage:.1f}%)")
            
        return "\n".join(report)

    def generate_category_pie_chart(self):
        """Generate a pie chart of expenses by category"""
        category_totals = self.expense_manager.calculate_category_totals()
        
        if not category_totals:
            return "No expenses found to generate chart."

        plt.figure(figsize=(10, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.axis('equal')
        
        # Save the chart
        plt.savefig('expense_categories.png')
        plt.close()
        
        return "Chart saved as 'expense_categories.png'"

    def generate_monthly_report(self):
        """Generate a monthly report of expenses"""
        expenses = self.expense_manager.get_all_expenses()
        if not expenses:
            return "No expenses found."

        df = pd.DataFrame(expenses, columns=['id', 'date', 'category', 'amount', 'description', 'created_at'])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        monthly_totals = df.groupby('month')['amount'].sum()
        
        report = []
        report.append("=== Monthly Expense Report ===")
        for month, total in monthly_totals.items():
            report.append(f"{month}: ₹{total:.2f}")
            
        return "\n".join(report)

    def generate_detailed_report(self, start_date=None, end_date=None):
        """Generate a detailed report of expenses"""
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        expenses = self.expense_manager.get_expenses_by_date_range(start_date, end_date)
        
        if not expenses:
            return f"No expenses found between {start_date} and {end_date}."

        # Convert to DataFrame
        df = pd.DataFrame(expenses, columns=['id', 'date', 'category', 'amount', 'description', 'created_at'])
        
        # Format the report
        report = []
        report.append(f"=== Detailed Expense Report ({start_date} to {end_date}) ===")
        report.append(tabulate(df[['date', 'category', 'amount', 'description']], 
                             headers=['Date', 'Category', 'Amount (₹)', 'Description'],
                             tablefmt='grid'))
        
        total = df['amount'].sum()
        report.append(f"\nTotal Expenses: ₹{total:.2f}")
        
        return "\n".join(report) 