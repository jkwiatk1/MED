import pandas as pd

'''
from mlxtend.frequent_patterns import apriori, association_rules
transaction = pd.read_csv('transactions.csv')

# Apply the Apriori algorithm
frequent_itemsets = apriori(transaction, min_support=0.01, use_colnames=True)

# Generate association rules
association_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)

# Print the frequent itemsets and association rules
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(association_rules)
'''

df_transaction_dataset = pd.read_csv('transactions_with_parents.csv')


# Count the occurrences of each individual item (4-digit columns)
item_counts = df_transaction_dataset[[col for col in df_transaction_dataset.columns if col.isdigit() and len(col) == 4]].sum()
print(item_counts)


# Sum up the occurrences of identical combinations separately for each hierarchical level (3-digit columns)
# Set to store unique combinations
unique_combinations = set()

# Dictionary to store combination counts
combination_counts = {}

# Iterate over the dataset
for index, row in df_transaction_dataset.iterrows():
    # Iterate over the columns
    for col in df_transaction_dataset.columns:
        # Check if the column is a 3-digit number
        if col.isdigit() and len(col) == 3:
            value = row[col]
            # Check if the value is not 0
            if value != 0:
                combination_key = (col,value)
                # Check if the combination exists in the set
                if combination_key in unique_combinations:
                    # Increment the count for the combination
                    combination_counts[combination_key] += 1
                else:
                    # Add the new combination to the set and initialize its count to 1
                    unique_combinations.add(combination_key)
                    combination_counts[combination_key] = 1

# Print the combination counts
for combination, count in combination_counts.items():
    print(f"Combination: {combination}, Count: {count}")
