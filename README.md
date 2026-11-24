# Expense & Budget Analytics CLI

A modular Python command-line application for tracking daily expenses, setting category budgets, viewing visual progress bars, and exporting reports to CSV using only the Python standard library.

## Key Features
- **Expense Tracking:** Log transactions with date, category, description, and amount.
- **Category Budgets & Alerts:** Define spending caps per category and get immediate alerts when limits are exceeded.
- **Visual Progress Bars:** Inspect category utilization percentages and remaining budget balances in the terminal.
- **Category Filtering & Deletion:** Filter logs by category or remove entries by ID.
- **CSV Export:** Generate clean CSV reports compatible with spreadsheets and data tools.

## Architecture
- `main.py` — CLI menu loop, input validation, and command orchestration.
- `storage.py` — Safe JSON load/save helpers for expenses and budgets.
- `analytics.py` — Aggregation logic, summary metrics, and progress bar formatting.
- `exporter.py` — CSV report generation.

## Usage
```bash
git clone [https://github.com/YOUR_USERNAME/expense-budget-cli.git](https://github.com/YOUR_USERNAME/expense-budget-cli.git)
cd expense-budget-cli
python main.py