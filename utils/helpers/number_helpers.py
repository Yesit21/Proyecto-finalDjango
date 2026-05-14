def format_currency(amount):
    return f"${amount:,.2f}"

def calculate_percentage(part, total):
    if total == 0:
        return 0
    return (part / total) * 100
