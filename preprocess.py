#https://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php

import requests
import numpy as np
import pandas as pd
import io

url_transactions = "https://www.philippe-fournier-viger.com/spmf/datasets/fruithut_original.txt"
url_taxonomy = "https://www.philippe-fournier-viger.com/spmf/datasets/Fruithut_taxonomy_data.txt"

response_transations = requests.get(url_transactions)
transactions_and_elements_txt = response_transations.text

response_taxonomy = requests.get(url_taxonomy)
taxonomy_txt = response_taxonomy.text

df_taxonomy = np.genfromtxt(io.StringIO(taxonomy_txt), delimiter=',')
df_taxonomy = pd.DataFrame(df_taxonomy)
df_taxonomy = df_taxonomy.astype(int)
df_taxonomy.to_csv('taxonomy.csv', index=False)

elements_data = []
skip_first_line = True
last_index = 0
transactions_and_elements_list = transactions_and_elements_txt.split('\n')

for line in transactions_and_elements_list:
    if skip_first_line:
        skip_first_line = False
        continue

    if line.startswith("@ITEM="):
        line = line.replace("@ITEM=", "")
        parts = line.split("=")
        number = int(parts[0])
        description = parts[1].replace('\r', '')
        elements_data.append([number, description])
        last_index += 1
    elif not line.startswith("@ITEM="):
        break



df_elements = np.array(elements_data)
sorted_indices = np.argsort(df_elements[:, 0].astype(int))
df_elements = df_elements[sorted_indices]
transactions_list = transactions_and_elements_list[last_index+1:]

for i in range(len(transactions_list)):
    transactions_list[i] = transactions_list[i].replace('\r', '')

element_numbers = {row[0]: row[1] for row in df_elements}

transactions_data = []
for line in transactions_list:
    transaction = line.split(' ')
    transaction_data = np.array([1 if element in transaction else 0 for element in element_numbers])
    transactions_data.append(transaction_data)

df_transactions = pd.DataFrame(transactions_data, columns=list(element_numbers.keys()))

print("Taxonomy:")
print(df_taxonomy)
print("\n\nElements descriptions:")
print(df_elements)
print("\n\nTransactions:")
print(df_transactions)

df_transactions.to_csv('transactions.csv', index=False)
