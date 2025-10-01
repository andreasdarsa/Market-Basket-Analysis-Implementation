import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from preprocessing import get_items, create_random_dataset
import os

FILE_PATH = "backend/data/generated_transactions.csv"


def get_items_list(fpath=FILE_PATH) -> list:
    if os.path.exists(path=fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            items_list = [line.strip().split(",") for line in f]
    else:
        items_list = create_random_dataset()

    return items_list


def get_frequent_itemsets(path, min_sup=0.005) -> pd.DataFrame:
    items_list = get_items_list(fpath=path)
    te = TransactionEncoder()
    te_ary = te.fit(items_list).transform(items_list)
    enc_df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(enc_df, min_support=min_sup, use_colnames=True)
    return frequent_itemsets


def get_rules(path, min_support=0.005, min_confidence=0.2, min_lift=1.1) -> pd.DataFrame:
    frequent_itemsets = get_frequent_itemsets(path, min_support)

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules[(rules['support'] > min_support) & (rules['lift'] > min_lift) & (rules['confidence'] > min_confidence)]

    return rules
