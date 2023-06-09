import pandas as pd
import numpy as np
import csv

class TaxonomyDictionary:
    def __init__(self, arr, taxonomy_groups):
        self.dictionary = {}
        self.build_dictionary(arr)
        self.extend_dictionary(taxonomy_groups)

    def build_dictionary(self, arr):
        for item in arr:
            key, parent = item
            self.dictionary[key] = [parent]

    def extend_dictionary(self, taxonomy_groups):
        for key, value in self.dictionary.items():
            while True:
                found_match = False
                for group in taxonomy_groups:
                    if value[-1] == group[0]:
                        value.append(group[1])
                        found_match = True
                if not found_match:
                    break
    def get_dictionary(self):
        return self.dictionary
    def get_value(self, key):
        if isinstance(key, list):
            if len(key) > 1:
                return self.dictionary[key[0]][-1]
            nested_dict = self.dictionary
            for k in key:
                nested_dict = nested_dict.get(k, {})
                if not isinstance(nested_dict, dict):
                    return nested_dict
            return nested_dict
        else:
            return self.dictionary.get(key)

def split_base_taxonomy(base):
    first_level = []
    taxonomy_groups = []

    for item in base:
        value_1, value_2 = item
        value_1_str = str(value_1)
        if len(value_1_str) == 4:
            first_level.append(item)
        else:
            taxonomy_groups.append(item)

    return first_level, taxonomy_groups

def read_csv_as_list(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append([int(value) for value in row])
    return data

file_path = 'taxonomy.csv'
df_taxonomy_basic = read_csv_as_list(file_path)
df_transactions = pd.read_csv('transactions.csv')

# Split taxonomy to first level (items -> parents) and others (parents -> parents)
taxonomy_elements_parents, taxonomy_groups = split_base_taxonomy(df_taxonomy_basic)
taxonomy_dict = TaxonomyDictionary(taxonomy_elements_parents, taxonomy_groups).get_dictionary()

# print(taxonomy_dict.get_dictionary())
# print(taxonomy_dict.get_value([1012]))
# print(taxonomy_dict.get_value([1012, 152, 150]))

parents_names = [110, 120, 131, 132, 140, 151, 152, 153, 154, 155, 156, 157, 158, 159, 211, 212, 213, 220, 231, 232, 233, 234, 235, 236, 237, 240, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 130, 150, 210, 230, 100, 200]

# Append the new rows to the existing DataFrame
df_transactions_with_parents = df_transactions.copy(deep=False)
# Add new columns with specified names and values of 0
for name in parents_names:
    df_transactions_with_parents[name] = 0

taxonomy = taxonomy_dict

# Iterate over each row
for i, row in df_transactions.iterrows():
    # Initialize the counts for each row
    row_counts = {}

    # Iterate over each item in the row
    for column, value in row.items():
        # Check if the value is 1
        if value == 1:
            # Iterate over the taxonomy dictionary
            for group, descendants in taxonomy.items():
                # Check if the column is a descendant
                if int(column) == group:
                    # Increment the count for/to all descendants
                    for descendant in descendants:
                        if descendant != group:
                            if descendant in row_counts:
                                row_counts[descendant] += 1
                            else:
                                row_counts[descendant] = 1

    # Add the counts to the appropriate cells in the dataset
    for group, count in row_counts.items():
        df_transactions_with_parents.at[i, group] = count
print(df_transactions_with_parents)
df_transactions_with_parents.to_csv('transactions_with_parents.csv', index=False)


