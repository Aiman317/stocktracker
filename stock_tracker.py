
import csv
from datetime import datetime

STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "AMZN": 145,
    "MSFT": 410,
}


def get_user_portfolio():
    """
    Ask the user for stock names and quantities.
    Returns a dictionary like {"AAPL": 10, "TSLA": 5}.
    """
    portfolio = {}
    print("Available stocks:", ", ".join(STOCK_PRICES.keys()))
    print("Enter stock symbol and quantity. Type 'done' when finished.\n")

    while True:
        symbol = input("Stock symbol (or 'done'): ").strip().upper()
        if symbol == "DONE":
            break

        if symbol not in STOCK_PRICES:
            print(f"  '{symbol}' not found in price list. Try again.\n")
            continue

        qty_input = input(f"Quantity of {symbol}: ").strip()
        try:
            quantity = int(qty_input)
            if quantity <= 0:
                print("  Quantity must be a positive whole number.\n")
                continue
        except ValueError:
            print("  Please enter a valid whole number.\n")
            continue

        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"  Added {quantity} share(s) of {symbol}.\n")

    return portfolio


def calculate_investment(portfolio):
    """
    Given a portfolio dict {"AAPL": 10, ...}, return:
    - a list of rows: [(symbol, quantity, price, value), ...]
    - total investment value
    """
    rows = []
    total = 0
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * quantity
        rows.append((symbol, quantity, price, value))
        total += value
    return rows, total


def display_summary(rows, total):
    """Print a formatted summary table to the console."""
    print("\n" + "=" * 45)
    print(f"{'Symbol':<8}{'Qty':<8}{'Price':<10}{'Value':<10}")
    print("-" * 45)
    for symbol, quantity, price, value in rows:
        print(f"{symbol:<8}{quantity:<8}${price:<9}${value:<9}")
    print("-" * 45)
    print(f"{'TOTAL INVESTMENT:':<26}${total:,.2f}")
    print("=" * 45 + "\n")


def save_to_file(rows, total):
    """Ask the user whether to save results, and in which format."""
    choice = input("Save results to a file? (y/n): ").strip().lower()
    if choice != "y":
        print("Skipping file save.")
        return

    fmt = input("Choose format - txt or csv: ").strip().lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if fmt == "csv":
        filename = f"portfolio_{timestamp}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Quantity", "Price", "Value"])
            for row in rows:
                writer.writerow(row)
            writer.writerow([])
            writer.writerow(["Total Investment", "", "", f"{total:.2f}"])
        print(f"Saved to {filename}")

    elif fmt == "txt":
        filename = f"portfolio_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write("Stock Portfolio Summary\n")
            f.write("=" * 45 + "\n")
            f.write(f"{'Symbol':<8}{'Qty':<8}{'Price':<10}{'Value':<10}\n")
            f.write("-" * 45 + "\n")
            for symbol, quantity, price, value in rows:
                f.write(f"{symbol:<8}{quantity:<8}${price:<9}${value:<9}\n")
            f.write("-" * 45 + "\n")
            f.write(f"TOTAL INVESTMENT: ${total:,.2f}\n")
        print(f"Saved to {filename}")

    else:
        print("Unrecognized format. File not saved.")


def main():
    print("=== Stock Portfolio Tracker ===\n")
    portfolio = get_user_portfolio()

    if not portfolio:
        print("No stocks entered. Exiting.")
        return

    rows, total = calculate_investment(portfolio)
    display_summary(rows, total)
    save_to_file(rows, total)


if __name__ == "__main__":
    main()
