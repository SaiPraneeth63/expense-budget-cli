import json
import os

EXPENSES_FILE = "expenses.json"
BUDGET_FILE = "budget.json"


def load_json(filepath, default_value):
    """Load JSON data from a file, returning default_value if missing or invalid."""
    if not os.path.exists(filepath):
        return default_value
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default_value


def save_json(filepath, data):
    """Write data to a JSON file with readable formatting."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_expenses():
    """Return list of expense dictionaries."""
    return load_json(EXPENSES_FILE, [])


def save_expenses(expenses):
    """Save list of expense dictionaries."""
    save_json(EXPENSES_FILE, expenses)


def load_budgets():
    """Return dictionary mapping category names to monthly budget limits."""
    return load_json(BUDGET_FILE, {})


def save_budgets(budgets):
    """Save category budget limits dictionary."""
    save_json(BUDGET_FILE, budgets)