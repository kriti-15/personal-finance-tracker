# ============================================================
# PERSONAL FINANCE TRACKER
# A beginner-friendly tool to track income and expenses
# using Python and SQLite (a simple built-in database)
# ============================================================

import sqlite3          # Built-in Python library for databases
import csv              # Built-in library to read/write CSV files
from datetime import datetime  # To work with dates

# ──────────────────────────────────────────────
# STEP 1: Set up the database
# ──────────────────────────────────────────────

def create_database():
    """
    Creates a local SQLite database file called 'finance.db'
    and sets up a table to store transactions.
    This runs only once when you first start the app.
    """
    conn = sqlite3.connect("finance.db")   # Creates the file if it doesn't exist
    cursor = conn.cursor()                 # A cursor lets us run SQL commands

    # Create the transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date      TEXT NOT NULL,
            type      TEXT NOT NULL,        -- 'income' or 'expense'
            category  TEXT NOT NULL,        -- e.g. 'food', 'salary', 'rent'
            amount    REAL NOT NULL,        -- amount in your currency
            note      TEXT                 -- optional description
        )
    """)

    conn.commit()   # Save changes
    conn.close()    # Always close the connection when done
    print("✅ Database ready.")


# ──────────────────────────────────────────────
# STEP 2: Add a transaction
# ──────────────────────────────────────────────

def add_transaction(type_, category, amount, note=""):
    """
    Adds one income or expense record to the database.

    Parameters:
        type_    : 'income' or 'expense'
        category : e.g. 'salary', 'groceries', 'rent'
        amount   : how much money (e.g. 5000.00)
        note     : optional extra detail
    """
    # Validate inputs
    if type_ not in ("income", "expense"):
        print("❌ Type must be 'income' or 'expense'.")
        return
    if amount <= 0:
        print("❌ Amount must be greater than 0.")
        return

    date_today = datetime.today().strftime("%Y-%m-%d")  # Format: 2025-07-15

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Insert the row into the table
    cursor.execute("""
        INSERT INTO transactions (date, type, category, amount, note)
        VALUES (?, ?, ?, ?, ?)
    """, (date_today, type_, category, amount, note))  # '?' prevents SQL injection

    conn.commit()
    conn.close()
    print(f"✅ Added: {type_.upper()} ₹{amount:.2f} [{category}]")


# ──────────────────────────────────────────────
# STEP 3: View all transactions
# ──────────────────────────────────────────────

def view_all():
    """
    Fetches and prints all transactions from the database.
    """
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()   # Get all results as a list
    conn.close()

    if not rows:
        print("📭 No transactions found.")
        return

    # Print a neat table
    print(f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10} {'Note'}")
    print("─" * 65)
    for row in rows:
        id_, date, type_, category, amount, note = row
        print(f"{id_:<5} {date:<12} {type_:<10} {category:<15} ₹{amount:>9.2f}  {note or ''}")
    print()


# ──────────────────────────────────────────────
# STEP 4: Show monthly summary
# ──────────────────────────────────────────────

def monthly_summary(year, month):
    """
    Shows total income, total expenses, and net savings
    for a given month.

    Example: monthly_summary(2025, 7)  → July 2025
    """
    month_str = f"{year}-{month:02d}"  # e.g. "2025-07"

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Total income for the month
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income' AND date LIKE ?
    """, (f"{month_str}%",))
    total_income = cursor.fetchone()[0]

    # Total expenses for the month
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense' AND date LIKE ?
    """, (f"{month_str}%",))
    total_expense = cursor.fetchone()[0]

    conn.close()

    net_savings = total_income - total_expense

    print(f"\n📅 Summary for {month_str}")
    print("─" * 35)
    print(f"  💰 Total Income  : ₹{total_income:,.2f}")
    print(f"  💸 Total Expenses: ₹{total_expense:,.2f}")
    print(f"  🏦 Net Savings   : ₹{net_savings:,.2f}")
    if net_savings < 0:
        print("  ⚠️  You spent more than you earned this month!")
    else:
        print("  ✅ Great job staying in the green!")
    print()


# ──────────────────────────────────────────────
# STEP 5: Export to CSV
# ──────────────────────────────────────────────

def export_to_csv(filename="transactions_export.csv"):
    """
    Exports all transactions to a CSV file.
    Useful for opening in Excel or analyzing further.
    """
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    conn.close()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Note"])  # Header
        writer.writerows(rows)

    print(f"✅ Exported {len(rows)} records to '{filename}'")


# ──────────────────────────────────────────────
# STEP 6: Simple text menu (run the app)
# ──────────────────────────────────────────────

def main():
    create_database()

    while True:
        print("\n╔══════════════════════════════╗")
        print("║   💰 Personal Finance Tracker ║")
        print("╚══════════════════════════════╝")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Monthly Summary")
        print("5. Export to CSV")
        print("6. Quit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            category = input("Category (e.g. salary, freelance): ").strip()
            amount   = float(input("Amount (₹): ").strip())
            note     = input("Note (optional): ").strip()
            add_transaction("income", category, amount, note)

        elif choice == "2":
            category = input("Category (e.g. food, rent, transport): ").strip()
            amount   = float(input("Amount (₹): ").strip())
            note     = input("Note (optional): ").strip()
            add_transaction("expense", category, amount, note)

        elif choice == "3":
            view_all()

        elif choice == "4":
            year  = int(input("Year  (e.g. 2025): ").strip())
            month = int(input("Month (1-12)     : ").strip())
            monthly_summary(year, month)

        elif choice == "5":
            export_to_csv()

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1–6.")


# This block runs only when you execute this file directly
if __name__ == "__main__":
    main()
