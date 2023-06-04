import pandas as pd
import numpy as np

def create_taxonomy_dataframe(data):
    df = pd.DataFrame(columns=['Elements', 'Level1', 'Level2', 'Root'], dtype=int)
    level2_start_filling = False
    df['Level2'] = np.nan

    for row in data:
        level_before = int(row[0])
        level_after = int(row[1])

        if len(str(level_before)) == 3:
            df.loc[df['Level1'] == level_before, 'Level2'] = level_after
            level2_start_filling = True

        if not level2_start_filling:
            df = df.append({'Elements': level_before, 'Level1': level_after, 'Level2': np.nan, 'Root': 10}, ignore_index=True)

    df['Level2'] = df.apply(lambda row: row['Level1'] if pd.isnull(row['Level2']) else row['Level2'], axis=1)
    df = df.astype(int)
    return df
# def create_taxonomy_dataframe(data):
#     df = pd.DataFrame(columns=['Elements', 'Level1', 'Level2', 'Root'], dtype=int)
#     level2_start_filling = False
#     df['Level2'] = float('nan')
#
#     for row in data:
#         level_before = row[0]
#         level_after = row[1]
#
#         if len(str(int(level_before))) == 3:
#             for index, value in df['Level1'].iteritems():
#                 if value == level_before:
#                     df.at[index, 'Level2'] = level_after
#             level2_start_filling = True
#         if level2_start_filling == False:
#             df = df.append({'Elements': level_before, 'Level1': level_after, 'Level2': float('nan'), 'Root': 10},
#                            ignore_index=True)
#
#     df['Level2'] = df.apply(lambda row: row['Level1'] if pd.isnull(row['Level2']) else row['Level2'], axis=1)
#     return df


df_transactions = pd.read_csv('transactions.csv')
df_taxonomy_basic = np.genfromtxt('taxonomy.csv', delimiter=',', skip_header=1, dtype=int)

df_taxonomy = create_taxonomy_dataframe(df_taxonomy_basic)
df_taxonomy.to_csv('taxonomy_process.csv', index=False)
# print(df_taxonomy)
# print(df_transactions)

df = pd.DataFrame(df_transactions)
transactions = df.apply(lambda row: row.index[row == 1].tolist(), axis=1).tolist()




###########################################################
# BASE TRANSACTION TREE
###########################################################
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


# Budowanie drzewa Trie
trie_root = build_trie(transactions)

# Wypisanie drzewa Trie
print_transaction_trie(trie_root)



###########################################################
# TAXONOMY TREE
###########################################################
from pygtrie import Trie

def build_trie_from_dataframe(df):
    trie = Trie()

    for _, row in df.iterrows():
        product = row[0]
        parent = row[1]
        grandparent = row[2]
        # root = row[3]
        root = tuple(str(row[3]).split('.'))
        trie.setdefault(root, {}).setdefault(grandparent, {}).setdefault(parent, set()).add(product)

    return trie

def print_trie(trie, node=None, prefix=[]):
    if node is None:
        node = trie

    if node:
        if isinstance(node, set):
            for value in node:
                print(prefix + [value])
        else:
            for key, child_node in node.items():
                print_trie(trie, child_node, prefix + [key])


# NIE DZIALA zwracanie pelnej sciezki do elementu
# TODO
def find_path(trie, product):
    path = []
    node = trie

    while True:
        path.append(product)

        if product not in node:  # Przerwij pętlę, jeśli produkt nie jest kluczem w danym węźle
            break

        child_nodes = node[product]

        if len(child_nodes) == 1:  # Istnieje tylko jeden klucz (produkt) w danym węźle
            product = next(iter(child_nodes))
            node = child_nodes[product]
        else:
            break  # Przerwij pętlę, jeśli istnieje więcej niż jeden klucz (niejednoznaczna ścieżka)

    return path

# def find_path(trie, product):
#     path = []
#     node = trie
#
#     while product in node:
#         path.append(product)
#         product = next(iter(node[product]))  # Pobranie jedynego klucza (produktu) w danym węźle
#         node = node[product]
#
#     path.append(product)  # Dodanie korzenia
#
#     return path


# Konwertowanie typów na łańcuchy znaków
df_taxonomy['Elements'] = df_taxonomy['Elements'].astype(str)
df_taxonomy['Level1'] = df_taxonomy['Level1'].astype(str)
df_taxonomy['Level2'] = df_taxonomy['Level2'].astype(str)
df_taxonomy['Root'] = df_taxonomy['Root'].astype(str)

trie = build_trie_from_dataframe(df_taxonomy)

# Wyświetlanie drzewa trie
# print(trie)
print_trie(trie)

product = '1005.0'
path = find_path(trie, product)
print(path)
