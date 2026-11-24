from datetime import date
from storage import (
    load_expenses,
    save_expenses,
    load_budgets,
    save_budgets,
)
from analytics import (
    evaluate_budgets,
    calculate_overall_summary,
)
from exporter import export_expenses_to_csv


def get_next_id(expenses):
    """Return the next available integer ID."""
    if not expenses:
        return 1
    highest = 0
    for item in expenses:
        if item["id"] > highest:
            highest = item["id"]
    return highest + 1


def parse_positive_float(prompt_text):
    """Prompt until a valid positive number is entered."""
    while True:
        raw = input(prompt_text).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return round(value, 2)
        except ValueError:
            print("Invalid number. Try again (e.g., 120 or 49.50).")


def add_expense(expenses, budgets):
    """Add an expense record and warn if it exceeds the category budget."""
    category = input("Category (e.g., Food, Travel, Books): ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    if not description:
        description = "General expense"

    amount = parse_positive_float("Amount: ")
    expense_date = input(f"Date [YYYY-MM-DD, default {date.today()}]: ").strip()
    if not expense_date:
        expense_date = str(date.today())

    record = {
        "id": get_next_id(expenses),
        "date": expense_date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(record)
    save_expenses(expenses)
    print(f"Saved expense #{record['id']}: {category} - {amount:.2f}")

    if category in budgets:
        report = evaluate_budgets(expenses, budgets)
        for row in report:
            if row["category"] == category and row["status"] == "OVER BUDGET":
                diff = round(row["spent"] - row["limit"], 2)
                print(f"Alert: '{category}' is over budget by {diff:.2f}!")


def set_category_budget(budgets):
    """Set or update a monthly spending limit for a category."""
    category = input("Category to budget: ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return

    limit = parse_positive_float(f"Monthly limit for {category}: ")
    budgets[category] = limit
    save_budgets(budgets)
    print(f"Budget set: {category} -> {limit:.2f}")


def view_expenses(expenses, filter_category=None):
    """Display expenses, optionally filtered by category."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Expense Log ---")
    shown = 0
    for item in expenses:
        if filter_category and item["category"].lower() != filter_category.lower():
            continue
        print(
            f"#{item['id']} | {item['date']} | {item['category']} | "
            f"{item['description']} | {item['amount']:.2f}"
        )
        shown += 1

    if shown == 0:
        print(f"No expenses found for category '{filter_category}'.")


def view_analytics(expenses, budgets):
    """Print overall summary and category budget progress bars."""
    summary = calculate_overall_summary(expenses)
    print("\n--- Spending Summary ---")
    print(f"Transactions: {summary['count']}")
    print(f"Total Spent:  {summary['total']:.2f}")
    print(f"Avg / Entry:  {summary['average']:.2f}")

    print("\n--- Category Budget Status ---")
    rows = evaluate_budgets(expenses, budgets)
    if not rows:
        print("No categories or budgets configured yet.")
        return

    for row in rows:
        limit_str = f"{row['limit']:.2f}" if row["limit"] is not None else "N/A"
        rem_str = f"{row['remaining']:.2f}" if row["remaining"] is not None else "N/A"
        print(
            f"{row['category']}: Spent {row['spent']:.2f} / Limit {limit_str} "
            f"(Remaining: {rem_str}) [{row['status']}]"
        )
        print(f"  {row['bar']}")


def delete_expense(expenses):
    """Delete an expense entry by ID."""
    view_expenses(expenses)
    if not expenses:
        return

    raw_id = input("\nEnter expense ID to delete: ").strip()
    try:
        target_id = int(raw_id)
    except ValueError:
        print("Invalid ID.")
        return

    for idx in range(len(expenses)):
        if expenses[idx]["id"] == target_id:
            removed = expenses.pop(idx)
            save_expenses(expenses)
            print(f"Deleted #{target_id} ({removed['description']}).")
            return

    print(f"No expense found with ID #{target_id}.")


def handle_export(expenses):
    """Export current expenses to a CSV file."""
    if not expenses:
        print("No expenses to export.")
        return
    filename = input("Output CSV filename [expenses_report.csv]: ").strip()
    if not filename:
        filename = "expenses_report.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"
    saved_path = export_expenses_to_csv(expenses, filename)
    print(f"Exported {len(expenses)} expenses to {saved_path}")


def main():
    expenses = load_expenses()
    budgets = load_budgets()

    while True:
        print("\n=== Expense & Budget Analytics CLI ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses by category")
        print("4. Set category budget")
        print("5. View analytics & budget bars")
        print("6. Delete expense")
        print("7. Export expenses to CSV")
        print("8. Exit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            add_expense(expenses, budgets)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            cat = input("Enter category name: ").strip()
            view_expenses(expenses, filter_category=cat)
        elif choice == "4":
            set_category_budget(budgets)
        elif choice == "5":
            view_analytics(expenses, budgets)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            handle_export(expenses)
        elif choice == "8":
            print("Exiting. Keep tracking!")
            break
        else:
            print("Choose a valid option from 1 to 8.")


if __name__ == "__main__":
    main()