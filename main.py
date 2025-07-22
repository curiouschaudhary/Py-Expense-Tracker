from expense_manager import ExpenseManager
from reports import ExpenseReports
from datetime import datetime

def print_menu():
    """Print the main menu"""
    print("\n=== Expense Tracker Menu ===")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Generate Summary Report")
    print("4. Generate Category Pie Chart")
    print("5. Generate Monthly Report")
    print("6. Generate Detailed Report")
    print("7. Exit")
    print("=========================")

def get_valid_amount():
    """Get a valid amount from user input"""
    while True:
        try:
            amount = float(input("Enter amount: ₹"))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")

def get_date_input(prompt):
    """Get a valid date from user input"""
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

def main():
    expense_manager = ExpenseManager()
    reports = ExpenseReports(expense_manager)
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            category = input("Enter category: ")
            amount = get_valid_amount()
            description = input("Enter description (optional): ")
            
            if expense_manager.add_expense(category, amount, description):
                print("Expense added successfully!")
            else:
                print("Failed to add expense.")
                
        elif choice == "2":
            expenses = expense_manager.get_all_expenses()
            if not expenses:
                print("No expenses found.")
            else:
                print("\nAll Expenses:")
                for expense in expenses:
                    print(f"Date: {expense[1]}, Category: {expense[2]}, Amount: ₹{expense[3]:.2f}, Description: {expense[4]}")
                    
        elif choice == "3":
            print(reports.generate_summary_report())
            
        elif choice == "4":
            result = reports.generate_category_pie_chart()
            print(result)
            
        elif choice == "5":
            print(reports.generate_monthly_report())
            
        elif choice == "6":
            start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
            end_date = get_date_input("Enter end date (YYYY-MM-DD): ")
            print(reports.generate_detailed_report(start_date, end_date))
            
        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 