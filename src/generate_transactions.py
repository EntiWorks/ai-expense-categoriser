import os
import csv
import random

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

OUTPUT_PATH = "data/transactions.csv"

CATEGORIES = {
    "Groceries": [
        "Tesco", "Sainsbury's", "Asda", "Lidl", "Aldi", "Waitrose"
    ],
    "Transport": [
        "Shell Petrol Station", "BP Fuel", "Trainline", "Uber", "Stagecoach Bus"
    ],
    "Entertainment": [
        "Netflix", "Spotify", "Cineworld", "Odeon", "Steam Purchase"
    ],
    "Shopping": [
        "Amazon", "eBay", "Argos", "Currys", "IKEA"
    ],
    "Bills": [
        "BT Broadband", "O2 Mobile", "EE Mobile", "Thames Water", "British Gas"
    ],
    "Eating Out": [
        "McDonald's", "KFC", "Nando's", "Starbucks", "Local Restaurant"
    ]
}

def generate_transaction():
    category = random.choice(list(CATEGORIES.keys()))
    merchant = random.choice(CATEGORIES[category])

    amount = round(random.uniform(3, 120), 2)

    description = f"{merchant} £{amount}"
    return {
        "description": description,
        "amount": amount,
        "category": category
    }

def main(n_rows: int = 300):
    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["description", "amount", "category"])
        writer.writeheader()

        for _ in range(n_rows):
            writer.writerow(generate_transaction())

    print(f"Generated {n_rows} rows at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
