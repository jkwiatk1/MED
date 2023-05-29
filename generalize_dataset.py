import pandas as pd
import numpy as np


def create_taxonomy_dataframe(data):
    df = pd.DataFrame(columns=['Elements', 'Level1', 'Level2', 'Root'])
    level2_start_filling = False
    df['Level2'] = float('nan')

    for row in data:
        level_before = row[0]
        level_after = row[1]

        if len(str(int(level_before))) == 3:
            for index, value in df['Level1'].iteritems():
                if value == level_before:
                    df.at[index, 'Level2'] = level_after
            level2_start_filling = True
        if level2_start_filling == False:
            df = df.append({'Elements': level_before, 'Level1': level_after, 'Level2': float('nan'), 'Root': 10},
                           ignore_index=True)


    df['Level2'] = df.apply(lambda row: row['Level1'] if pd.isnull(row['Level2']) else row['Level2'], axis=1)
    return df

df_transactions = pd.read_csv('transactions.csv')
df_taxonomy_basic = np.genfromtxt('taxonomy.csv', delimiter=',', skip_header=1)

df_taxonomy = create_taxonomy_dataframe(df_taxonomy_basic)
print(df_taxonomy)
print(df_transactions)




from anytree import Node, RenderTree

# node_dict = {}
# for index, row in df_taxonomy_basic.iterrows():
#     node_id = row['0']
#     parent_id = row['1']
#     if node_id not in node_dict:
#         node_dict[node_id] = Node(node_id)
#     if parent_id not in node_dict:
#         node_dict[parent_id] = Node(parent_id)
#     node_dict[node_id].parent = node_dict[parent_id]
#
# # Znajdowanie korzenia drzewa
# root = None
# for node in node_dict.values():
#     if node.is_root:
#         root = node
#         break

# # Wypisanie drzewa
# for pre, fill, node in RenderTree(root):
#     print(f"{pre}{node.name}")