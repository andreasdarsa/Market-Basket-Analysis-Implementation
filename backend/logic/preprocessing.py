import pandas as pd
import random

GROCERIES_PATH = "backend/data/Groceries_dataset.csv"
GENERATED_PATH = "backend/data/generated_transactions.csv"


# This function returns a list of basket items from each transaction
def get_items():
    df = pd.read_csv(GROCERIES_PATH)
    items_list = df["itemDescription"].apply(lambda x : x.split('/'))
    return items_list

# This function creates a generic dataset of basket items
def create_dataset():
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
