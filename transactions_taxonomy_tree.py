import pandas as pd
df_transactions = pd.read_csv('transactions.csv')
df_transactions_with_parents = pd.read_csv("transactions_with_parents.csv")

# ###########################################################
# TRANSACTION TREE
# ###########################################################
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0

def build_trie(transactions):
    root = TrieNode()
    for transaction in transactions:
        current = root
        for product in transaction:
            if product not in current.children:
                current.children[product] = TrieNode()
            current = current.children[product]
            current.count += 1
    return root

def print_transaction_trie(node, prefix=[]):
    if node.count > 0:
        print(prefix, "Count:", node.count)
    for product, child in node.children.items():
        print_transaction_trie(child, prefix + [product])
df = pd.DataFrame(df_transactions)
transactions = df.apply(lambda row: row.index[row == 1].tolist(), axis=1).tolist()
print(transactions)

# Budowanie drzewa Trie
trie_root = build_trie(transactions)

# Wypisanie drzewa Trie
print_transaction_trie(trie_root)



# ###########################################################
# TAXONOMY TREE
# ###########################################################
import csv

filename = 'taxonomy_dictionary.csv'

import pygraphviz as pgv
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
trees = defaultdict(list)

with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        elements = row['Elements'].split(',')
        ancestors = row['Ancestors'].split(',')

        for i in range(len(ancestors)):
            root = ancestors[-1]
            if i < len(ancestors) - 1:
                descendant = ancestors[len(ancestors) - 2 - i]
                trees[root].append(descendant)
            else:
                trees[root].append(elements)

# Print the trees
for root, descendants in trees.items():
    print('Root:', root)
    for descendant in descendants:
        print('Descendant:', descendant)
    print('----------------------')

for root, descendants in trees.items():
    G = nx.DiGraph()

    G.add_node(root)
    for descendant in descendants:
        if isinstance(descendant, list):
            for leaf in descendant:
                G.add_node(leaf)
                G.add_edge(root, leaf)
        else:
            G.add_edge(root, descendant)

    plt.figure(figsize=(10, 8))
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw_networkx(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10)
    plt.title(f"Tree with root {root}")
    plt.axis('off')
    plt.show()





# ###########################################################
# SHOW TAXONOMY ON CMD
# ###########################################################
# from collections import defaultdict
# trees = defaultdict(list)
#
# # Read the CSV file and populate the trees dictionary
# with open(filename, 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         elements = row['Elements'].split(',')
#         ancestors = row['Ancestors'].split(',')
#
#         for i in range(len(ancestors)):
#             root = ancestors[-1]
#             if i < len(ancestors) - 1:
#                 descendant = ancestors[len(ancestors) - 2 - i]
#                 trees[root].append(descendant)
#             else:
#                 trees[root].append(elements)
#
# # Print the trees
# for root, descendants in trees.items():
#     print('Root:', root)
#     for descendant in descendants:
#         print('Descendant:', descendant)
#     print('----------------------')