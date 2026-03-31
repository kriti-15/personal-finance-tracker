# ============================================================
# MONTHLY BUDGET AUTOMATION TOOL
# Reads your expenses from a CSV file and automatically:
#   - Categorizes spending
#   - Compares against your budget limits
#   - Generates a summary report + pie chart
#   - Sends alerts for overspending categories
# ============================================================

import csv
import os
from collections import defaultdict   # A dictionary that auto-creates keys
from datetime import datetime
import matplotlib.pyplot as plt


# ──────────────────────────────────────────────
# STEP 1: Define your monthly budget limits
# ──────────────────────────────────────────────

# Edit these values to match your real budget (in ₹ or your currency)
MONTHLY_BUDGET = {
    "food"        : 8000,
    "transport"   : 2000,
    "rent"        : 12000,
    "utilities"   : 1500,
    "entertainment": 3000,
    "health"      : 2000,
    "shopping"    : 4000,
    "education"   : 2000,
    "other"       : 2000,
}


# ──────────────────────────────────────────────
# STEP 2: Create a sample CSV if none exists
# ──────────────────────────────────────────────

def create_sample_csv(filename="expenses.csv"):
    """
    Creates a sample expenses CSV file so you can test the tool.
    In real use, you'd fill this file with your actual expenses.
    """
    if os.path.exists(filename):
        return  # Don't overwrite if file already exists

    sample_data = [
        ["date",       "category",    "amount", "note"],
        ["2025-07-01", "rent",        12000,    "Monthly rent"],
        ["2025-07-02", "food",        450,      "Groceries"],
        ["2025-07-03", "transport",   80,       "Metro card top-up"],
        ["2025-07-04", "food",        320,      "Lunch"],
        ["2025-07-05", "utilities",   800,      "Electricity bill"],
        ["2025-07-06", "entertainment", 599,    "Netflix subscription"],
        ["2025-07-08", "food",        1200,     "Restaurant dinner"],
        ["2025-07-10", "shopping",    2500,     "Clothes"],
        ["2025-07-11", "health",      600,      "Medicines"],
        ["2025-07-12", "food",        380,      "Groceries"],
        ["2025-07-14", "transport",   500,      "Cab rides"],
        ["2025-07-15", "education",   1999,     "Udemy course"],
        ["2025-07-17", "food",        850,      "Groceries"],
        ["2025-07-19", "entertainment", 1200,   "Movie + popcorn"],
        ["2025-07-20", "shopping",    1800,     "Books"],
        ["2025-07-22", "food",        290,      "Coffee & snacks"],
        ["2025-07-24", "utilities",   400,      "Internet bill"],
        ["2025-07-25", "health",      1500,     "Doctor visit"],
        ["2025-07-26", "food",        750,      "Groceries"],
        ["2025-07-28", "transport",   300,      "Auto rides"],
        ["2025-07-29", "entertainment", 900,    "Concert ticket"],
        ["2025-07-30", "food",        620,      "Restaurant"],
        ["2025-07-31", "other",       350,      "Miscellaneous"],
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

    print(f"📄 Created sample file: '{filename}' (edit this with your real expenses!)")


# ──────────────────────────────────────────────
# STEP 3: Read and process the CSV
# ──────────────────────────────────────────────

def read_expenses(filename="expenses.csv"):
    """
    Reads the CSV and returns:
    - A dict of {category: total_amount_spent}
    - Total number of transactions
    """
    spending = defaultdict(float)  # Auto-initializes missing keys to 0.0
    count = 0

    with open(filename, "r") as f:
        reader = csv.DictReader(f)  # Reads rows as dictionaries using header row

        for row in reader:
            category = row["category"].strip().lower()
            amount   = float(row["amount"])
            spending[category] += amount
            count += 1

    print(f"✅ Read {count} transactions from '{filename}'")
    return dict(spending), count


# ──────────────────────────────────────────────
# STEP 4: Compare spending vs budget
# ──────────────────────────────────────────────

def compare_with_budget(spending):
    """
    Compares actual spending against budget limits.
    Returns a list of categories where you overspent.
    """
    overspent = []

    print("\n📊 Budget vs Actual Spending")
    print("─" * 65)
    print(f"  {'Category':<16} {'Budget':>10} {'Spent':>10} {'Remaining':>12} {'Status'}")
    print("─" * 65)

    for category, budget in MONTHLY_BUDGET.items():
        spent     = spending.get(category, 0.0)
        remaining = budget - spent
        pct       = (spent / budget) * 100

        if remaining < 0:
            status = "🔴 OVER"
            overspent.append((category, abs(remaining)))
        elif pct >= 80:
            status = "🟡 WARN"
        else:
            status = "🟢 OK"

        print(f"  {category:<16} ₹{budget:>8,.0f}  ₹{spent:>8,.2f}  ₹{remaining:>10,.2f}  {status}")

    print("─" * 65)

    # Show categories NOT in the predefined budget
    for cat, amt in spending.items():
        if cat not in MONTHLY_BUDGET:
            print(f"  {cat:<16} {'N/A':>10}  ₹{amt:>8,.2f}  {'N/A':>10}  ⚪ NO BUDGET SET")

    return overspent


# ──────────────────────────────────────────────
# STEP 5: Print alert messages
# ──────────────────────────────────────────────

def print_alerts(overspent):
    """Prints warning messages for overspent categories."""
    if not overspent:
        print("\n🎉 Congratulations! You stayed within budget in all categories!")
        return

    print("\n⚠️  OVERSPENDING ALERTS")
    print("─" * 40)
    for category, excess in overspent:
        print(f"  🔴 {category.upper()}: Overspent by ₹{excess:,.2f}")
    print("\n💡 Tip: Review these categories next month to cut back.")


# ──────────────────────────────────────────────
# STEP 6: Generate a pie chart
# ──────────────────────────────────────────────

def generate_pie_chart(spending, month="July 2025"):
    """
    Creates a pie chart showing how spending is distributed
    across categories. Saves it as a PNG file.
    """
    labels = list(spending.keys())
    values = list(spending.values())

    # Color palette for the pie slices
    colors = [
        "#2196F3", "#F44336", "#4CAF50", "#FF9800",
        "#9C27B0", "#00BCD4", "#FF5722", "#607D8B", "#E91E63"
    ]

    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",     # Show percentage on each slice
        colors=colors[:len(labels)],
        startangle=140,
        pctdistance=0.82
    )

    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight("bold")

    ax.set_title(f"Spending Breakdown — {month}", fontsize=14, fontweight="bold", pad=20)

    total = sum(values)
    ax.text(0, -1.3, f"Total Spent: ₹{total:,.2f}", ha="center", fontsize=11, color="gray")

    plt.tight_layout()
    filename = "spending_breakdown.png"
    plt.savefig(filename, dpi=150)
    print(f"\n✅ Pie chart saved as '{filename}'")
    plt.show()


