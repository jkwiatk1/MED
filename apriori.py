from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

dataset = pd.read_csv('transactions.csv')

# Apply the Apriori algorithm
frequent_itemsets = apriori(dataset, min_support=0.01, use_colnames=True)

# Generate association rules
association_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)

# Print the frequent itemsets and association rules
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(association_rules)