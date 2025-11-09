import pandas as pd
import random
from collections import Counter

GROCERIES_PATH = "backend/data/Groceries_dataset.csv"
GENERATED_PATH = "backend/data/generated_transactions.csv"


# This function returns a list of basket items from each transaction
def get_items():
    df = pd.read_csv(GROCERIES_PATH)
    items_list = df["itemDescription"].apply(lambda x : x.split('/'))
    return items_list

# This function creates a generic dataset of basket items
def create_random_dataset():
    # what items are going to be included
    items = [
        'bread', 'milk', 'cheese', 'butter', 'eggs', 'apples', 'bananas', 'oranges',
        'potatoes', 'onions', 'tomatoes', 'pasta', 'rice', 'olive oil',
        'sugar', 'salt', 'coffee', 'tea', 'chocolate', 'orange juice',
        'chicken', 'beef', 'fish', 'salad', 'carrots', 'filter coffee',
        'cereal', 'yoghurt', 'beer', 'wine', 'soda', 'chewing gum']

    # represents how often these items are purchased
    weights = [
        8, 10, 6, 5, 9, 7, 7, 7,
        6, 6, 7, 8, 6, 5,
        5, 5, 7, 4, 3, 6,
        5, 3, 2, 4, 3, 4,
        7, 6, 3, 3, 4, 2
    ]

    # our final dataset
    transactions = []
    num_of_transactions = 5000

    for _ in range(num_of_transactions):
        items_in_basket = random.randint(2,7) # each basket contains 2 to 7 items
        basket = random.choices(items, weights=weights, k=items_in_basket)
        basket = list(set(basket)) # if there are duplicates, delete them
        transactions.append(basket)

    print(f"✅ A list of {num_of_transactions} transactions has been successfully generated.")

    with open(GENERATED_PATH, "w") as f:
        f.write("Transaction" + "\n")
        for basket in transactions:
            f.write(",".join(basket) + "\n")

    print("✅ Baskets written to csv file.")

    return transactions

def clean_csv(path, min_support=0.005, min_items_per_transaction=2):
    df = pd.read_csv(path)

    # Check if the CSV file has the correct columns
    if list(df.columns) != ["TransactionID", "Items"]:
        raise ValueError("CSV file must only have two columns named 'TransactionID' and 'Items'.")
    
    # Replace '/' with ',' in the 'Items' column in order to split items correctly
    df['Items'] = df['Items'].str.replace('/', ',', regex=False)

    # Split the 'Items' column in list of items
    df['Items'] = df['Items'].apply(lambda x: x.split(','))

    # Remove transactions with less than minimum items
    df = df[df['Items']].apply(lambda x: len(x) >= min_items_per_transaction)

    # Calculate support
    all_items = [item for sublist in df['Items'] for item in sublist]
    item_counts = Counter(all_items)
    total_transactions = len(df)
    support = {item: count / total_transactions for item, count in item_counts.items() if count / total_transactions >= min_support}

    # Remove items that do not meet the minimum support
    df['Items'] = df['Items'].apply(lambda items: [item for item in items if item in support])

    # Remove empty/small transactions
    df = df[df['Items'].apply(lambda x: len(x) >= min_items_per_transaction)]

    # Calculate cleaning statistics
    stats = {
        "total_transactions": total_transactions,
        "removed_transactions": total_transactions - len(df),
        "total_items": len(all_items),
        "removed_items": sum(item_counts[item] for item in item_counts if item_counts[item] / total_transactions < min_support),
        "support": support,
        "frequent_items": len(support),
        "avg_items_per_transaction": df['Items'].apply(len).mean()
    }

    return df, stats
