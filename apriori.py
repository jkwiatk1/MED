import pandas as pd
import itertools

########################################
# Step 0: Parameters
########################################
IS_PRINT_ = False
min_support = 100
min_confidence = 0.2


########################################
# Step 1: Load data
########################################
df_transaction_dataset = pd.read_csv('transactions_with_parents.csv')

# ONLY FOR TESTING
df_transaction_dataset = df_transaction_dataset.head(3000)


########################################
# Step 2: Frequency Counting
########################################
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

# Merge occuracy from each individual item with combinations for each hierarchical level
combination_counts_series = pd.Series(combination_counts)
transations_taxonomy_elements_frequency = pd.concat([item_counts, combination_counts_series])

if IS_PRINT_ == True:
    # Print the items counts
    print(item_counts)
    # Print the hierarchy combination counts
    for combination, count in combination_counts.items():
        print(f"Combination: {combination}, Count: {count}")

if IS_PRINT_ == True:
    print(transations_taxonomy_elements_frequency)


########################################
# Step 3: Generate Frequent k-itemsets
########################################
# Function to generate candidate itemsets of length k
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
    if rejected_itemsets:
        itemsets = set(itemset for itemset in itemsets if itemset not in rejected_itemsets)
    for itemset in itemsets:
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
            rejected_itemsets.add(itemset)
    return pruned_itemsets


# Frequent itemsets dictionary
frequent_itemsets = {}

# Initialize frequent 1-itemsets
frequent_1_itemsets = {}

# Set to store rejected itemsets
rejected_itemsets = set()

for item, count in transations_taxonomy_elements_frequency.items():
    if count >= min_support:
        frequent_1_itemsets[frozenset([item])] = count

frequent_itemsets[1] = frequent_1_itemsets

# Generate frequent k-itemsets
k = 2
while frequent_itemsets[k - 1]:
    # Generate candidate itemsets
    candidate_itemsets = generate_candidates(frequent_itemsets[k - 1].keys(), k)

    # Prune infrequent itemsets
    frequent_itemsets[k] = prune_itemsets(candidate_itemsets, min_support, rejected_itemsets)

    k += 1

if IS_PRINT_ == True:
    # Print frequent k-itemsets
    for k, itemsets in frequent_itemsets.items():
        print(f"Frequent {k}-itemsets:")
        for itemset, support in itemsets.items():
            print(f"Itemset: {itemset}, Support: {support}")


########################################
# Step 4: Generate Association Rules
########################################
# Function to generate association rules from frequent itemsets
def generate_association_rules(frequent_itemsets_to_create_rules, min_confidence):
    association_rules = []

    for itemset in frequent_itemsets_to_create_rules.items():
        support_without_tuple = itemset[1]
        itemset = itemset[0]
        new_itemset = True
        last_support_for_tuple = None
        subsets = get_subsets(itemset)

        for subset in subsets:
            antecedent = subset
            consequent = itemset - subset
            if len(antecedent) >= 2 or isinstance(antecedent,tuple) or any(isinstance(x,tuple) for x in consequent):
                    antecedent_support = sum(
                        all(
                            (row[item[0]] > item[1])
                            if isinstance(item, tuple)
                            else (row[item] == 1)
                            for item in antecedent
                        )
                    for _, row in df_transaction_dataset.iterrows()
                    )

                    if new_itemset == True:
                        new_itemset = False
                        base_support = sum(
                            all(
                                (row[item[0]] > item[1])
                                if isinstance(item, tuple)
                                else (row[item] == 1)
                                for item in itemset
                            )
                            for _, row in df_transaction_dataset.iterrows()
                        )

                        last_support_for_tuple = base_support
                    support = last_support_for_tuple
                    if antecedent_support > 0:
                        confidence = support / antecedent_support
                        if confidence >= min_confidence:
                            association_rules.append((antecedent, consequent, support, confidence))
            else:
                antecedent_support = frequent_itemsets[len(antecedent)][antecedent]
                confidence = support_without_tuple / antecedent_support
                if confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, support_without_tuple, confidence))

    return association_rules

# Function to get all possible subsets of an itemset
def get_subsets(itemset):
    subsets = []
    itemset = list(itemset)
    num_items = len(itemset)

    for i in range(1, num_items):
        subsets.extend(itertools.combinations(itemset, i))

    return [frozenset(subset) for subset in subsets]

# Generate association rules from frequent itemsets: [k-2] - last;  [k-3] - one before last
association_rules = generate_association_rules(frequent_itemsets[k-3], min_confidence)

# Print the generated association rules
print("Association Rules:")
for antecedent, consequent, support, confidence in association_rules:
    # print(f"Antecedent: {antecedent}, Consequent: {consequent}, Support: {support}, Confidence: {confidence}")
    antecedent_str = ', '.join([str(item) for item in antecedent])
    consequent_str = ', '.join([str(item) for item in consequent])
    print(f"Antecedent: {antecedent_str}, Consequent: {consequent_str}, Support: {support}, Confidence: {confidence}")






