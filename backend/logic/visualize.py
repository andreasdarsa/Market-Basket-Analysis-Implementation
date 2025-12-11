import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import networkx as nx
import base64
import io

matplotlib.use('Agg')  # Use a non-interactive backend

# encodes a plot image to base64, so that it can be parsed into HTML later on
def encode_to_base_64(fig: plt.figure = None) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# creates a heatmap showing the most common items inside the transactions
def create_heatmap(transactions: list) -> str:
    items = list(set(item for sublist in transactions for item in sublist)) # deletes any duplicates
    matrix = pd.DataFrame(0, index=items, columns=items)

    for t in transactions:
        for i1 in t:
            for i2 in t:
                if i1 != i2:
                    matrix.loc[i1,i2] += 1

    fig,ax = plt.subplots(figsize=(10,8))
    sns.heatmap(matrix, cmap="YlGnBu", linewidths=0.5, ax=ax)
    plt.title("Heatmap of common appearances")
    plt.tight_layout()
    encoded = encode_to_base_64(fig=fig)
    plt.close(fig)
    return encoded

# creates a bar plot of the most common items (by default it plots the top 10, but the number can change if the user wants otherwise)
def plot_frequent_items(freq_itemsets : pd.DataFrame, n=10) -> str:
    top_items = freq_itemsets.sort_values(by='support', ascending=False).head(n=n)
    top_items['item_str'] = top_items['itemsets'].apply(lambda x: ', '.join(list(x)))

    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(x='support', y='item_str', data=top_items, palette='crest', ax=ax)
    plt.xlabel('Support')
    plt.ylabel('Itemsets')
    plt.title(f"Top {n} most common itemsets")
    plt.tight_layout()
    encoded = encode_to_base_64(fig=fig)
    plt.close(fig)
    return encoded

# creates a graph network showing all the rules created given the itemsets
def draw_rules_network(rules: pd.DataFrame) -> str:
    print(rules.head())
    G = nx.DiGraph() # V1 = antecedents, V2 = consequents, G = V1 union V2

    for _, rule in rules.iterrows():
        G.add_edge(str(rule['antecedents']), str(rule['consequents']), weight=rule['lift'])

    fig,ax = plt.subplots(figsize=(12,8))
    pos = nx.spring_layout(G=G, k=1)
    num_nodes = len(G.nodes())
    node_size = max(1000, 20000 // num_nodes)
    nx.draw(G=G, pos=pos, with_labels=True, node_color='blue', edge_color='black', 
            node_size=node_size, font_size=10, ax=ax)
    labels = nx.get_edge_attributes(G=G, name='weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k, v in labels.items()})
    plt.title("Rules Network")
    plt.tight_layout()
    encoded = encode_to_base_64(fig=fig)
    plt.close(fig)
    return encoded

# creates a scatter plot comparing support and confidence for the same plot
def scatter_lift_support(rules: pd.DataFrame) -> str:
    fig,ax = plt.subplots(figsize=(10,6))
    scatter = ax.scatter(
        x=rules['support'], 
        y=rules['confidence'], 
        s=rules['lift']*10, 
        alpha=0.6, 
        c=rules['lift'], 
        cmap='viridis', 
    )
    ax.set_xlabel("Support")
    ax.set_ylabel("Confidence")
    ax.set_title("Lift vs Support/Confidence")
    plt.colorbar(scatter, label="lift")
    plt.tight_layout()
    encoded = encode_to_base_64(fig=fig)
    plt.close(fig)
    return encoded
