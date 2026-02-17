#damn
# ============================================================
# EXPENSE CLASS - Stores one single expense
# ============================================================
class Expense:
    # Define the Expense class to store one expense
    def __init__(self, amount, category, date_str, note=""):
        # Constructor that creates an Expense object with basic fields
        self.amount = float(amount)  # Store amount as float for arithmetic
        self.category = str(category).strip()  # Store category as trimmed string
        self.date = str(date_str).strip()  # Store date as string "YYYY-MM-DD"
        self.note = str(note).strip()  # Store optional note about the expense

    # Convert self.date "YYYY-MM-DD" into tuple of ints (year, month, day)
    def date_tuple(self):
        # Split the date string by hyphen
        parts = self.date.split("-")
        # Check if date format seems wrong
        if len(parts) != 3:
            # Return a default invalid tuple if format wrong
            return (0, 0, 0)
        # Parse year as integer
        year = int(parts[0])
        # Parse month as integer
        month = int(parts[1])
        # Parse day as integer
        day = int(parts[2])
        # Return the tuple (year, month, day)
        return (year, month, day)

    # Convert this Expense to a dictionary for easy viewing
    def to_dict(self):
        # Return dictionary with all expense details
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

    # String representation used when printing an Expense object
    def __repr__(self):
        # Return formatted string showing expense details
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}', note='{self.note}')"


# ============================================================
# EXPENSE MANAGER CLASS - Manages all expenses
# ============================================================
class ExpenseManager:
    # Manager class to store multiple expenses and analyze them
    def __init__(self):
        # Constructor initializes an empty list of expenses
        self.expenses = []  # List will hold Expense objects
        self.categories = set()  # Set keeps unique category names

    # Add an Expense object to the manager
    def add_expense(self, expense):
        # Ensure input is Expense instance
        if not isinstance(expense, Expense):
            # Raise error on wrong type
            raise TypeError("add_expense expects an Expense object")
        # Append expense to the list
        self.expenses.append(expense)
        # Add category to the categories set
        self.categories.add(expense.category)

    # Remove an expense using its index in the list
    def remove_expense_by_index(self, index):
        # Check index validity
        if index < 0 or index >= len(self.expenses):
            # Raise when invalid index
            raise IndexError("Index out of range")
        # Remove and get the removed Expense object
        removed = self.expenses.pop(index)
        # Rebuild categories because removal might remove last of a category
        self._rebuild_categories()
        # Return the removed expense for confirmation
        return removed

    # Internal helper to rebuild the categories set from current expenses
    def _rebuild_categories(self):
        # Start with empty set
        new_set = set()
        # Iterate over all expenses
        for e in self.expenses:
            # Add category from each expense
            new_set.add(e.category)
        # Replace categories set with new set
        self.categories = new_set

    # Return a list of dictionaries for all expenses for easy reading
    def list_expenses(self):
        # Convert each expense to dict
        return [e.to_dict() for e in self.expenses]

    # Return all expenses that match a specific category string
    def filter_by_category(self, category):
        # Case-insensitive match
        return [e for e in self.expenses if e.category.lower() == category.lower()]

    # Return all expenses that happened in a given year and month
    def filter_by_month(self, year, month):
        # Prepare container list
        result = []
        # Check each expense
        for e in self.expenses:
            # Get year and month from date
            y, m, _ = e.date_tuple()
            # If both match
            if y == year and m == month:
                # Add to result list
                result.append(e)
        # Return the filtered list
        return result

    # Compute total amount spent across all expenses
    def total_spent(self):
        # Start total at 0.0
        total = 0.0
        # Iterate expenses
        for e in self.expenses:
            # Add each amount to total
            total += e.amount
        # Return the sum
        return total

    # Compute total amount per category and return as a dict
    def total_by_category(self):
        # Dictionary where key=category, value=sum
        totals = {}
        # Iterate expenses
        for e in self.expenses:
            # If category not seen yet
            if e.category not in totals:
                # Initialize category sum to 0.0
                totals[e.category] = 0.0
            # Add amount to that category
            totals[e.category] += e.amount
        # Return the dictionary of totals per category
        return totals

    # Return the top n expenses by amount as a list
    def top_expenses(self, n=3):
        # Sort descending by amount
        sorted_expenses = sorted(self.expenses, key=lambda x: x.amount, reverse=True)
        # Return first n items from sorted list
        return sorted_expenses[:n]

    # Return a nested dict { (year, month): total_amount } to see spend per month
    def monthly_summary(self):
        # Dictionary to hold month keys and totals
        summary = {}
        # Iterate all expenses
        for e in self.expenses:
            # Extract year and month
            y, m, _ = e.date_tuple()
            # Use tuple (year, month) as key
            key = (y, m)
            # If key not present
            if key not in summary:
                # Initialize month's sum to 0.0
                summary[key] = 0.0
            # Add amount to the month's total
            summary[key] += e.amount
        # Return the monthly totals dictionary
        return summary

    # Compute average expense amount across all expenses
    def average_expense(self):
        # Number of expenses
        count = len(self.expenses)
        # Avoid division by zero
        if count == 0:
            # Return zero when there are no expenses
            return 0.0
        # Reuse total_spent method
        total = self.total_spent()
        # Return average amount
        return total / count

    # Create a readable string report for totals by category
    def category_report_string(self):
        # Get totals per category
        totals = self.total_by_category()
        # List of string lines to join later
        lines = []
        # Iterate category totals
        for cat, val in totals.items():
            # Append formatted line for each category
            lines.append(f"{cat}: ${val:.2f}")
        # Join lines into one string separated by newlines
        return "\n".join(lines)


