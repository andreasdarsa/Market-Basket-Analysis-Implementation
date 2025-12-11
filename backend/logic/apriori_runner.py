import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os

def get_items_list(fpath) -> list:
    try:
        df = pd.read_csv(fpath)
        items_list = df['Items'].str.split(",").tolist()
    except FileNotFoundError:
        items_list = []

    return items_list


def get_frequent_itemsets(path, min_sup=0.005) -> pd.DataFrame:
    items_list = get_items_list(fpath=path)
    if not items_list:
        return pd.DataFrame(columns=['support', 'itemsets'])
    te = TransactionEncoder()
    te_ary = te.fit(items_list).transform(items_list)
    enc_df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(enc_df, min_support=min_sup, use_colnames=True)
    frequent_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) > 0)] # Only return itemsets with more than 1 item
    return frequent_itemsets


def get_rules(path, min_support=0.005, min_confidence=0.2, min_lift=1.1) -> pd.DataFrame:
    frequent_itemsets = get_frequent_itemsets(path, min_support)
    if frequent_itemsets.empty:
        return pd.DataFrame(columns=['antecedents', 'consequents', 'support', 'confidence', 'lift'])

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules[(rules['support'] > min_support) & (rules['lift'] > min_lift) & (rules['confidence'] > min_confidence)]

    return rules
