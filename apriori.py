import pandas as pd

IS_PRINT_ = False
min_support = 20

df_transaction_dataset = pd.read_csv('transactions_with_parents.csv')
df_transaction_dataset = df_transaction_dataset.head(2000)

# Count the occurrences of each individual item (4-digit columns)
item_counts = df_transaction_dataset[[col for col in df_transaction_dataset.columns if col.isdigit() and len(col) == 4]].sum()

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

if IS_PRINT_ == True:
    # Print the items counts
    print(item_counts)
    # Print the hierarchy combination counts
    for combination, count in combination_counts.items():
        print(f"Combination: {combination}, Count: {count}")

# Function to generate candidate itemsets of length k
def generate_candidates(prev_itemsets, k):
    candidates = set()
    for itemset1 in prev_itemsets:
        for itemset2 in prev_itemsets:
            if len(itemset1.union(itemset2)) == k:
                candidates.add(itemset1.union(itemset2))
    return candidates

# Function to prune infrequent itemsets
def prune_itemsets(itemsets, min_support):
    pruned_itemsets = {}
    for itemset in itemsets:
        support = sum(1 for _, row in df_transaction_dataset.iterrows() if all(row[item] != 0 for item in itemset))
        if support >= min_support:
            pruned_itemsets[itemset] = support
    return pruned_itemsets



# Frequent itemsets dictionary
frequent_itemsets = {}

# Initialize frequent 1-itemsets
frequent_1_itemsets = {}
for item, count in item_counts.items():
    if count >= min_support:
        frequent_1_itemsets[frozenset([item])] = count

frequent_itemsets[1] = frequent_1_itemsets

# Generate frequent k-itemsets
k = 2
while frequent_itemsets[k - 1]:
    # Generate candidate itemsets
    candidate_itemsets = generate_candidates(frequent_itemsets[k - 1].keys(), k)

    # Prune infrequent itemsets
    frequent_itemsets[k] = prune_itemsets(candidate_itemsets, min_support)

    k += 1

# Print frequent k-itemsets
for k, itemsets in frequent_itemsets.items():
    print(f"Frequent {k}-itemsets:")
    for itemset, support in itemsets.items():
        print(f"Itemset: {itemset}, Support: {support}")




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