# ============================================================
# MENU FUNCTIONS - Handle user interactions
# ============================================================

# Display the main menu to the user
def display_menu():
    # Print a decorative header
    print("\n" + "="*60)
    print("💰 PERSONAL EXPENSE TRACKER")
    print("="*60)
    # Print all menu options
    print("1.  ➕ Add New Expense")
    print("2.  📋 View All Expenses")
    print("3.  📊 View Category Totals")
    print("4.  📅 View Monthly Summary")
    print("5.  🏆 View Top 5 Expenses")
    print("6.  🔍 Filter by Category")
    print("7.  📈 View Statistics")
    print("8.  ❌ Delete Expense")
    print("9.  🚪 Exit")
    print("="*60)


# Function to add a new expense (gets user input)
def add_expense_interactive(manager):
    # Print section header
    print("\n" + "="*60)
    print("➕ ADD NEW EXPENSE")
    print("="*60)
    
    # Available categories for the user to choose from
    categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
    
    # Get amount from user with validation
    while True:
        # Ask user to enter amount
        amount_str = input("Enter amount ($): ").strip()
        # Try to convert to float
        try:
            # Convert string to number
            amount = float(amount_str)
            # Check if amount is positive
            if amount <= 0:
                # Show error for negative or zero amount
                print("⚠️  Amount must be greater than 0!")
                continue
            # Break out of loop if valid
            break
        # If user enters non-numeric value
        except ValueError:
            # Show error and ask again
            print("⚠️  Please enter a valid number!")
    
    # Display available categories
    print("\nAvailable categories:")
    # Loop through categories with index numbers
    for i, cat in enumerate(categories, start=1):
        # Print each category with its number
        print(f"  {i}. {cat}")
    
    # Get category choice from user
    while True:
        # Ask user to choose category by number
        choice = input("Enter category number (1-7): ").strip()
        # Try to convert to integer
        try:
            # Convert to int
            choice_num = int(choice)
            # Check if number is in valid range
            if 1 <= choice_num <= 7:
                # Get the category name from list (subtract 1 for 0-based index)
                category = categories[choice_num - 1]
                # Break out of loop
                break
            # If number is out of range
            else:
                # Show error
                print("⚠️  Please enter a number between 1 and 7!")
        # If user enters non-numeric value
        except ValueError:
            # Show error
            print("⚠️  Please enter a valid number!")
    
    # Get date from user
    while True:
        # Ask for date in specific format
        date = input("Enter date (YYYY-MM-DD) or press Enter for 2026-02-03: ").strip()
        # If user presses Enter without typing
        if not date:
            # Use default date
            date = "2026-02-03"
            break
        # Check if date format looks correct (basic validation)
        if len(date) == 10 and date[4] == "-" and date[7] == "-":
            # Accept the date
            break
        # If format is wrong
        else:
            # Show error
            print("⚠️  Please use format YYYY-MM-DD (e.g., 2026-02-03)")
    
    # Get optional note from user
    note = input("Enter note (optional, press Enter to skip): ").strip()
    
    # Create new Expense object with user's input
    expense = Expense(amount, category, date, note)
    # Add expense to manager
    manager.add_expense(expense)
    
    # Show success message
    print(f"\n✅ Successfully added: ${amount:.2f} for {category}")


