import csv


def export_expenses_to_csv(expenses, filename="expenses_report.csv"):
    """Write all expenses to a CSV file and return the output filename."""
    fieldnames = ["id", "date", "category", "description", "amount"]
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in expenses:
            writer.writerow({
                "id": item["id"],
                "date": item["date"],
                "category": item["category"],
                "description": item["description"],
                "amount": f"{item['amount']:.2f}",
            })
    return filename 