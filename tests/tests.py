import pandas as pd

data = [
    [100,110,120,130,140,150],
    [0,1,0,1,1,1],
    [0,1,0,0,3,0],
    [0,1,0,1,2,1],
    [0,1,0,0,4,0],
    [0,1,0,0,3,0],
    [0,2,0,0,4,0],
    [0,1,0,0,1,1],
    [1,2,0,0,3,1],
    [0,0,1,1,0,3],
    [1,0,0,1,1,1],
    [1,4,0,0,5,1],
    [0,3,0,0,3,0],
    [0,0,2,0,0,3],
    [0,0,0,2,0,3],
    [0,1,1,2,1,5],
    [1,4,0,4,5,4],
    [1,2,0,0,3,0],
    [1,2,3,4,3,9],
    [0,1,0,1,1,2],
    [0,0,1,1,0,3],
    [0,0,1,2,0,3],
    [0,6,1,1,6,2],
    [1,3,1,0,4,1]
]
df_transaction_dataset = pd.DataFrame(data[1:], columns=data[0])


unique_combinations = set()

# Dictionary to store combination counts
combination_counts = {}


# Iterate over the dataset
for index, row in df_transaction_dataset.iterrows():
    # Iterate over the columns
    for col in df_transaction_dataset.columns:
        # Check if the column is a 3-digit number
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



#########################################################################
# tworzenie silnych reguł ze zbiorów czestych
#########################################################################

df_transaction_dataset = pd.read_csv('transactions_with_parents.csv')

# ONLY FOR TESTING
df_transaction_dataset = df_transaction_dataset.head(3000)