# Function to view all expenses
def view_all_expenses(manager):
    # Print section header
    print("\n" + "="*60)
    print("📋 ALL EXPENSES")
    print("="*60)
    
    # Get list of all expenses
    expenses = manager.list_expenses()
    
    # Check if there are no expenses
    if not expenses:
        # Show message if empty
        print("No expenses recorded yet! Add some expenses to get started.")
        return
    
    # Loop through each expense with index number
    for i, exp_dict in enumerate(expenses, start=1):
        # Print expense number
        print(f"\n#{i}")
        # Print amount with 2 decimal places
        print(f"  Amount:   ${exp_dict['amount']:.2f}")
        # Print category
        print(f"  Category: {exp_dict['category']}")
        # Print date
        print(f"  Date:     {exp_dict['date']}")
        # Print note
        print(f"  Note:     {exp_dict['note']}")
        # Print separator line
        print("-" * 60)
    
    # Calculate and show total
    total = manager.total_spent()
    print(f"\n💰 TOTAL SPENT: ${total:.2f}")


# Function to show totals by category
def view_category_totals(manager):
    # Print section header
    print("\n" + "="*60)
    print("📊 SPENDING BY CATEGORY")
    print("="*60)
    
    # Get category totals dictionary
    totals = manager.total_by_category()
    
    # Check if there are no expenses
    if not totals:
        # Show message if empty
        print("No expenses to analyze yet!")
        return
    
    # Loop through each category and its total
    for category, amount in totals.items():
        # Print category and amount
        print(f"  {category}: ${amount:.2f}")
    
    # Show overall total
    print(f"\n💰 TOTAL: ${manager.total_spent():.2f}")


# Function to show monthly summary
def view_monthly_summary(manager):
    # Print section header
    print("\n" + "="*60)
    print("📅 MONTHLY SPENDING SUMMARY")
    print("="*60)
    
    # Get monthly summary dictionary
    summary = manager.monthly_summary()
    
    # Check if empty
    if not summary:
        # Show message
        print("No expenses to summarize yet!")
        return
    
    # Create list of month names (index 0 is placeholder)
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Loop through each month and its total (sorted by date)
    for (year, month), amount in sorted(summary.items()):
        # Get month name from list
        month_name = month_names[month]
        # Print month and total
        print(f"  {month_name} {year}: ${amount:.2f}")


# Function to show top 5 expenses
def view_top_expenses(manager):
    # Print section header
    print("\n" + "="*60)
    print("🏆 TOP 5 HIGHEST EXPENSES")
    print("="*60)
    
    # Get top 5 expenses from manager
    top = manager.top_expenses(5)
    
    # Check if empty
    if not top:
        # Show message
        print("No expenses yet!")
        return
    
    # Loop through top expenses with ranking number
    for i, exp in enumerate(top, start=1):
        # Print ranking, amount, category, and date
        print(f"\n#{i}  ${exp.amount:.2f} - {exp.category} ({exp.date})")
        # Print note
        print(f"     Note: {exp.note}")


# Function to filter expenses by category
def filter_by_category_interactive(manager):
    # Print section header
    print("\n" + "="*60)
    print("🔍 FILTER BY CATEGORY")
    print("="*60)
    
    # Show available categories from manager
    if not manager.categories:
        # If no categories exist yet
        print("No expenses recorded yet!")
        return
    
    # Print available categories
    print("\nAvailable categories:")
    # Convert set to sorted list
    cat_list = sorted(list(manager.categories))
    # Loop through categories with numbers
    for i, cat in enumerate(cat_list, start=1):
        # Print each category
        print(f"  {i}. {cat}")
    
    # Get user's choice
    choice = input("\nEnter category number: ").strip()
    
    # Try to convert to integer
    try:
        # Convert to int
        choice_num = int(choice)
        # Check if valid range
        if 1 <= choice_num <= len(cat_list):
            # Get category name
            category = cat_list[choice_num - 1]
        # If out of range
        else:
            # Show error and return
            print("⚠️  Invalid category number!")
            return
    # If not a number
    except ValueError:
        # Show error and return
        print("⚠️  Please enter a valid number!")
        return
    
    # Get filtered expenses
    filtered = manager.filter_by_category(category)
    
    # Check if no expenses found
    if not filtered:
        # Show message
        print(f"No expenses found for category: {category}")
        return
    
    # Print header for filtered results
    print(f"\n📋 EXPENSES IN CATEGORY: {category}")
    print("="*60)
    
    # Loop through filtered expenses
    for i, exp in enumerate(filtered, start=1):
        # Print expense details
        print(f"\n#{i}")
        print(f"  Amount: ${exp.amount:.2f}")
        print(f"  Date:   {exp.date}")
        print(f"  Note:   {exp.note}")
        print("-" * 60)
    
    # Calculate total for this category
    total = sum(exp.amount for exp in filtered)
    print(f"\n💰 Total for {category}: ${total:.2f}")


