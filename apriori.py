import pandas as pd

IS_PRINT_ = False
min_support = 30

df_transaction_dataset = pd.read_csv('transactions_with_parents.csv')

# ONLY FOR TESTING
df_transaction_dataset = df_transaction_dataset.head(1000)

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



# Merge occuracy from each individual item with combinations for each hierarchical level
combination_counts_series = pd.Series(combination_counts)
transations_taxonomy_elements_frequency = pd.concat([item_counts, combination_counts_series])
# # Convert the merged Series to a DataFrame
# merged_df = pd.DataFrame({'Count': transations_taxonomy_elements_frequency})
#
# # Reset index of the merged DataFrame to make the columns accessible
# merged_df.reset_index(inplace=True)
# merged_df.rename(columns={'index': 'Item'}, inplace=True)

if IS_PRINT_ == True:
    print(transations_taxonomy_elements_frequency)



# Function to generate candidate itemsets of length k
'''
mozna zamiast dwoch petli uzyc 
import itertools
for combination in itertools.combinations(prev_itemsets, 2):
    candidates2.add(frozenset(combination))
'''
def generate_candidates(prev_itemsets, k):
    candidates = set()
    for itemset1 in prev_itemsets:
        for itemset2 in prev_itemsets:
            if len(itemset1.union(itemset2)) == k:
                candidates.add(itemset1.union(itemset2))
    return candidates



# Function to prune infrequent itemsets
def prune_itemsets(itemsets, min_support, rejected_itemsets):
    pruned_itemsets = {}
    filtered_itemsets = set(itemset for itemset in itemsets if itemset not in rejected_itemsets)
    for itemset in filtered_itemsets:
        support = sum(
            all(
                (item[0] in row and row[item[0]] == item[1])
                if isinstance(item, tuple)
                else (item in row and row[item] != 0)
                for item in itemset
            )
            for _, row in df_transaction_dataset.iterrows()
        )
        if support >= min_support:
            pruned_itemsets[itemset] = support
        else:
            rejected_itemsets.append(itemset)
    return pruned_itemsets

########################################
# Step 3: Generate Frequent k-itemsets
########################################
# Frequent itemsets dictionary
frequent_itemsets = {}

# Initialize frequent 1-itemsets
frequent_1_itemsets = {}

# List to store rejected itemsets
rejected_itemsets = []

for item, count in transations_taxonomy_elements_frequency.items():
    if count >= min_support:
        frequent_1_itemsets[frozenset([item])] = count
    else:
        rejected_itemsets.append(item)

frequent_itemsets[1] = frequent_1_itemsets

# Generate frequent k-itemsets
k = 2
while frequent_itemsets[k - 1]:
    # Generate candidate itemsets
    candidate_itemsets = generate_candidates(frequent_itemsets[k - 1].keys(), k)

    # Prune infrequent itemsets
    frequent_itemsets[k] = prune_itemsets(candidate_itemsets, min_support, rejected_itemsets)

    k += 1

# Print frequent k-itemsets
for k, itemsets in frequent_itemsets.items():
    print(f"Frequent {k}-itemsets:")
    for itemset, support in itemsets.items():
        print(f"Itemset: {itemset}, Support: {support}")




'''
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





