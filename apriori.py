import pandas as pd

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


'''
# Step 3: Generate Frequent k-itemsets
# Assuming you have defined the minimum support threshold as 'min_support'
frequent_itemsets = []
k = 1
while True:
    candidate_itemsets = list(combinations(item_counts.index, k))
    frequent_candidates = []
    for itemset in candidate_itemsets:
        if all(item_counts[item] >= min_support for item in itemset):
            frequent_candidates.append(itemset)
    if not frequent_candidates:
        break
    frequent_itemsets.extend(frequent_candidates)
    k += 1

# Step 4: Generate Association Rules
# Assuming you have defined the minimum confidence threshold as 'min_confidence'
association_rules = []
for itemset in frequent_itemsets:
    if len(itemset) > 1:
        subsets = list(combinations(itemset, len(itemset) - 1))
        for subset in subsets:
            antecedent_support = item_counts[list(subset)].min()
            consequent_support = item_counts[itemset].min()
            confidence = consequent_support / antecedent_support
            if confidence >= min_confidence:
                rule = (list(subset), list(set(itemset) - set(subset)), confidence)
                association_rules.append(rule)

# Print the frequent itemsets and association rules
print("Frequent Itemsets:")
for itemset in frequent_itemsets:
    print(itemset)

print("\nAssociation Rules:")
for rule in association_rules:
    print(f"Antecedent: {rule[0]}, Consequent: {rule[1]}, Confidence: {rule[2]}")
'''