frequent_itemsets = {1: {frozenset({'1002'}): 42, frozenset({'1008'}): 49, frozenset({'1017'}): 86, frozenset({'1021'}): 43, frozenset({'1032'}): 55, frozenset({'1037'}): 39, frozenset({'1039'}): 31, frozenset({'1058'}): 39, frozenset({'1071'}): 44,
                         frozenset({'1077'}): 42, frozenset({'1079'}): 48, frozenset({'1099'}): 36, frozenset({'1111'}): 40, frozenset({'1113'}): 67, frozenset({'2005'}): 35, frozenset({'2010'}): 195, frozenset({'2021'}): 42, frozenset({'2022'}): 81,
                         frozenset({'2030'}): 47, frozenset({'2032'}): 68, frozenset({'2036'}): 152, frozenset({'2038'}): 47, frozenset({'2045'}): 66, frozenset({'2047'}): 30, frozenset({'4029'}): 127, frozenset({'4033'}): 31, frozenset({('151', 1)}): 61,
                         frozenset({('236', 1)}): 101, frozenset({('150', 1)}): 311, frozenset({('230', 1)}): 305, frozenset({('100', 1)}): 321, frozenset({('200', 1)}): 410, frozenset({('110', 1)}): 49, frozenset({('100', 3)}): 88, frozenset({('100', 2)}): 123,
                         frozenset({('100', 4)}): 46, frozenset({('120', 1)}): 32, frozenset({('150', 2)}): 107, frozenset({('153', 1)}): 79, frozenset({('220', 1)}): 287, frozenset({('131', 1)}): 74, frozenset({('130', 1)}): 158, frozenset({('237', 1)}): 68,
                         frozenset({('210', 1)}): 230, frozenset({('200', 3)}): 82, frozenset({('132', 1)}): 125, frozenset({('235', 1)}): 147, frozenset({('154', 1)}): 138, frozenset({('155', 1)}): 72, frozenset({('150', 3)}): 62, frozenset({('212', 1)}): 195,
                         frozenset({('232', 1)}): 108, frozenset({('230', 2)}): 72, frozenset({('220', 2)}): 47, frozenset({('233', 1)}): 56, frozenset({('200', 4)}): 30, frozenset({('200', 2)}): 167, frozenset({('156', 1)}): 51, frozenset({('157', 1)}): 62,
                         frozenset({('159', 1)}): 96, frozenset({('130', 2)}): 37},
           2: {frozenset({('232', 1), '2005'}): 32, frozenset({('100', 1), ('212', 1)}): 35, frozenset({('200', 2), ('235', 1)}): 39, frozenset({('154', 1), ('150', 1)}): 52, frozenset({('230', 2), ('232', 1)}): 30, frozenset({('200', 1), '2010'}): 64,
               frozenset({('200', 1), ('132', 1)}): 38, frozenset({'2045', ('237', 1)}): 64, frozenset({('100', 3), ('150', 2)}): 38, frozenset({('200', 1), ('130', 1)}): 49, frozenset({'1071', ('130', 1)}): 33, frozenset({('220', 1), '2036'}): 113,
               frozenset({'1058', ('156', 1)}): 38, frozenset({'2022', ('235', 1)}): 72, frozenset({('200', 2), ('212', 1)}): 60, frozenset({('100', 1), ('230', 1)}): 64, frozenset({('150', 1), ('235', 1)}): 43, frozenset({('154', 1), ('230', 1)}): 34,
               frozenset({('100', 1), ('235', 1)}): 42, frozenset({'2010', ('220', 1)}): 60, frozenset({('200', 2), '2036'}): 44, frozenset({('220', 1), ('212', 1)}): 60, frozenset({('100', 1), ('154', 1)}): 40, frozenset({('154', 1), '2036'}): 32,
               frozenset({'4029', ('230', 1)}): 31, frozenset({('154', 1), ('212', 1)}): 34, frozenset({('131', 1), ('130', 1)}): 50, frozenset({('233', 1), '2038'}): 44, frozenset({('230', 1), '2022'}): 48, frozenset({('220', 1), '2030'}): 38,
               frozenset({('200', 2), ('230', 1)}): 90, frozenset({('154', 1), ('130', 1)}): 30, frozenset({('200', 1), '4029'}): 60, frozenset({('131', 1), '1021'}): 43, frozenset({('200', 1), ('220', 1)}): 144, frozenset({('220', 1), ('230', 1)}): 71,
               frozenset({('100', 1), '2036'}): 37, frozenset({('150', 1), '1017'}): 30, frozenset({('210', 1), ('232', 1)}): 40, frozenset({('220', 1), ('200', 2)}): 79, frozenset({('131', 1), '4033'}): 31, frozenset({('159', 1), '1017'}): 78,
               frozenset({('236', 1), '2032'}): 62, frozenset({('200', 3), ('212', 1)}): 40, frozenset({('212', 1), ('232', 1)}): 41, frozenset({('200', 1), ('100', 2)}): 38, frozenset({'2010', ('230', 1)}): 54, frozenset({('150', 1), ('230', 1)}): 70,
               frozenset({('220', 1), ('232', 1)}): 33, frozenset({('200', 1), ('210', 1)}): 89, frozenset({('200', 1), ('154', 1)}): 38, frozenset({('154', 1), '1113'}): 65, frozenset({'2010', ('200', 2)}): 60, frozenset({('132', 1), '1071'}): 40,
               frozenset({('200', 1), ('150', 2)}): 32, frozenset({('212', 1), ('150', 1)}): 40, frozenset({('200', 3), ('230', 2)}): 30, frozenset({('159', 1), ('150', 1)}): 35, frozenset({'2010', '2036'}): 37, frozenset({('200', 1), ('212', 1)}): 64,
               frozenset({('150', 1), ('153', 1)}): 42, frozenset({('230', 1), ('232', 1)}): 57, frozenset({('130', 1), '1077'}): 33, frozenset({('100', 1), '2010'}): 35, frozenset({('100', 2), ('230', 1)}): 34, frozenset({('100', 1), ('130', 1)}): 58,
               frozenset({'2010', ('212', 1)}): 195, frozenset({('236', 1), ('230', 1)}): 61, frozenset({('220', 1), '4029'}): 101, frozenset({('235', 1), '2021'}): 37, frozenset({'2010', ('232', 1)}): 41, frozenset({'2032', ('230', 1)}): 33,
               frozenset({('132', 1), ('130', 1)}): 97, frozenset({('200', 1), ('235', 1)}): 60, frozenset({('100', 1), ('210', 1)}): 44, frozenset({('100', 2), ('150', 1)}): 51, frozenset({('220', 1), ('200', 3)}): 38, frozenset({('237', 1), ('230', 1)}): 50,
               frozenset({('220', 1), ('130', 1)}): 31, frozenset({('200', 1), '2022'}): 30, frozenset({('212', 1), ('235', 1)}): 38, frozenset({('200', 1), ('150', 1)}): 86, frozenset({('220', 1), ('150', 1)}): 63, frozenset({('200', 2), ('150', 1)}): 39,
               frozenset({('100', 1), ('200', 2)}): 33, frozenset({('154', 1), '1111'}): 39, frozenset({('100', 1), ('220', 1)}): 63, frozenset({('200', 3), ('230', 1)}): 34, frozenset({('100', 1), ('200', 1)}): 83, frozenset({('212', 1), ('210', 1)}): 185,
               frozenset({('230', 1), ('130', 1)}): 50, frozenset({('230', 2), ('235', 1)}): 33, frozenset({('100', 2), ('130', 1)}): 42, frozenset({('220', 2), '2036'}): 34, frozenset({('151', 1), '1079'}): 48, frozenset({('154', 1), ('210', 1)}): 34,
               frozenset({('210', 1), ('130', 1)}): 34, frozenset({('210', 1), ('230', 1)}): 64, frozenset({('150', 1), ('130', 1)}): 41, frozenset({('100', 1), ('132', 1)}): 38, frozenset({('200', 1), '2036'}): 55, frozenset({'2010', ('210', 1)}): 185,
               frozenset({('100', 1), ('150', 1)}): 239, frozenset({'2010', ('235', 1)}): 38, frozenset({('132', 1), ('150', 1)}): 30, frozenset({('132', 1), '1077'}): 39, frozenset({('212', 1), ('230', 1)}): 54, frozenset({('210', 1), '2036'}): 38,
               frozenset({('155', 1), '1032'}): 55, frozenset({('230', 1), '2036'}): 38, frozenset({'2010', ('200', 3)}): 40, frozenset({('200', 2), '4029'}): 33, frozenset({('132', 1), ('230', 1)}): 45, frozenset({('230', 1), ('235', 1)}): 101,
               frozenset({('220', 1), ('210', 1)}): 66, frozenset({('200', 2), ('232', 1)}): 32, frozenset({('212', 1), '2036'}): 37, frozenset({('200', 2), ('210', 1)}): 69, frozenset({('210', 1), ('235', 1)}): 44, frozenset({'2045', ('230', 1)}): 49,
               frozenset({('200', 1), ('236', 1)}): 44, frozenset({('100', 3), ('150', 3)}): 32, frozenset({('150', 1), ('210', 1)}): 46, frozenset({('150', 1), '2036'}): 40, frozenset({('200', 1), ('230', 1)}): 177, frozenset({('200', 3), ('210', 1)}): 43,
               frozenset({('210', 1), ('230', 2)}): 30, frozenset({'2010', ('154', 1)}): 34, frozenset({('220', 1), ('154', 1)}): 41, frozenset({('220', 1), ('235', 1)}): 40, frozenset({('154', 1), ('150', 2)}): 37, frozenset({'2010', ('150', 1)}): 40,
               frozenset({('100', 3), ('130', 1)}): 30, frozenset({('100', 2), ('150', 2)}): 59},
           3: {frozenset({'2010', ('212', 1), ('230', 1)}): 54, frozenset({'2010', ('210', 1), '2036'}): 35, frozenset({'2010', ('210', 1), ('232', 1)}): 37, frozenset({('200', 1), ('220', 1), ('100', 1)}): 30,
               frozenset({('132', 1), ('230', 1), ('130', 1)}): 34, frozenset({'2010', ('200', 2), ('212', 1)}): 60, frozenset({('200', 2), ('212', 1), ('210', 1)}): 58, frozenset({('200', 1), ('230', 1), ('235', 1)}): 60,
               frozenset({'2010', ('200', 3), ('210', 1)}): 35, frozenset({('200', 1), ('236', 1), ('230', 1)}): 44, frozenset({('132', 1), '1071', ('130', 1)}): 33, frozenset({('212', 1), ('210', 1), ('235', 1)}): 37,
               frozenset({'2010', ('210', 1), ('150', 1)}): 40, frozenset({('154', 1), ('212', 1), ('210', 1)}): 32, frozenset({('100', 1), ('150', 1), ('235', 1)}): 35, frozenset({('200', 3), ('212', 1), ('210', 1)}): 35,
               frozenset({'2010', ('212', 1), ('210', 1)}): 185, frozenset({'2010', ('200', 2), ('210', 1)}): 58, frozenset({('220', 1), ('200', 2), ('230', 1)}): 50, frozenset({('212', 1), ('150', 1), ('210', 1)}): 40, frozenset({('200', 2), ('212', 1), ('230', 1)}): 32, frozenset({('200', 1), '2010', ('210', 1)}): 64, frozenset({'2010', ('212', 1), ('150', 1)}): 40, frozenset({('100', 1), ('132', 1), ('130', 1)}): 38, frozenset({'2010', ('154', 1), ('212', 1)}): 34, frozenset({'2010', ('210', 1), ('220', 1)}): 57, frozenset({'2010', ('212', 1), '2036'}): 37, frozenset({'2010', ('212', 1), ('232', 1)}): 41, frozenset({('100', 1), '2010', ('212', 1)}): 35, frozenset({('212', 1), ('210', 1), ('230', 1)}): 51, frozenset({('200', 2), ('210', 1), ('230', 1)}): 40, frozenset({('220', 1), ('150', 1), '2036'}): 30, frozenset({('100', 1), ('212', 1), ('210', 1)}): 35, frozenset({('236', 1), '2032', ('230', 1)}): 33, frozenset({'2010', ('212', 1), ('220', 1)}): 60, frozenset({('212', 1), ('210', 1), ('232', 1)}): 37, frozenset({'2010', ('154', 1), ('210', 1)}): 32, frozenset({'2045', ('237', 1), ('230', 1)}): 49, frozenset({('100', 1), '2010', ('210', 1)}): 35, frozenset({'2010', ('210', 1), ('230', 1)}): 51, frozenset({'2010', ('200', 2), ('230', 1)}): 32, frozenset({('200', 1), '2010', ('212', 1)}): 64, frozenset({('100', 1), ('220', 1), ('150', 1)}): 50, frozenset({('100', 1), ('230', 1), ('200', 1)}): 39, frozenset({('220', 1), ('212', 1), ('210', 1)}): 57, frozenset({('132', 1), ('130', 1), '1077'}): 33, frozenset({('100', 1), ('150', 1), '2036'}): 33, frozenset({('200', 1), '2022', ('235', 1)}): 30, frozenset({('200', 1), ('100', 1), ('150', 1)}): 62, frozenset({'2010', ('212', 1), ('235', 1)}): 38, frozenset({('100', 1), ('150', 1), ('210', 1)}): 32, frozenset({'2010', ('200', 3), ('212', 1)}): 40, frozenset({('200', 1), ('220', 1), '4029'}): 60, frozenset({'2010', ('210', 1), ('235', 1)}): 37, frozenset({('200', 1), ('220', 1), '2036'}): 55, frozenset({('159', 1), ('150', 1), '1017'}): 30, frozenset({('220', 1), ('200', 2), '2036'}): 31, frozenset({('200', 1), ('230', 1), '2022'}): 30, frozenset({('212', 1), ('210', 1), '2036'}): 35, frozenset({('100', 2), ('150', 1), ('130', 1)}): 37, frozenset({('100', 1), ('154', 1), ('150', 1)}): 40, frozenset({('200', 1), ('132', 1), ('130', 1)}): 30, frozenset({('200', 1), ('150', 1), ('230', 1)}): 43, frozenset({('200', 1), ('212', 1), ('210', 1)}): 64, frozenset({('100', 1), ('150', 1), ('230', 1)}): 44, frozenset({('230', 1), '2022', ('235', 1)}): 48},
           4: {frozenset({'2010', ('200', 1), ('212', 1), ('210', 1)}): 64, frozenset({'2022', ('235', 1), ('200', 1), ('230', 1)}): 30, frozenset({'2010', ('200', 2), ('212', 1), ('210', 1)}): 58, frozenset({('154', 1), '2010', ('212', 1), ('210', 1)}): 32,
               frozenset({'2010', ('235', 1), ('212', 1), ('210', 1)}): 37, frozenset({'2010', ('200', 2), ('210', 1), ('230', 1)}): 32, frozenset({'2010', ('150', 1), ('212', 1), ('210', 1)}): 40, frozenset({'2010', '2036', ('212', 1), ('210', 1)}): 35,
               frozenset({'2010', ('100', 1), ('212', 1), ('210', 1)}): 35, frozenset({'2010', ('212', 1), ('210', 1), ('232', 1)}): 37, frozenset({'2010', ('220', 1), ('212', 1), ('210', 1)}): 57, frozenset({'2010', ('200', 2), ('212', 1), ('230', 1)}): 32,
               frozenset({('200', 2), ('212', 1), ('210', 1), ('230', 1)}): 32, frozenset({'2010', ('200', 3), ('212', 1), ('210', 1)}): 35, frozenset({'2010', ('212', 1), ('210', 1), ('230', 1)}): 51},
           5: {frozenset({'2010', ('210', 1), ('230', 1), ('200', 2), ('212', 1)}): 32},
           6: {}}
k = 6
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

import itertools
# Function to get all possible subsets of an itemset
def get_subsets(itemset):
    subsets = []
    itemset = list(itemset)
    num_items = len(itemset)

    for i in range(1, num_items):
        subsets.extend(itertools.combinations(itemset, i))

    return [frozenset(subset) for subset in subsets]


# Set the minimum confidence threshold for association rules
min_confidence = 0.1

# Generate association rules from frequent itemsets
association_rules = generate_association_rules(frequent_itemsets[k-2], min_confidence)

# Print the generated association rules
print("Association Rules:")
for antecedent, consequent, support, confidence in association_rules:
    # print(f"Antecedent: {antecedent}, Consequent: {consequent}, Support: {support}, Confidence: {confidence}")
    antecedent_str = ', '.join([str(item) for item in antecedent])
    consequent_str = ', '.join([str(item) for item in consequent])
    print(f"Antecedent: {antecedent_str}, Consequent: {consequent_str}, Support: {support}, Confidence: {confidence}")