# Function to show statistics
def view_statistics(manager):
    # Print section header
    print("\n" + "="*60)
    print("📈 EXPENSE STATISTICS")
    print("="*60)
    
    # Check if no expenses
    if len(manager.expenses) == 0:
        # Show message
        print("No expenses to analyze!")
        return
    
    # Calculate statistics
    total = manager.total_spent()
    average = manager.average_expense()
    count = len(manager.expenses)
    categories_count = len(manager.categories)
    
    # Print statistics
    print(f"\n📊 Total Expenses Recorded: {count}")
    print(f"💰 Total Amount Spent:      ${total:.2f}")
    print(f"📉 Average Expense:         ${average:.2f}")
    print(f"🏷️  Number of Categories:    {categories_count}")
    
    # Find highest and lowest expense
    if count > 0:
        # Sort expenses by amount
        sorted_exp = sorted(manager.expenses, key=lambda x: x.amount)
        # Get lowest (first in sorted list)
        lowest = sorted_exp[0]
        # Get highest (last in sorted list)
        highest = sorted_exp[-1]
        
        # Print highest expense
        print(f"\n🔺 Highest Expense: ${highest.amount:.2f} ({highest.category} on {highest.date})")
        # Print lowest expense
        print(f"🔻 Lowest Expense:  ${lowest.amount:.2f} ({lowest.category} on {lowest.date})")


# Function to delete an expense
def delete_expense_interactive(manager):
    # Print section header
    print("\n" + "="*60)
    print("❌ DELETE EXPENSE")
    print("="*60)
    
    # Check if there are any expenses
    if len(manager.expenses) == 0:
        # Show error if no expenses
        print("No expenses to delete!")
        return
    
    # First show all expenses so user can see numbers
    view_all_expenses(manager)
    
    # Ask user for expense number
    choice = input("\nEnter expense number to delete (or 0 to cancel): ").strip()
    
    # Try to convert to integer
    try:
        # Convert to int
        index = int(choice)
        # Check if user wants to cancel
        if index == 0:
            # Cancel operation
            print("Delete cancelled.")
            return
        # Convert to 0-based index
        index = index - 1
        # Try to remove the expense
        removed = manager.remove_expense_by_index(index)
        # Show success message
        print(f"\n✅ Deleted expense: ${removed.amount:.2f} - {removed.category}")
    # If user entered invalid number or index out of range
    except (ValueError, IndexError):
        # Show error message
        print("⚠️  Invalid expense number!")


# ============================================================
# MAIN PROGRAM - Runs the application
# ============================================================
def main():
    # Create an ExpenseManager to store all expenses
    manager = ExpenseManager()
    
    # Print welcome message
    print("\n" + "="*60)
    print("🎉 WELCOME TO PERSONAL EXPENSE TRACKER!")
    print("="*60)
    print("Track your expenses and analyze your spending habits!")
    
    # Create infinite loop for menu
    while True:
        # Display the menu
        display_menu()
        
        # Get user's choice
        choice = input("\nEnter your choice (1-9): ").strip()
        
        # Check which option user selected
        if choice == "1":
            # Add new expense
            add_expense_interactive(manager)
        
        elif choice == "2":
            # View all expenses
            view_all_expenses(manager)
        
        elif choice == "3":
            # View category totals
            view_category_totals(manager)
        
        elif choice == "4":
            # View monthly summary
            view_monthly_summary(manager)
        
        elif choice == "5":
            # View top 5 expenses
            view_top_expenses(manager)
        
        elif choice == "6":
            # Filter by category
            filter_by_category_interactive(manager)
        
        elif choice == "7":
            # View statistics
            view_statistics(manager)
        
        elif choice == "8":
            # Delete expense
            delete_expense_interactive(manager)
        
        elif choice == "9":
            # Exit the program
            print("\n" + "="*60)
            print("👋 Thank you for using Expense Tracker!")
            print("💰 Keep tracking your expenses! Goodbye!")
            print("="*60 + "\n")
            # Break out of the loop to end program
            break
        
        else:
            # If user enters invalid option
            print("\n⚠️  Invalid choice! Please enter a number between 1 and 9.")
        
        # Pause so user can read the output
        input("\nPress Enter to continue...")
        
        


# Entry point - run the main function
if __name__ == "__main__":
    # Call the main function to start the program
    main()