# ──────────────────────────────────────────────
# STEP 7: Save a text report
# ──────────────────────────────────────────────

def save_report(spending, overspent, filename="budget_report.txt"):
    """
    Saves a simple text report of this month's budget analysis.
    Useful to keep records over time.
    """
    today = datetime.today().strftime("%Y-%m-%d %H:%M")
    total_spent  = sum(spending.values())
    total_budget = sum(MONTHLY_BUDGET.values())

    with open(filename, "w") as f:
        f.write(f"BUDGET REPORT — Generated on {today}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Budget : ₹{total_budget:,.2f}\n")
        f.write(f"Total Spent  : ₹{total_spent:,.2f}\n")
        f.write(f"Net Remaining: ₹{total_budget - total_spent:,.2f}\n\n")

        f.write("CATEGORY BREAKDOWN\n")
        f.write("-" * 40 + "\n")
        for cat, amt in sorted(spending.items(), key=lambda x: -x[1]):
            f.write(f"  {cat:<16}: ₹{amt:,.2f}\n")

        if overspent:
            f.write("\nOVERSPENT CATEGORIES\n")
            f.write("-" * 40 + "\n")
            for cat, excess in overspent:
                f.write(f"  {cat}: Over by ₹{excess:,.2f}\n")

    print(f"✅ Report saved as '{filename}'")


# ──────────────────────────────────────────────
# MAIN RUNNER
# ──────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════╗")
    print("║  🤖 Monthly Budget Automation Tool ║")
    print("╚══════════════════════════════════╝\n")

    csv_file = "expenses.csv"

    # Create sample data if no file exists
    create_sample_csv(csv_file)

    # Read and process the file
    spending, _ = read_expenses(csv_file)

    # Compare vs budget and get alerts
    overspent = compare_with_budget(spending)
    print_alerts(overspent)

    # Generate visual chart
    generate_pie_chart(spending)

    # Save text report
    save_report(spending, overspent)

    print("\n✅ Budget analysis complete!")


if __name__ == "__main__":
    main()
