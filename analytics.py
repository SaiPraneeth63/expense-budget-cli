def calculate_category_totals(expenses):
    """Return a dict mapping each category to total spent amount."""
    totals = {}
    for item in expenses:
        category = item["category"]
        amount = item["amount"]
        if category in totals:
            totals[category] += amount
        else:
            totals[category] = amount
    return totals


def build_progress_bar(spent, limit, width=20):
    """Create a simple ASCII progress bar comparing spent against limit."""
    if limit <= 0:
        return "[" + ("-" * width) + "] No limit"
    ratio = spent / limit
    filled = int(round(ratio * width))
    if filled > width:
        filled = width
    if filled < 0:
        filled = 0
    bar = ("#" * filled) + ("-" * (width - filled))
    percent = round(ratio * 100, 1)
    return f"[{bar}] {percent}%"


def evaluate_budgets(expenses, budgets):
    """Compare category spending against set budgets and flag over-budget items."""
    totals = calculate_category_totals(expenses)
    report = []

    all_categories = set(totals.keys()) | set(budgets.keys())
    for category in sorted(all_categories):
        spent = round(totals.get(category, 0.0), 2)
        limit = budgets.get(category)
        if limit is None:
            status = "UNBUDGETED"
            remaining = None
            bar = "No budget set"
        else:
            remaining = round(limit - spent, 2)
            status = "OVER BUDGET" if spent > limit else "WITHIN BUDGET"
            bar = build_progress_bar(spent, limit)

        report.append({
            "category": category,
            "spent": spent,
            "limit": limit,
            "remaining": remaining,
            "status": status,
            "bar": bar,
        })

    return report


def calculate_overall_summary(expenses):
    """Return total spent, transaction count, and average transaction size."""
    count = len(expenses)
    total = 0.0
    for item in expenses:
        total += item["amount"]
    average = (total / count) if count > 0 else 0.0
    return {
        "count": count,
        "total": round(total, 2),
        "average": round(average, 2),
    }