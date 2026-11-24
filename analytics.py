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